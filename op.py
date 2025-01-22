from base import *

# =============================================================================
# notes 
# ** img to be ocr'd should be of QImage.Format_Indexed8 (grayscale)
# =============================================================================

import books
span = books.span
zo = books.zo
# XXX hardcoded magic; 
md = QTransform(2, 0, 0, 2, 0, 0)

prf_fit_width, prf_fit_height = range(2)

def bk(name):
    m = __import__(name)
    return getattr(m, name)()

def boxes(i, s):
    p = popen(['/home/cytu/usr/src/cpp/text_mask', i, s], stdout=pipe, universal_newlines=True)
    r = p.communicate()[0]
    try:
        return [tuple(int(n) for n in b.split(',')) for b in r.split('\n') if ',' in b]
    except:
        return []

def matches(f_i, f_t, score=70):
    p = popen(['/home/cytu/usr/src/cpp/match', f_i, f_t, str(score)], stdout=pipe, universal_newlines=True)
    r = p.communicate()[0]
    if r.find('ERROR') != -1:
        return []
    l = [[i for i in b.split(',') if i.strip()] for b in r.split('\n') if b.strip()]
    return l

def ocr(f_i, f_w):
    p = popen(['tesseract', f_i, f_w, '--psm', '7'], stdout=pipe, universal_newlines=True)
    r = p.communicate()[0]
    try:
        # Note that tesseract will automatically add suffix '.txt' to output file!
        if os.path.isfile(f_w + '.txt'):
            return True
        return False
    except:
        return False 

def get_s(f):
    s = ''
    try:
        s = codecs.open(f, 'r', 'utf-8-sig').read().strip()
    
    finally:
        return s
    
def get_ocr(f, p):
    try:
        s = get_s(f) 
        match = re.compile(p).match(s)
        return match, s

    except:
        return None, ''

def get_z(bx):
    try:
        return 0.93 * w_desktop * zo / (2 * span(bx)[2]) 
    except:
        return 0
    
def get_bx(i, td, book, morph=''):
    f = cat(td, 'box.tif')
    i.convertToFormat(QImage.Format_Indexed8).save(f)
    return boxes(f, morph if morph else book.morph0)

def get_corr(i, td, book, nn=(-1, 0, 1, 0)):
    bxl = get_bx(i, td, book, 'c3.1')
    n = len(bxl) 
    rw = sum(sorted([bb[2] for bb in bxl])) // n
    rh = sum(sorted([bb[-1] for bb in bxl])) // n
    return (nn[0] * rw, nn[1] * rh, nn[2] * rw, nn[3] * rh)

def get_y(book, bx):
    if bx:
        return book.ym(bx)
    return [] 

def get_tk(i, td, book, bx, n_pg='', corr=None):
    tkdl = []
    if bx:
        bxs = book.bxs(bx)
        for tk, spec in book.tokens.items():
            if not spec:
                continue
            for b in getattr(bxs, spec['class'])():
                # early exit of none ocr token s
                if not spec.get('ocr', ''):
                    tkdl.append((b, tk, '', ''))
                    continue

                # convert to grayscale 
                r = md.mapRect(QRect(*b))
                # adjust r
                if corr:
                    rc = md.mapRect(QRect(*corr))
                    rw, rh = rc.width(), rc.height()
                    r.adjust(-rw, -rh, rw, rh)
                f_i = cat(td, f'ocr_{n_pg}_{b}.tif') 
                if not os.path.isfile(f_i):
                    i.copy(r).convertToFormat(QImage.Format_Indexed8).save(f_i)

                # ocr
                f_w = cat(td, f'ocr_{n_pg}_{b}')
                f_w_t = f_w + '.txt'
                if not os.path.isfile(f_w_t):
                    # tesseract may fail
                    if not ocr(f_i, f_w):
                        continue
                
                m = get_ocr(f_w_t, spec['ocr'])[0]
                if m is not None:
                    s = m.groups()[0] if len(m.groups()) else m.group(0)
                    tkdl.append((b, tk, s, ''))
    return tkdl

def get_gap(bx):
    bbx = sorted(bx, key=lambda b: b[1])
    l1 = [b[1] for b in bx]
    l1.extend([b[1] + b[-1] for b in bx])
    l2 = sorted(l1)
    gapdl = []
    gap = []
    for n, i in enumerate(l2):
        if n < len(l2) - 1:
            mid = (l2[n] + l2[n + 1]) / 2
            is_in = False
            for b in bbx:
                if b[1] > mid:
                    break
                if (b[1] + b[-1]) >= mid and b[1] <= mid:
                    is_in = True
                    break
            if is_in:
                if gap:
                    gapdl.append((gap[0][0], gap[-1][-1]))
                    gap = []
            else:
                gap.append((l2[n], l2[n + 1]))
    if gap:
        gapdl.append((gap[0][0], gap[-1][-1]))
    return sorted(gapdl)

def get_l(tkd, yd):
    ll = []
    if tkd is None:
        return ll
    
    for pg in tkd:
        for b, tk, s, ke in tkd[pg]:
            # XXX 
            try:
                ymin, ymax = yd[int(pg)]  
                if b[1] >= ymin and (b[1] + b[-1]) <= ymax: 
                    ll.append((int(pg), b[1], tk, s, ke))
            except:
                continue
    return ll

def get_qa(book, tkd, bxd, yd, tkd_man=None):
    bxd = dict((int(k), [tuple(ii) for ii in i]) for k, i in bxd.items())
    yd = dict((int(k), i) for k, i in yd.items())

    sieve = book.sieve
    l = []
    l.extend(get_l(tkd, yd))
    l.extend(get_l(tkd_man, yd))
   
    l = sorted(l)
    n_l = len(l)
    qa = {'q': {}, 'a': {}}
    d_tk = {}
    
    for (n1, y1, tk1, s1, ke1), (n2, y2, tk2, s2, ke2) in [(l[i], l[i + 1]) for i in range(n_l) if i < n_l - 1]:
        b_skip, d_tk = book.tk_action((tk1, s1), d_tk)
        if b_skip:
            continue
        aa = []
        if n1 == n2: 
            # within the same page
            try:
                bx = bxd[n1]
                y = yd[n1]
                a = span(sieve(bx, y1, y2, y)) 
                if a:
                    aa = [(n1, a)]
            except:
                pass

        else:  
            # across several pages
            for i in range(n1, n2 + 1):
                try:
                    bx = bxd[i]
                    y = yd[i]
                except:
                    continue

                if i == n1:
                    # first page
                    sv = sieve(bx, y1=y1, ym=y)

                elif i == n2:
                    # last page 
                    sv = sieve(bx, y2=y2, ym=y)
                
                else:  
                    # in between
                    sv = sieve(bx, ym=y)
                
                a = span(sv) 
                if a:
                    aa.append((i, a))

        if ke1:
            d_tk['k'] = ke1
        
        try:
            k, q_or_a = d_tk['k'], d_tk['q_or_a']
            if aa:
                if k in qa[q_or_a]: 
                    qa[q_or_a][k].extend(aa)
                else:
                    qa[q_or_a][k] = aa
        except:
            continue
    
    s_q = set(qa['q'].keys())
    s_a = set(qa['a'].keys())

    return {'qa': qa, 'err_q_no_a': sorted(list(s_q - s_a)), 'err_a_no_q': sorted(list(s_a - s_q)),}

def tk_k_real(book, tkd, yd, tkd_man=None):
    yd = dict((int(k), i) for k, i in yd.items())
    l = []
    l.extend(get_l(tkd, yd))
    l.extend(get_l(tkd_man, yd))
   
    l = sorted(l)
    n_l = len(l)
    d_tk = {}
    
    d = {}
    for (n1, y1, tk1, s1, ke1), (n2, y2, tk2, s2, ke2) in [(l[i], l[i + 1]) for i in range(n_l) if i < n_l - 1]:
        b_skip, d_tk = book.tk_action((tk1, s1), d_tk)
        if b_skip:
            continue
        #print(d_tk['k'])
        d[(n1, y1, tk1, s1, ke1)] = ke1 if ke1 else d_tk['k']
    return d 

def get_sep_sym(bx, fi, fs, score=75.0):
    o = []
    for s, x, y in matches(fi, fs):  
        s, x, y = float(s), int(x), int(y)
        if s < score:
            print(s, x, y) 
            continue
        # note that b produced by leptonica are 1/2 of the original!
        o.append(y / 2)
    return o

def get_sep_heu(book, bx, gaps, y, typ='median'):
    bxs = book.bxs(bx)
    l = sorted([b - a for a, b in gaps])
    thr = 1.8 * (sum(l) / len(l) if typ == 'avg' else l[len(l)/2]) if l else 0
    # XXX a - 1 hack
    return [yy for yy in [a - 1 for a, b in gaps if (b in [i[1] for i in getattr(bxs, 'indent1')()]) and (b - a) >= thr] if (yy - y) > 2 * thr]
    
def parse(name):
    book = bk(name)    
    dc = book.doc()
    dc.set_z(zo)
    td = tempfile.mkdtemp(dir=tmp)
    
    tkd, bxd, yd = {}, {}, {}
    lz = []
    tic = dt_now()
    pgl = book.pgs
    corr = []
    for ii, n_pg in enumerate(pgl):
        log(f'processing page {n_pg:4d} ({ii + 1:4d} of {len(pgl):4d}: {int((ii + 1) * 100. / len(pgl)):4d} %) ... time elapsed: {lapse(dt_now() - tic)}')
        
        i = dc.render(n_pg)
        if i is None:
            continue
        
        # get bx
        bx = get_bx(i, td, book)
        if bx: 
            bxd.update({n_pg: bx})

        # get best z 
        z = get_z(bx)
        if z:
            lz.append(z)

        # compute y bound
        y = get_y(book, bx)
        if y:
            yd.update({n_pg: y})

        # get correction
        if not corr:
            corr = get_corr(i, td, book, book.nn_corr)

        # get tokens
        tk = get_tk(i, td, book, bx, n_pg, corr)
        if tk:
            tkd.update({n_pg: tk})
    
    try:
        z = sorted(lz)[len(lz) // 2]

    except:
        z = 2.7
    
    d = {'src': book.src, 'sha': sha(book.src), 'name': name, 'zo': zo, 'z': z, 'w_desktop': w_desktop, 
         'dpix': dpix, 'bxd': bxd, 'tkd': tkd, 'yd': yd, 'tkd_man': {}}
    
    book.post(d)

    try:
        d.update(get_qa(book, tkd, bxd, yd))

    except:
        log(f'error generating [{name}] qa: skipped')

    log(f'\nparsing completed; total time lapse: {lapse(dt_now() - tic)}')
    
    shutil.rmtree(td)
    return d

def pg_fact(qa):
    d = {}
    for typ in ['q', 'a']:
        for k in qa[typ]:
            for pg, a in qa[typ][k]:
                if pg not in d:
                    d[pg] = []
                d[pg].append([k, a, typ])
    return d

def render_i(i, l, mm, b_text=False):
    p = QPainter(i)
    p.setFont(QFont('Helvetica', 24))
    for k, a, typ in l:
        pen = QPen()
        pen.setColor(QColor('blue' if typ == 'a' else 'red'))
        pen.setWidth(2)
        p.setPen(pen)
        br = QBrush(QColor(0 if typ == 'a' else 255, 0, 0, 32))
        p.setBrush(br)
        r = mm.mapRect(QRectF(*a)).toRect()
        p.drawRect(r)
        if b_text:
            p.drawText(r.x(), r.y(), k)
        #p.drawText(r, Qt.AlignCenter, k)
    p.end()

def render_pg_fact(l, pg, dc, mm, td):
    try:
        i = dc.render(pg) 
        render_i(i, l, mm)
        f = cat(td, f'{pg}_pg.png')
        i.save(f)
        return True, f

    except:
        return False, ''

def render(qa, k, book, dc, mm, td):
    aa1 = qa['q'].get(k, [])
    aa2 = qa['a'].get(k, [])
    
    for n_pg, a in (aa1 + aa2):
        f = cat(td, f'{n_pg}.tif')
        if not os.path.isfile(f):
            i = dc.render(n_pg)
            i.save(f)
    
    for ii, ll in enumerate([aa1, aa2]):
        for n_pg, a in ll:
            f = cat(td, f'{k}_comp_{n_pg}.png')
            i = QImage(f if os.path.isfile(f) else cat(td, f'{n_pg}.tif'))
            p = QPainter(i)
            pen = QPen()
            pen.setColor(QColor('blue' if ii else 'red'))
            pen.setWidth(2)
            p.setPen(pen)
            br = QBrush(QColor(0 if ii else 255, 0, 0, 32))
            p.setBrush(br)
            p.drawRect(mm.mapRect(QRectF(*a)).toRect())
            p.end()
            i.save(f)

    pl, pr, pt, pb, wp = 30, 30, 30, 30, 6 
    c = {}
    for nn, ll in enumerate([aa1, aa2]):
        l = []
        for n_pg, a in ll: 
            i = QImage(cat(td, f'{n_pg}.tif'))
            l.append(i.copy(mm.mapRect(QRectF(*a)).toRect()))
        try:
            c[nn] = combine(l, width_qa(l))
        except:
            c[nn] = QImage()

    l = []
    for nn in range(2):
        sz = QSize(max([v.width() for v in c.values()]) + pl + pr + 2 * wp, c[nn].height() + pt + pb + 2 * wp)
        i = QImage(sz, QImage.Format_RGB32)
        i.fill(QColor('white').rgb())
        p = QPainter(i)
        p.drawImage(QPoint(pl + wp, pt + wp), c[nn])
        
        if book.replace_title:
            f_b = cat(td, f'box_{k}_{nn}.tif')
            i.convertToFormat(QImage.Format_Indexed8).save(f_b)
            # find out first line
            bx = boxes(f_b, book.morph0)
            if bx:
                l1 = [b for b in sorted(bx, key=lambda b: b[1]) if (b[2] > 50 and b[-1] > 5)][0]
                f_b = cat(td, f'box_{k}_{nn}_.tif')
                i.copy(md.mapRect(QRect(*l1))).convertToFormat(QImage.Format_Indexed8).save(f_b)
                bx1 = boxes(f_b, book.morph1)
                # get first word
                if bx1:
                    r = QRect(*sorted(bx1, key=lambda b:b[0] + b[1])[0]).translated(*l1[:2])
                    r1 = QRect(r.x(), r.y(), r.height(), r.height())
                    p.save()
                    # clear the numbering
                    p.setBrush(QBrush(QColor('white')))
                    p.setPen(Qt.NoPen)
                    p.drawRect(md.mapRect(r))
                    if nn:
                        p.setBrush(QBrush(QColor('black')))
                    wp1 = 3 
                    p.setPen(QPen(QBrush(QColor('black')), wp1, join=Qt.MiterJoin))
                    p.drawRect(md.mapRect(r1))
                    p.restore()

        combine([i,], width_qa([i,]), 0).save(cat(td, f"{k}_{'ans' if nn else 'prob'}.png"))
        # draw the black frame for question
        pen = QPen()
        pen.setColor(QColor('black'))
        pen.setWidth(wp)
        p.setPen(pen)
        if nn == 0:
            p.drawRect(QRect(QPoint(0, 0), sz))
        p.end()
        l.append(i)
    combine(l, width_qa(l), 0).save(cat(td, f'{k}_fact.png'))

def rename_fact_qa_png(fd):
    ff = []
    for root, dirs, files in os.walk(fd):
        for f in files:
            if f.find('_fact.png') != -1 or f.find('_prob.png') != -1 or f.find('_ans.png') != -1:
                ff.append(f)
    keys = list(set([f.replace('_fact.png', '').replace('_prob.png', '').replace('_ans.png', '') for f in ff]))

    def mycmp(s):
        # assume the folder name is the same as ana
        dd = get_ana(os.path.split(fd)[1])
        # sort by page and y
        q1 = dd['qa']['q'][s][0]
        return (q1[0], q1[1][1])

    keys = sorted(keys, key=mycmp)

    digits = 4 #XXX round(math.log(len(keys), 10) + 1)
    ddd = dict([(i, str(ii + 1).zfill(digits)) for ii, i in enumerate(keys)])
    
    for f in ff:
        for ft in ['fact', 'prob', 'ans',]:
            if f.find(f'_{ft}.png') != -1:
                key = f.replace(f'_{ft}.png', '')
                fts = ''
                if ft == 'prob':
                    fts = '_prob'
                elif ft == 'ans':
                    fts = '_ans'
                os.rename(cat(root, f), cat(root, ddd[key] + '_' + key + fts + '.png'))  

def render_all(name, td='', b_fact_qa_only=True, b_rename_fact_qa_png=True, b_remove_prob_ans_png=False, b_render_q_no_a=False):
    d = get_ana(name) 
    zo = d['zo']
    z = d['z'] * 0.96 * w_desktop / d['w_desktop']
    base_dpix = d.get('dpix', 96)
    zz = 2. * z / zo * dpix / base_dpix
    mm = QTransform(zz, 0, 0, zz, 0, 0)

    book = bk(name)
    dc = book.doc()
    dc.set_z(z)
    dc1 = book.doc()

    if td:
        if not os.path.isdir(td):
            os.mkdir(td)
    else:
        td = tempfile.mkdtemp(prefix=name + '_', dir=tmp)
    
    qa = d['qa']
    
    def right(key, keywords=['Theorem', 'Lemma', 'Corollary', 'Definition', 'Example']):
        for keyword in keywords:
            if key.find(keyword) != -1:
                return True
        return False
        
    qa_ = set(qa['q'].keys()) & set(qa['a'].keys())
    qa_proper = qa_.union(set([key for key in qa['q'].keys() if right(key)])) if b_render_q_no_a else qa_
    for k in qa_proper:
        render(qa, k, book, dc, mm, td)
    
    pf = pg_fact(qa)
    for pg in pf:
        render_pg_fact(pf[pg], pg, dc, mm, td)

    # remove all tifs
    ff = []
    for root, dirs, files in os.walk(td):
        for f in files:
            if fnmatch(f, '*.tif'):
                ff.append(cat(root, f))
    for f in ff:
        os.remove(f)

    # remove all comps, pgs
    if b_fact_qa_only:
        ff = []
        for root, dirs, files in os.walk(td):
            for f in files:
                if f.find('_comp_') != -1 or f.find('_pg') != -1:
                    ff.append(cat(root, f))
        for f in ff:
            os.remove(f)

    if b_rename_fact_qa_png:
        rename_fact_qa_png(td)

    if b_remove_prob_ans_png:
        ff = []
        for root, dirs, files in os.walk(td):
            for f in files:
                if f.find('_prob.png') != -1 or f.find('_ans.png') != -1:
                    ff.append(cat(root, f))
        for f in ff:
            os.remove(f)

# XXX from os.walk or query dd['qa']?
def pixd(dd, td):
    qa = dd['qa']

    fact_pg, fact, prob, ans, comp = [], [], [], [], []
    for root, dirs, files in os.walk(td):
        for f in files:
            ff = cat(root, f)
            if fnmatch(f, '*_fact.png'):
                fact.append(ff)
            elif fnmatch(f, '*_pg.png'):
                fact_pg.append(ff)
            elif fnmatch(f, '*_prob.png'):
                prob.append(ff)
            elif fnmatch(f, '*_ans.png'):
                ans.append(ff)
            elif fnmatch(f, '*.png'): 
                comp.append(ff)
        
    ks = [f_no_ext(i)[:-5] for i in fact]
    pgs = [f_no_ext(i)[:-3] for i in fact_pg]
    p = re.compile(r'^(.+)_comp_(\d+)$')
    
    d_k, d_pg = {}, {}
    for i in comp:
        m = p.match(f_no_ext(i))
        
        k = m.group(1)
        if k not in d_k:
            d_k[k] = []
        d_k[k].append(i) 
        
        pg = m.group(2)
        if pg not in d_pg:
            d_pg[pg] = []
        d_pg[pg].append(i)
    
    return {'comp_by_k': d_k, 'comp_by_pg': d_pg,
            'fact_by_k': dict([(f_no_ext(i)[:-5], [i]) for i in fact]), 
            'fact_by_pg': dict([(str(pg), list(set([cat(td, f'{i[0]}_fact.png') for i in ii]))) for pg, ii in pg_fact(qa).items()]), 
            'comp': comp, 'fact': fact, 'pgs': pgs, 'ks': ks}

def update_qa(d):
    try:
        qa = get_qa(bk(d['name']), d['tkd'], d['bxd'], d['yd'], d['tkd_man'])
        d.update(qa)
        return True
    
    except:
        traceback.print_exc()
        log(f"error generating [{d['name']}] qa: skipped")
        return False

def erase_ana(name, l):
    book = bk(name)
    d = get_ana(name)
    for s in ['bxd', 'tkd', 'yd', 'tkd_man']:
        for pg in d[s]:
            if int(pg) in l:
                d[s][pg] = []
    update_qa(d)
    save_ana(d)

def update_ana(b_sha=False):
    t = []
    for root, dirs, files in os.walk(cwd):
        for f in files:
            if fnmatch(f, '*.ana'):
                t.append(os.path.splitext(f)[0])
    for n in t:
        d = get_ana(n)
        if d:
            b = update_qa(d)
            if b_sha:
                d['sha'] = sha(bk(n).src)
            print(n, b)
            save_ana(d)
        else:
            print(n, f'load [{n}] error')

def update_ana_dpix():
    t = []
    for root, dirs, files in os.walk(cwd):
        for f in files:
            if fnmatch(f, '*.ana'):
                t.append(os.path.splitext(f)[0])
    for n in t:
        d = get_ana(n)
        if d:
            d['dpix'] = 96
            save_ana(d)
        else:
            print(n, f'load [{n}] error')

def delete_tk(n, tpl):
    d = get_ana(n)
    tkd = d['tkd']
    for pg in tkd:
        l = []
        for tk in tkd[pg]:
            if tk[1] in tpl:
                l.append(tk)
        tkd[pg] = [tk for tk in tkd[pg] if tk not in l]
    update_qa(d)
    save_ana(d)

def wipe_all(n, pgs):
    d = get_ana(n)
    for s in ['bxd', 'yd', 'tkd_man', 'tkd']:
        t = d[s]
        for pg in pgs:
            try:
                del t[pg]
            except:
                continue
    update_qa(d)
    save_ana(d)

class pix_view(QGraphicsView):
    
    msg_pix_view = pyqtSignal(dict)

    def __init__(self, par=None):
        super(pix_view, self).__init__(par)
        self.setRenderHints(QPainter.Antialiasing|QPainter.TextAntialiasing)
        self.scn = QGraphicsScene(self)
        self.setScene(self.scn)
        self.pix = []
        self.ix = 0
        self.z = 1.0
        self.prf = prf_fit_width
    
    def send(self, **d):
        self.msg_pix_view.emit(d)

    def set_prf(self, prf):
        if prf == self.prf:
            return
        self.prf = prf
        self.display()

    def navigate(self, forward=True):
        i = self.ix
        if self.pix:
            self.ix += (1 if forward else -1)
            self.ix %= len(self.pix)
        else:
            self.ix = 0
        if self.ix != i:
            self.display()
            self.verticalScrollBar().setValue(0)
    
    def load_pix(self, pix):
        if pix:
            self.pix = pix
            self.ix = 0
            self.display()

    def display(self):
        scn = self.scn
        scn.clear()
        try:
            pix = self.pix[self.ix]
        except:
            return

        p = QPixmap(pix)
        if p.width():
            if self.prf == prf_fit_width:
                p = p.scaledToWidth(int(0.96 * self.width()), Qt.SmoothTransformation)
            elif self.prf == prf_fit_height:
                p = p.scaledToHeight(int(0.96 * self.height()), Qt.SmoothTransformation)
            scn.setSceneRect(0, 0, p.width(), p.height())
            scn.addItem(QGraphicsPixmapItem(p))

        self.send(cnd='displayed')

    def keyPressEvent(self, e):
        k = e.key()
        if k == Qt.Key_PageUp:
            self.navigate(False)

        elif k == Qt.Key_PageDown:
            self.navigate()
        
        else:
            QGraphicsView.keyPressEvent(self, e)
    
    def resizeEvent(self, e):
        self.display()
        QGraphicsView.resizeEvent(self, e)

class pix_maker(thread):
    
    def __init__(self, par):
        super(pix_maker, self).__init__(par)

    def run(self):
        try:
            self.send(cnd='start')
            render(self.qa, self.k, self.book, self.dc, self.mm, self.td)
            self.send(cnd='end')

        except:
            self.send(cnd='error')

class wdg_fact(QWidget):
    
    msg_wdg_fact = pyqtSignal(dict)

    def __init__(self, par=None):
        QWidget.__init__(self, par)
        
        self.spl = spl = QSplitter(Qt.Horizontal, self)
        lo = QVBoxLayout()
        for i in ['vw_comp', 'vw_fact',]:
            setattr(self, i, pix_view(self))
            w = getattr(self, i)
            w.msg_pix_view.connect(self.handler_pix_view)
            spl.addWidget(w)
            if i == 'vw_comp':
                w.set_prf(prf_fit_height)
        lo.addWidget(spl)
        self.setLayout(lo)

    def send(self, **d):
        self.msg_wdg_fact.emit(d)
        
    def handler_pix_view(self, d):
        self.send(**d) 

    def n(self):
        return self.__class__.__name__

class win_fact(QMainWindow):

    def __init__(self, par, name, key, td):
        super(win_fact, self).__init__(par)
        self.setWindowTitle(u'Ebook Fact Dissected')
        
        attrs_from_dict(locals())

        self.stb = stb = QStatusBar(self)
        self.setStatusBar(stb)
        for ii, (i, l) in enumerate([('fact', 1),
                                     ('comp', 1), 
                                     ('aux',  2)]):
            n = f'lbl_{i}'
            setattr(self, n, QLabel(self))
            w = getattr(self, n)
            w.setAlignment(Qt.AlignCenter)
            w.setScaledContents(True)
            w.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
            stb.insertPermanentWidget(ii, w, l)
            
        stb.setSizeGripEnabled(False)

        for i, k in [('quit', ('Q', 'Esc')),]: 
            s = f'act_{i}'
            if not getattr(self, s, ''):
                setattr(self, s, QAction(self))
            a = getattr(self, s)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            a.triggered.connect(partial(self.handler, i))
            self.addAction(a)
        
        n = self.n()
        self.restoreState(sts.value(f'{n}/state', type=QByteArray))  
        self.td = tempfile.mkdtemp(prefix=n + '_', dir=td)
        self.w = w = wdg_fact(self)
        self.setCentralWidget(w)
        w.msg_wdg_fact.connect(self.refresh)
        w.spl.restoreState(sts.value(f'{n}/spl/state', type=QByteArray))

        self.overlay = overlay(self.centralWidget())

        name = self.name
        self.dd = dd = get_ana(name) 
        zo = dd['zo']
        z = dd['z']

        base_dpix = dd.get('dpix', 96)
        zz = 2. * z / zo * self.physicalDpiX() / base_dpix
        mm = QTransform(zz, 0, 0, zz, 0, 0)
        
        self.book = book = bk(name)
        dc = book.doc()
        dc.set_z(z)
        
        self.pix_maker = m = pix_maker(self)
        m.msg_thread.connect(self.make_pix)
        m.go(qa=dd['qa'], k=key, book=book, dc=dc, mm=mm, td=self.td)
         
    def handler(self, i):
        if i == 'quit':
            self.close()

        elif i == '':
            pass

    def refresh(self, d):
        o = self.overlay
        c = d['cnd']
        if c == 'start':
            o.show()
        else:
            o.hide()

        self.update_stb([('fact', ''), ('comp', ''),])

    def make_pix(self, d):
        c = d['cnd']
        if c == 'start':
            pass

        elif c == 'end':
            w = self.w
            k = self.key
            pd = pixd(self.dd, self.td)
            w.vw_fact.load_pix(sorted(pd['fact_by_k'][k]))
            w.vw_comp.load_pix(sorted(pd['comp_by_k'][k]))
            #w.vw_fact.load_pix(sorted(pd['fact_by_pg'][pg]))
            #w.vw_comp.load_pix([cat(self.td, f'{pg}_pg.png')])
            #w.vw_fact.load_pix(sorted(pd['comp_by_pg'][pg]))

        elif c == 'error':
            self.send(cnd='error')

    def closeEvent(self, e):
        self.cls()
        n = self.n()
        sts.setValue(f'{n}/spl/state', QVariant(self.w.spl.saveState()))
        sts.setValue(f'{n}/state', QVariant(self.saveState()))     

    def update_stb(self, tl):
        for sct, s in tl:
            self.msg({'msg': s}, sct)

    def msg(self, d, sct):
        lbl = getattr(self, f'lbl_{sct}')
        msg = d.get('msg', '')
        to = d.get('to', 0)
        lbl.setText(msg)
        
        if to:
            QTimer.singleShot(to, partial(lbl, setText, ''))
    
    def n(self):
        return self.__class__.__name__

    def cls(self):
        shutil.rmtree(self.td)

def group(name):
    cn = sqlite3.connect('/home/cytu/usr/src/py/ananda/db/ananda.db')
    cr = cn.cursor()

    def ks2ids(ks):
        ids = []
        all_id = cr.execute('select id from fact').fetchall()
        for i in all_id:
            ii = i[0]
            n, k = get_name_key(ii, cr)
            if n == name and k in ks:
                ids.append((ii, k))
        return ids 

    d = get_ana(name)

    def k_txt():
        dd = {}
        r = cr.execute('select id, data from fact').fetchall()
        for ii, data in r:
            n, k = get_name_key(ii, cr)
            if n == name and data.find('"txt"') > 0:
                dd[k] = json.loads(data)['qas']
        return dd 

    # scenarios: none/some of the facts are in db; prefab
    qa = d['qa']
    gp = d['groups']
    
    def mycmp(s):
        def mycmp_(s):
            q1 = qa['q'][s][0]
            return (q1[0], q1[1][1])

        # sort by page and y
        qaq = qa['q']
        if s not in qaq:
            for g in d['groups']:
                if g['key'] == s:
                    s = sorted(g['keys'], key=mycmp_)[0]
                    break 
        q1 = qa['q'][s][0]
        return (q1[0], q1[1][1])
    
    keys = sorted(list((set(qa['q'].keys()) & set(qa['a'].keys())) - set(d.get('del', []))  - set([k for g in d['groups'] for k in g['keys']]) | set([g['key'] for g in d['groups']])), key=mycmp)
    #print(keys) 
    #return

    for g in d['groups']:
        ks = [k for k in g['keys'] if k not in d['del']]
        if ks:
            insert_new_fact(fact_key(g, d, k_txt()), cr)
            # delete all (single) facts
            ids = [ii for ii, i in ks2ids(ks)]             
            for i in ids:
                cr.execute('delete from fact where id = ?', (i,))
                cr.execute('delete from rev where fact_id = ?', (i,))
    cn.commit()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    desktop = app.desktop()
    w_desktop = desktop.availableGeometry().width()
    dpix = desktop.physicalDpiX()
    
    screen = app.screens()[0]
    physical_dpi_x = screen.physicalDotsPerInchX()
    physical_dpi_y = screen.physicalDotsPerInchY()
    logical_dpi_x = screen.logicalDotsPerInchX()
    logical_dpi_y = screen.logicalDotsPerInchY()
    dpr = screen.devicePixelRatio()

    begin = time.perf_counter() 
    print(f'begin:   {now(utc=False)}')

    #group('ash_real')
    
    #wipe_all('kirsch', [str(i) for i in range(1, 15)])
    
    for i in ['aliprantis',]: # ['grimmett_sol', 'baldi1', 'knapp_basic_real']:
        folder = cat('/home/cytu/thm', i)
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        render_all(i, folder, b_remove_prob_ans_png=True)#, b_render_q_no_a=True)
       #render_all(i, folder, b_fact_qa_only=True, b_rename_fact_qa_png=True, b_remove_prob_ans_png=False, b_render_q_no_a=False)

    ## detect which problems are not in the list; designed only for tkachuk books
    #d = get_ana('tkachuk_3')
    #print sorted(list(set([f'U.{i:03d}' for i in range(1,500)]) - set(d['qa']['q'].keys())))
    
    ## code to detect qa generating problem
    #d = get_ana('baldi1')
    #update_qa(d)
    
    #for name in ['evans',]:
    #    d = parse(name)
    #    save_ana(d)

    print(f'end:     {now(utc=False)}')
    print(f'elapsed: {nr2t(int(time.perf_counter() - begin))}')
