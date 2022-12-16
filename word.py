from base import *
from img import *

de = 'de_grundwortschatz'

from ed import qas2db, db2qas 
from db.make_db import make_db

def get_words():
    root = '/home/cytu/usr/src/py/ananda/tmp/words'
    shutil.rmtree(root)
    os.mkdir(root)

    # words per file
    NVI, NNI, NI = 1000, 3000, 2000 
    tl, vl, nl = [], [], []
    i, ii, vi, vii, ni, nii = [1] * 6
    ana = get_ana(de)

    vk, nk, ok = [], [], []
    for k in sorted(ana['qa'].keys(), key=lambda i:int(i)):
        fact = json.loads(fact_key(k, ana)) 
        qa = fact['qas'][0]
        tq = qa['q'][0]['txt']
        ta = qa['a'][0]['txt'].replace('<br /><br />', '\n')
        #tl.append(u'{0:<55}'.format(ta) + tq)
        
        atoms = [s.strip() for s in tq.split(' ')]
        if 'v' in atoms or 'vm' in atoms:
            vl.append('\n'.join([str(vi if vi else NVI), tq, ta]))
            if vi == 0:
                codecs.open(cat(root, 'verbs_%s.txt' % str(vii).zfill(2)), 'w', 'utf-8').write('\n\n'.join(vl))
                vii += 1
                vl = []
            vi += 1
            vi %= NVI
            vk.append(k)

        elif 'n' in atoms:
            nl.append('\n'.join([str(ni if ni else NNI), tq, ta]))
            if ni == 0:
                codecs.open(cat(root, 'nouns_%s.txt' % str(nii).zfill(2)), 'w', 'utf-8').write('\n\n'.join(nl))
                nii += 1
                nl = []
            ni += 1
            ni %= NNI 
            nk.append(k)

        else:
            tl.append('\n'.join([str(i if i else NI), tq, ta]))
            if i == 0:
                codecs.open(cat(root, 'others_%s.txt' % str(ii).zfill(2)), 'w', 'utf-8').write('\n\n'.join(tl))
                ii += 1
                tl = []
            i += 1
            i %= NI 
            ok.append(k)
            
    if vl:    
        codecs.open(cat(root, 'verbs_%s.txt' % str(vii).zfill(2)), 'w', 'utf-8').write('\n\n'.join(vl))
    if nl:
        codecs.open(cat(root, 'nouns_%s.txt' % str(nii).zfill(2)), 'w', 'utf-8').write('\n\n'.join(nl))
    if tl:
        codecs.open(cat(root, 'others_%s.txt' % str(ii).zfill(2)), 'w', 'utf-8').write('\n\n'.join(tl))
    
    new = False 
    wdb = cat('db', 'word.db')
    if new:
        try:
            os.remove(wdb)
        except:
            pass
    if not os.path.isfile(wdb):
        make_db(sqlite3.connect(wdb))

    cn = sqlite3.connect(wdb)
    cr = cn.cursor()
    cr.execute('insert into prefab(name, keys) values(?, ?)', ('de_grundwortschatz_pre', json.dumps(vk + nk + ok)))
    cn.commit()

#get_words()
#sys.exit()

def get_loci(lid):
    cn = sqlite3.connect(cat('db', 'loci.db'))
    cr = cn.cursor()
    ids = json.loads(cr.execute('select data from route where id = ?', (lid,)).fetchone()[0])['loci']
    pxs = []
    for i in ids:
        pxs.append(cr.execute('select pix from loci where id = ?', (i,)).fetchone()[0])
    return pxs

class it_p(QGraphicsPixmapItem):

    def __init__(self, o, rct):
        super(it_p, self).__init__()
        self.rct = rct
        self.setPos(o)
    
    def boundingRect(self):
        return self.rct.adjusted(-1, -1, 1, 1)

class it_t(QGraphicsTextItem):

    def __init__(self, o, rct):
        super(it_t, self).__init__()
        self.rct = rct
        self.setPos(o)
        self.setFont(QFont('Microsoft JhengHei', 30))
    
    def boundingRect(self):
        return self.rct.adjusted(-1, -1, 1, 1)

class wdg_w(wdg_i):
    
    def __init__(self, par):
        super(wdg_w, self).__init__(par)

        self.av = av = wdg_a(self)
        av.hide()
        av.msg_av.connect(self.handler_av)
        
        new = True
        wdb = cat('db', 'word.db')
        if new:
            try:
                os.remove(wdb)
            except:
                pass
        if not os.path.isfile(wdb):
            make_db(sqlite3.connect(wdb))
        self.cn = cn = sqlite3.connect(wdb)
        cr = cn.cursor()
        cn.commit()

        self.reset()

    def create_it(self):
        scn = self.scn
        gv = self.gv
        w, h = gv.width(), gv.height()
        scn.setSceneRect(0, 0, 0.97 * w, 0.99 * h)
        
        self.it_r = it_p(QPointF(40, 10), QRectF(0, 0, 450, 270))
        scn.addItem(self.it_r)
        self.it_l = it_p(QPointF(530, 10), QRectF(0, 0, 450, 270))
        scn.addItem(self.it_l)
        self.it_qp = it_p(QPointF(40, 367), QRectF(0, 0, 450, 270))
        scn.addItem(self.it_qp)
        self.it_ap = it_p(QPointF(530, 367), QRectF(0, 0, 450, 270))
        scn.addItem(self.it_ap)

        self.it_q = it_t(QPointF(40, 290), QRectF(0, 0, 450, 67))
        scn.addItem(self.it_q)
        self.it_a = it_t(QPointF(530, 290), QRectF(0, 0, 450, 67))
        scn.addItem(self.it_a)
       
    def reset(self, qas=None):
        self.fact_id, self.side, self.slide = [0] * 3
        self.qas = [{}.fromkeys(['q_audio', 'a_audio', 'q_text', 'a_text', 'q_pix', 'a_pix'], '')] if qas is None else qas

    def display(self):
        qa = self.qas[0]
        self.show_txt(qa['q_text'], 'q')
        self.show_txt(qa['a_text'], 'a')
        self.show_pix(qa['q_pix'], 'it_q')
        self.show_pix(qa['a_pix'], 'it_a')
        
    def show_txt(self, txt, role):
        i = getattr(self, 'it_%s' % role)
        i.setHtml(txt)

    def show_pix(self, pix, role):
        if not pix:
            i.setPixmap(QPixmap())
            return

        if isinstance(pix, QPixmap):
            p = pix
        else:
            f = cat(self.td, 'display.png')
            open(f, 'wb').write(pix)
            p = QPixmap(f)

        if p.width():
            i = getattr(self, role)
            r = i.boundingRect()
            w, h = r.width(), r.height() 
            if p.height() >= h:
                p = p.scaledToHeight(h, Qt.SmoothTransformation)
            if p.width() >= w:
                p = p.scaledToWidth(w, Qt.SmoothTransformation)
            i.setPixmap(p)
    
    def handler_av(self, d):
        c = d['cnd']
        if c == 'rec_start':
            self.send(cnd='rec_start')

        elif c == 'rec_stop':
            self.send(cnd='rec_stop')
            self.qas[self.slide]['%s_audio' % ('a' if self.side == 1 else 'q')] = d['f']
            # automatically switch side.
            #self.flip()
    
    def flip(self, side=None):
        self.side = side if side is not None else (0 if self.side == 1 else 1)
        self.send(cnd='update_stb') 
    
    def rec(self):
        self.av.rec()

    def handler(self, d):
        c = d['cnd']
        if c == 'page_changed':
            self.update_tb()
        
        elif c == 'show_lw':
            l = d['url']
            self.lw.clear()
            d = self.mgr.src()[l]
            for ii, i in enumerate(d):
                fn = i['thn']['fn']
                if fn is None:
                    fn = ':/res/img/google.png'
                    self.mgr.download({'td': self.td, 
                                       'key': l, 
                                       'it': ii, 
                                       'typ': 'thn', 
                                       'url': i['thn']['url'], 
                                       'ref': ''})
                li = QListWidgetItem(i['dsc'])
                li.setData(Qt.UserRole, QVariant(json.dumps({'key': l, 'it': ii})))
                li.setData(Qt.UserRole + 1, QVariant(fn))
                self.lw.addItem(li)
        
        elif c == 'update_gv':
            fn = d['fn']
            self.fn = fn
            p = QPixmap(fn)
            ow, oh = p.width(), p.height()
            if not ow or not oh:
                self.send(cnd='msg', sct='pix', to=20000, msg='<font color="red">error: selected pix is null</font>')
                return
            self.show_pix(p, 'it_r') 
            pw, ph = p.width(), p.height()
            self.send(cnd='msg', msg='<font color="blue">original pix size: %s x %s (%s%%) </font>' % (ow, oh, int(100. * (pw * ph) / (ow * oh))), sct='pix')
            
        elif c == 'update_lw':
            t = d['t']
            if t['key'] == self.mgr.ks()[self.pg()]:
                self.lw.item(t['it']).setData(Qt.UserRole + 1, QVariant(t['fn']))
        
        elif c == 'update_q':
            self.led.setText(d['q'])
        
        elif c == 'msg':
            self.send(**d) 
    
    def add(self):
        pass

    def save(self):
        fact_id = self.fact_id
        cn = self.cn
        save_fact(qas2db(self.qas, cn.cursor(), fact_id), cn, fact_id=fact_id)
        self.reset()
        self.send(cnd='saved')
        self.play_audio('res/av/saved.mp3')
    
    def play_audio(self, src):
        a = self.av
        a.set_src(src)
        a.play()

    def timerEvent(self, e):
        pass
    
class win_word(QMainWindow):
    l_stw = ['stw', 'stw1'] 

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(u'Word Power')
        self.setWindowIcon(QIcon('./res/img/tools_check_spelling.png'))
        self.td = tempfile.mkdtemp(prefix='%s_%s_' % (self.n(), now().replace(':', '')), dir=cat(os.getcwd(), tmp))
        self.w = wdg_w(self)
        self.setCentralWidget(self.w)
        getattr(self.w, 'msg_%s' % self.w.n()).connect(self.handler_w)    

        for i, k in [('focus_led', ('Ctrl+K',)),
                     ('save',      ('F2',)), 
                     ('add',       ('F3',)),
                     ('rec',       ('F4',)),
                     ('flip',      ('Ctrl+M',)),
                     ('next',      ('PgDown',)),
                     ('prev',      ('PgUp',)),
                    ]:
            s = 'act_%s' % i
            setattr(self, s, QAction(self))
            a = getattr(self, s)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            a.triggered.connect(partial(self.handler, i))
            self.addAction(a)
        
        stb = QStatusBar(self)
        self.setStatusBar(stb)
        for ii, (i, l, tlt) in enumerate([
            ('rec',  1, 'recording status'),
            ('side', 1, 'side'),
            ('gen',  12, 'generic message'),
            ('stw',  2, 'time spent on this query | session'),
            ('pix',  10, 'info of picture'),
            ('aux',  4, 'session status'),
        ]):
            n = 'lbl_%s' % i
            setattr(self, n, QLabel(self))
            w = getattr(self, n)
            w.setAlignment(Qt.AlignCenter)
            w.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
            w.setToolTip(tlt)
            stb.insertPermanentWidget(ii, w, l)
        stb.setSizeGripEnabled(False)

        n = self.n()
        self.w.spl.restoreState(sts.value('%s/spl/state' % n, type=QByteArray))
        self.restoreState(sts.value('%s/state' % n, type=QByteArray))        
        self.resize(sts.value('%s/size' % n, type=QSize))

        for i in self.l_stw:
            setattr(self, i, stopwatch(self))

        self.startTimer(1000)
        self.w.focus_led()
        
        self.update_stb()

    def msg(self, d):
        lbl = getattr(self, 'lbl_%s' % d.get('sct', 'info'))
        msg = d.get('msg', '')
        to = d.get('to', 0)
        lbl.setText(msg)
        
        if to:
            QTimer.singleShot(to, partial(lbl.setText, ''))
    
    def handler_w(self, d):
        c = d['cnd']
        if c == 'msg':
            self.msg(d)

        elif c == 'reset':
            self.stw.reset()
        
        elif c == 'rec_start':
            self.lbl_rec.setPixmap(QPixmap(':/res/img/audio_headset.png'))
        
        elif c == 'rec_stop':
            self.lbl_rec.setPixmap(QPixmap())

        elif c == 'update_stb':
            self.update_stb()

    def update_stb(self):
        s = 'a' if self.w.side else 'q'
        self.lbl_side.setText('<font color="blue">%s</font>' % s.upper())

    def timerEvent(self, e):
        self.msg({'sct': 'stw', 'msg': '<font color="purple">%s</font>' % nr2t(self.stw.cnt / 10)})
            
    def handler(self, i):
        w = self.w
        getattr(w, i)()

    def n(self):
        return self.__class__.__name__

    def closeEvent(self, e):
        n = self.n()
        sts.setValue('%s/size' % n, QVariant(self.size()))
        sts.setValue('%s/state' % n, QVariant(self.saveState()))        
        sts.setValue('%s/spl/state' % n, QVariant(self.w.spl.saveState()))
        shutil.rmtree(self.td)

    def event(self, e):
        try:
            typ = e.type()
            if typ == QEvent.WindowActivate:
                for s in self.l_stw:
                    getattr(self, s).start() 
            
            elif typ == QEvent.WindowDeactivate:
                for s in self.l_stw:
                    getattr(self, s).stop() 
        finally:
            return QMainWindow.event(self, e) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('word')
    app.setFont(QFont('Microsoft JhengHei'))
    w = win_word()
    w.show()
    w.w.create_it()
    app.exec_()
