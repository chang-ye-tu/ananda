from base import *
from urllib import quote
from bs4 import BeautifulSoup

b_debug = 1

def make_db(cn):
    cr = cn.cursor()

    def create_ix(t, i):
        cr.execute('create index ix_%s_%s on %s(%s)' % (t, i, t, i))

    for t in ['img']:
        cr.execute('''create table %s (id integer primary key, 
                                       data blob not null,
                                       sha text not null,
                                       qry text not null,
                                       ext text not null default "",
                            created text not null default current_timestamp,
                                       unique (sha))''' % t)
        for i in ['sha', 'qry', 'ext', 'created']:
            create_ix(t, i)

    cn.commit()

db = cat('db', 'img.db')
if not os.path.isfile(db):
    make_db(sqlite3.connect(db))
cn = sqlite3.connect(db)

def n_fact(interval=None):
    try:
        cr = cn.cursor()
        count = 'select count(*) from img'
        sql = (count,) if interval is None else \
              (' '.join([count, 'where created between ? and ?']), interval)
        
        return cr.execute(*sql).fetchone()[0]
    
    except:
        return 0

def start_n(l):
    try:
        return int(re.compile(r'&start=(\d+)').search(l).groups()[0])
    except:
        return -1 

class dl_(QNetworkAccessManager):

    completed = pyqtSignal('PyQt_PyObject')
    error = pyqtSignal('PyQt_PyObject')

    def __init__(self, par):
	super(dl_, self).__init__(par)
        self.finished.connect(self.completed)
        self.task = {}

    # task = dict(url='', ref='', td='', key='', it=0, typ='thn', fn=None)  
    def fetch(self, t):
        self.task[t['url']] = t
        q = QNetworkRequest()
        q.setUrl(QUrl.fromEncoded(t['url'].encode('utf-8')))
        q.setRawHeader('User-Agent', 
                       'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
        if t['ref']:
            q.setRawHeader('Referer', t['ref'])
        self.get(q)
    
    def completed(self, r):
        pass
        
class dl(dl_):
    
    def __init__(self, par):
	super(dl, self).__init__(par)

    def completed(self, r):
        t = self.task[str(r.url().toEncoded())]
        if r.error() == QNetworkReply.NoError:
            b = str(r.readAll())
            sha = hashlib.sha224(b).hexdigest()
            fn = cat(t['td'], sha)
            open(fn, 'wb').write(b)
            t['fn'] = fn
            t['sha'] = sha
            s, rr = 'completed', t
        else:
            s, rr = 'error', r.errorString()
        getattr(self, s).emit(rr)

class dlp(dl_):
    
    def __init__(self, par):
	super(dlp, self).__init__(par)

    def completed(self, r):
        if r.error() == QNetworkReply.NoError:
            b = str(r.readAll())
            #open('debug.htm', 'wb').write(b)
            s, rr = 'completed', (str(r.url().toEncoded()), b)
        else:
            s, rr = 'error', r.errorString() 
        getattr(self, s).emit(rr)

class delg(QStyledItemDelegate):

    def __init__(self, par=None):
        super(delg, self).__init__(par)
    
    def paint(self, p, opt, ix):
        txt = ix.model().data(ix).toString()
        doc = QTextDocument()
        doc.setDefaultFont(opt.font)
        doc.setHtml(txt)
        f = ix.model().data(ix, Qt.UserRole + 1).toString()
        i = QImage(f)
        rct = opt.rect
        size = i.size()
        p.save()
        # set background color
        p.setPen(QPen(Qt.NoPen))
        if opt.state & QStyle.State_Selected:
            p.setBrush(QBrush(Qt.lightGray))
        else:
            p.setBrush(QBrush(Qt.white))
        p.drawRect(rct)
        p.drawImage(rct.x(), rct.y(), i)
        p.translate(rct.x() + size.width(), 
                rct.y() + int(1./2 * (size.height() - opt.fontMetrics.height())))
        doc.drawContents(p)
        p.restore()

    def sizeHint(self, opt, ix):
        f = ix.model().data(ix, Qt.UserRole + 1).toString()
        i = QImage(f)
        size = i.size()
        txt = ix.model().data(ix).toString()
        doc = QTextDocument()
        doc.setDefaultFont(opt.font)
        doc.setHtml(txt)
        return QSize(doc.idealWidth() + size.width() + 5, size.height() + 10)

class mgr(QObject):
    
    msg_mgr = pyqtSignal(dict)

    def __init__(self, par=None, q=''):
        QObject.__init__(self, par)
        
        self.root = 'http://images.google.com'
        
        for i in ['dlp', 'dl']:
            setattr(self, i, globals()[i](self))
            w = getattr(self, i)
            w.completed.connect(getattr(self, '%s_completed' % i))
            w.error.connect(getattr(self, '%s_error' % i))

        self.set_q(q)
    
    def send(self, **d):
        self.msg_mgr.emit(d)

    def n(self):
        return self.__class__.__name__
    
    def set_q(self, q=''):
        self.d = {}
        self.pgs = 0
        self.pg = -1 
         
        if q and getattr(self, 'q', '') != q:
            self.q = q
            url = self.url_n(self.q, 0)            
            self.get_page({'url': url, 'ref': ''})
    
    # normalized url
    def url_n(self, q, start):
        return self.root + '/search?q=%s&hl=en&gbv=2&tbs=isch:1&start=%s&sa=N&tbm=isch' % ('+'.join([quote(i.encode('utf-8')) for i in q.split()]), start) 

    def get_page(self, t):
        self.dlp.fetch(t)

    def download(self, t):
        self.dl.fetch(t)
   
    def dl_error(self, r):
        self.send(cnd='msg', msg='<font color="red">pix download error: %s</font>' % ellipsis(r, typ='middle'), sct='pix', to=20000)

    def dlp_error(self, r):
        self.send(cnd='msg', msg='<font color="red">load page error: %s</font>' % ellipsis(r, typ='middle'), sct='gen', to=20000)

    def dl_completed(self, t):
        self.d[t['key']][t['it']][t['typ']]['fn'] = t['fn']
        if t['typ'] == 'img':
            self.send(cnd='update_gv', fn=t['fn'])
        elif t['typ'] == 'thn':
            self.send(cnd='update_lw', t=t) 

    def dlp_completed(self, tp):
        url, b = tp
        src = BeautifulSoup(b)
        
        if not src or src.find_all(text=re.compile('did not match any documents')):
            self.d[url] = []
            return

        if b_debug:
            open(cat('tmp', 'src_debug.html'), 'w').write(b)
        
        # XXX 01/18/16
        # get number of result pages
        br = src.find_all('br', clear='all')[-1]
        cnt = br.find_next('br').find_previous('table')
        for a in cnt.find_all('a'):
            n = start_n(a['href'])
            if n == -1:
                print('error now') 

            else:
                u = self.url_n(self.q, n)
                if u not in self.d:
                    self.d[u] = None
        
        # Get all pic items within the page
        dsc, thn, img = [], [], []
        tds = src.find_all('td', style='line-height:17px;padding-bottom:16px;width:25%;                    word-wrap:break-word')
        for td in tds:
            f = td.find('font', size='-1')
            # get description.
            # f.contents[-4:] looks like
            # ['<br />', '328 x 483 - 47k&nbsp;-&nbsp;jpg', '<br />', '<font color="green">yiyuanyi.org</font>']
            # rendered as:
            #
            #   328 x 483 - 47k - jpg
            #   yiyuanyi.org
            contents = f.contents[:-4]
            dsc.append(''.join([i for i in contents]))

            a = td.find('a')
            h = a['href']
            img_url = 'http://www.google.com' + h
            open(cat('tmp', 'test.txt'), 'a').write(img_url + '\n')
            thn_url = a.find('img')['src']
            thn.append(thn_url)  
            img.append(img_url)
        
        self.d[url] = [{'dsc': i, 
            'thn': {'url': thn[ii], 'ref': '', 'visit': 0, 'fn': None}, 
            'img': {'url': img[ii], 'ref': '', 'visit': 0, 'fn': None}} for ii, i in enumerate(dsc)]
       
        self.pgs = len(self.d)        
        self.set_pg(self.ks().index(url))
        self.send(cnd='show_lw', url=url)
        self.send(cnd='page_changed')

    def src(self):
        return self.d    
    
    def ks(self):
        return sorted(self.d.keys(), key=start_n)

    def set_pg(self, n):        
        if self.pg != n and 0 <= n < self.pgs: 
            self.pg = n 
            l = self.ks()[self.pg]
            if self.d[l] is None:
                self.get_page({'url': l, 'ref': ''})
            else:
                self.send(cnd='show_lw', url=l)
            self.send(cnd='page_changed')
    
    def fst(self):
        self.set_pg(0)

    def last(self):        
        self.set_pg(self.pgs - 1)
    
    def next(self):
        self.set_pg(self.pg + 1)

    def prev(self):
        self.set_pg(self.pg - 1)
    
class wdg_i(QWidget):
    
    msg_wdg_i = pyqtSignal(dict)

    def __init__(self, par):
        super(wdg_i, self).__init__(par)
        self.td = par.td 

        hlo1 = QHBoxLayout(self)
        self.spl = spl = QSplitter(self)
        spl.setOrientation(Qt.Horizontal)
        w = QWidget(spl)
        vlo = QVBoxLayout(w)
        vlo.setMargin(0)
        hlo = QHBoxLayout()
        self.led = QLineEdit(w)
        hlo.addWidget(self.led)
        self.spb = QSpinBox(w)
        hlo.addWidget(self.spb)
        self.lbl = QLabel(w)
        hlo.addWidget(self.lbl)
        vlo.addLayout(hlo)
        self.lw = QListWidget(w)
        vlo.addWidget(self.lw)
        self.gv = QGraphicsView(spl)
        hlo1.addWidget(spl)
        self.scn = QGraphicsScene(self)
        self.gv.setScene(self.scn)
        
        self.mgr = m = mgr()
        m.msg_mgr.connect(self.handler)
        self.led.returnPressed.connect(self.set_q)
        
        lw = self.lw
        lw.setEditTriggers(QAbstractItemView.NoEditTriggers)
        lw.setSelectionMode(QAbstractItemView.ExtendedSelection)
        lw.setItemDelegate(delg(self))
        lw.itemClicked.connect(self.show_i)
        lw.itemActivated.connect(self.show_i) 

        self.set_q()
        self.fn = ''

        self.spb.editingFinished.connect(self.spb_changed)
        
    def send(self, **d):
        self.msg_wdg_i.emit(d)

    def n(self):
        return self.__class__.__name__

    def spb_changed(self):
        spb = self.sender()
        if spb is self.spb:
            self.set_pg(spb.value() - 1) 

    def set_q(self, q=''):
        if q:
            self.led.setText(q)
        self.mgr.set_q(self.led.text())
        self.send(cnd='reset')
        self.lw.setFocus()

    def show_i(self, it):
        dd = json.loads(it.data(Qt.UserRole).toString())
        try:
            d = self.mgr.src()[dd['key']][dd['it']]
        except:
            self.send(cnd='msg', sct='pix', to=20000,
                msg='<font color="red">error: unable to load pix ...</font>')
            return

        fn = d['img']['fn']
        if fn is None:
            t = {'td': self.td, 
                 'key': dd['key'], 
                 'it': dd['it'], 
                 'typ': 'img', 
                 'url': d['img']['url'], 
                 'ref': d['img']['ref']}
            self.mgr.download(t)
            self.send(cnd='msg', sct='pix', msg='<font color="green">loading pix ...</font>')
        else:
            self.handler({'cnd': 'update_gv', 'fn': fn})
    
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
            scn = self.scn
            scn.clear()
            ow, oh = p.width(), p.height()
            if not ow or not oh:
                self.send(cnd='msg', sct='pix', to=20000,
                    msg='<font color="red">error: selected pix is null</font>')
                return

            gv = self.gv
            w, h = gv.width() * 0.98, gv.height() * 0.98
            if p.height() >= h:
                p = p.scaledToHeight(h, Qt.SmoothTransformation)
            if p.width() >= w:
                p = p.scaledToWidth(w, Qt.SmoothTransformation)
            pw, ph = p.width(), p.height()
            scn.setSceneRect(0, 0, pw, ph)
            scn.addItem(QGraphicsPixmapItem(p))
            self.send(cnd='msg', msg='<font color="blue">original pix size: %s x %s (%s%%) </font>' % (ow, oh, int(100. * (pw * ph) / (ow * oh))), sct='pix')
            
        elif c == 'update_lw':
            t = d['t']
            if t['key'] == self.mgr.ks()[self.pg()]:
                self.lw.item(t['it']).setData(Qt.UserRole + 1, QVariant(t['fn']))
        
        elif c == 'update_q':
            self.led.setText(d['q'])
        
        elif c == 'msg':
            self.send(**d) 

    def update_tb(self):
        self.lbl.setText('/ %s' % self.pgs())
        spb = self.spb
        spb.setValue(self.pg() + 1)
        spb.setRange(1, self.pgs())

    def fst(self):
        self.mgr.fst()
        
    def last(self):
        self.mgr.last()

    def next(self):
        self.mgr.next()

    def prev(self):
        self.mgr.prev()

    def set_pg(self, n):
        self.mgr.set_pg(n)

    def save(self):
        if not os.path.isfile(self.fn):
            self.send(cnd='msg', msg='<font color="red">error: selected pix does not exist ...</font>', to=20000, sct='gen')
            return

        p = QPixmap(self.fn)
        if not p.width() or not p.height():
            self.send(cnd='msg', msg='<font color="red">error: selected pix is null ...</font>', to=20000, sct='gen')
            return
        
        self.send(cnd='save', q=self.q(), fn=self.fn)

    def focus_led(self):
        self.led.selectAll()
        self.led.setFocus()

    def pgs(self):
        return self.mgr.pgs

    def pg(self):
        return self.mgr.pg 

    def q(self):
        return self.mgr.q
    
class win_i(QMainWindow):
    l_stw = ['stw', 'stw1'] 
    
    msg_win_i = pyqtSignal(dict)

    def __init__(self, par=None):

        QMainWindow.__init__(self, par)
        self.setWindowTitle('Image Cue')
        self.setWindowIcon(QIcon(':/res/img/img.png'))
        self.par = par

        self.td = tempfile.mkdtemp(prefix='%s_%s_' % (self.n(), now().replace(':', '')), dir=cat(os.getcwd(), tmp))
        self.w = wdg_i(self)
        self.setCentralWidget(self.w)
        self.w.msg_wdg_i.connect(self.handler_w)    

        for i, k in [('focus_led', ('Ctrl+K',)),
                     ('save',      ('F2',)), 
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
            ('gen', 6, 'generic message'),
            ('stw', 2, 'time spent on this query | session'),
            ('num', 1, '# of stored query/image pairs: today | all'),
            ('pix', 6, 'info of picture'),
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

        self.msg({'msg': '<font color="blue">%s</font>&nbsp;&nbsp;&nbsp;<font color="green">%s</font>' % (n_fact((today(), tomorrow())), n_fact()), 'sct': 'num'})

        for i in self.l_stw:
            setattr(self, i, stopwatch(self))

        self.startTimer(1000)
        self.w.focus_led()

    def send(self, **d):
        self.msg_win_i.emit(d)
    
    def n(self):
        return self.__class__.__name__

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
        
        elif c == 'save':
            q, fn = d['q'], d['fn']
            ext, ok = QInputDialog.getText(self, 'Extension ...', 
                        'Original Query is:  %s\n\nEnter Your Extension:' % q)
            if not ok:
                return

            if self.par:
                self.send(cnd='save', q=q, fn=fn, ext=ext)
                self.close()
                return

            b = open(fn, 'rb').read()
            sha = hashlib.sha224(b).hexdigest()
            try:
                cn.cursor().execute('''insert into img (data, sha, qry, ext) 
                                       values (?, ?, ?, ?)''', 
                                    (sqlite3.Binary(b), sha, q, ext))
                cn.commit()

            except:
                cn.rollback()
                self.msg({'msg': '<font color="red">error saving query [ %s ] & pix: mostly redundant</font>' % q, 'to': 10000, 'sct': 'gen'})
                return

            self.msg({'msg': '<font color="blue">%s</font>&nbsp;&nbsp;&nbsp;<font color="green">%s</font>' % (n_fact((today(), tomorrow())), n_fact()), 'sct': 'num'})

            self.msg({'msg': '<font color="blue">save query [ %s ] & pix successfully !</font>' % q, 'to': 10000, 'sct': 'gen'})

    def timerEvent(self, e):
        self.msg({'sct': 'stw', 'msg': '<font color="purple">%s</font>&nbsp;&nbsp;<font color="blue">%s</font>' % tuple([nr2t(getattr(self, s).cnt / 10) for s in self.l_stw])})
            
    def handler(self, i):
        w = self.w
        getattr(w, i)()

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
    app.setApplicationName('img')
    app.setFont(QFont('Microsoft JhengHei'))
    w = win_i()
    w.show()
    app.exec_()
