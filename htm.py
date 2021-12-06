from base import *
from bs4 import BeautifulSoup, Tag

fs = []
repo = '/home/cytu/usr/doc/lang/txt/Collins-English-Grammar/'
for root, dirs, files in os.walk(cat(repo, 'html')):
    for f in files:
        if fnmatch(f, '*.html'):
            fs.append(cat(root, f))
def mycmp(f):
    return [int(s) for s in f_no_ext(f).split('.')]
fs = sorted(fs, key=mycmp)

def htm(s, b_centered=False):
    return r'''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 
    'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<meta http-equiv='X-UA-Compatible' content='IE=EmulateIE7' >
<head>
<link rel='stylesheet' type='text/css' href='css.css' media='screen, projection'/>
<link rel='stylesheet' type='text/css' href='css.css' media='screen, projection'/>
</head>
<body>
%s
</body>
</html>
''' %  ('''<div id='outer'><div id='middle'><div id='inner'>
%s
</div></div></div>''' % s if b_centered else s)

def beautify(f):
    r = BeautifulSoup(codecs.open(cat(repo, 'html_orig', f), 'r', 'utf-8').read())
    
    # kill all link, div with id = 'collins...'
    links = r.findAll('link')
    [l.extract() for l in links]
    h3s = r.findAll('h3')
    [h.extract() for ii, h in enumerate(h3s) if ii == 1]
    divs = r.findAll('div', id=re.compile(r'^collins'))
    [div.extract() for div in divs]
    
    # find digit elements
    digits = r.findAll(text=re.compile('^\d+\.\d+$'))
    for dg in digits:
        # should be links, not only bold
        if dg.previous.name != 'a':
            tg1 = Tag(r, 'b')
            tg = Tag(r, 'a', [('href', '%s.html' % unicode(dg)),])
            tg.insert(0, unicode(dg))
            tg1.insert(0, tg)
            dg.previous.replaceWith(tg1)
   
    # fix <b><a href="...">...</a> to <a href="...">...</a></b> to
    #     <b><a href="...">...</a></b> to <b><a href="...">...</a></b>
    num = 0
    ps = r.findAll('p')
    for p in ps:
        bs = p.findAll('b')
        for b in bs:
            ct = b.contents
            if u' to ' in ct and len(ct) == 3:
                num += 1
                # XXX hack!
                b.contents[1].replaceWith('</b> to <b>')
    #if num:
    #    print(f)

    # some <pre><i> are wrongly rendered as <blockquote><i>
    blqs = r.findAll('blockquote')
    for bl in blqs:
        b = False
        for ct in bl.contents:
            if not isinstance(ct, unicode):
                #print(f, ct)
                b = True
                break
        if b:
            tg = Tag(r, 'pre')
            tg.insert(0, ct)
            bl.replaceWith(tg)

    # <tt>n</tt>,'n', .n', ?n' in sentences. eg. 4.16.html 
    # replace with em dash
    pres = r.findAll('pre')
    b = 0
    for pre in pres:
        tts = pre.contents[0].findAll('tt')
        if tts:
            for tt in tts:
                tt.replaceWith(u'\u2014')
            b += 1
        ns = pre.contents[0].findAll(text=re.compile(r"'n'|(\.n')|(\?n')"))
        if ns:
            for nn in ns:
                nn.replaceWith(nn.replace("'n'", u"'\u2014'").replace(".n'", u".\u2014'").replace("?n'", u"?'\u2014'"))
            b += 1
    #if b:
    #    print(f)

    # fix examples: <p>&nbsp;&nbsp; &nbsp;<i>......</i></p> should be
    #               <pre><i>....</i></pre>

    codecs.open(cat(repo, 'html', f), 'w', 'utf-8').write(htm((unicode(r).strip(),)))

def contents(k):
    r = BeautifulSoup(codecs.open(cat(repo, 'html', '%s.html' % k), 'r', 'utf-8').read())
    return {'ex': [pre.text for pre in r.findAll('pre')],
            'list': [q.text for q in r.findAll('blockquote')]}

def beautify_all():
    for root, dirs, files in os.walk(cat(repo, 'html_orig')):
        for f in files:
            if fnmatch(f, '*.html'):
                beautify(f)

class win_htm(QMainWindow):

    l_stw = ['stw', 'stw1']
    msg_win_htm = pyqtSignal(dict)
    
    def __init__(self):

        QMainWindow.__init__(self)
        self.setWindowTitle('HTML Reader')
        self.setWindowIcon(QIcon('./res/img/internet_web_browser.png'))

        self.b = b = browser(self)
        b.urlChanged.connect(self.url_changed)
        self.setCentralWidget(b)
        b.setFocusPolicy(Qt.NoFocus)

        self.idx = 0 
        self.set_content()

        for i, k in [('back',    (QKeySequence.Back,)),
                     ('forward', (QKeySequence.Forward,)),
                     #('pg_up',   ('PgUp', 'Up')),
                     #('pg_dn',   ('PgDown', 'Down')),
                     ('delete',  ('Ctrl+Del',)), 
                     ('defer',   ('Ctrl+D',)),
                     ('full',    ('F11',)),
                     ('reset',   ('U',)),
                     ('refresh', ('F5',)),
                     ('edit',    ('E',)),
                    ]:

            s = 'act_%s' % i
            setattr(self, s, QAction(self))
            a = getattr(self, s)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            
            #if i in ('pg_dn', 'pg_up'):
            #    f = partial(b.page().scroll, 0, (1 if i == 'pg_dn' else -1) * 50)
            #else:
            #    f = partial(self.handler, {'cnd': i})
            f = partial(self.handler, {'cnd': i})
            a.triggered.connect(f)
            
            self.addAction(a)
        
        # setup stb
        self.stb = stb = QStatusBar(self)
        self.setStatusBar(stb)
        
        lstb = [('info',   3,  u'htm info'),
                ('stw',    1,  u'active time of this htm'),
                ('n_span', 1,  u'logged active time: today'),
                ('aux',    1,  u'session status'),
                ]

        for ii, (i, l, tlt) in enumerate(lstb):
            n = 'lbl_%s' % i
            setattr(self, n, QLabel(self))
            w = getattr(self, n)
            w.setToolTip(tlt)
            w.setAlignment(Qt.AlignCenter)
            w.setScaledContents(True)
            w.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
            stb.insertPermanentWidget(ii, w, l)
        stb.setSizeGripEnabled(False)

        self.tmr = t = QTimer(self)
        t.timeout.connect(self.handler_tmr)
        t.start(1000)
        
        for i in self.l_stw:
            setattr(self, i, stopwatch(self))
        
        self.busy = False
        self.state, self.interval = st_rest, None
        self.startTimer(1000)
    
        n = self.n()
        self.restoreState(sts.value('%s/state' % n, type=QByteArray))        
        self.resize(sts.value('%s/size' % n, type=QSize))
        self.move(sts.value('%s/pos' % n, type=QPoint))

        #self.mgr = m = mgr_due(self, cat('db', 'htm.db'))
        #m.msg_mgr.connect(self.handler_mgr)
        #self.cn = sqlite3.connect(m.db)
    
    def set_content(self):
        self.b.setUrl(QUrl.fromLocalFile(fs[self.idx]))

    def url_changed(self, u):
        pass #print(u.path())

    def handler(self, d):
        c = d['cnd'] 
        if c == 'full':
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        
        elif c == 'back':
            #self.b.back()
            self.idx -= 1
            self.idx %= len(fs)
            self.set_content()

        elif c == 'forward':
            #self.b.forward()
            self.idx += 1
            self.idx %= len(fs)
            self.set_content()

        elif c == 'edit':
            popen(['gvim', cat(repo, 'html_orig', '%s.html' % self.key())]) 

        elif c == 'refresh':
            beautify('%s.html' % self.key())
            self.set_content() 

        elif c == 'reset':
            self.stw.reset()
        
        elif c in ('delete', 'defer'):
            cn = self.cn
            cr = cn.cursor()
            if c == 'delete':
                self.prepare(s='')

            elif c == 'defer':
                self.prepare(s='')

    def handler_mgr(self, d):
        c = d['cnd'] 
        if c == 'rev':
            if self.state == st_learn:
                self.rev(d)
        
    def handler_tmr(self):
        st = self.state
        i = self.interval
        if i: 
            a, b = self.interval
            t2 = str2dt(now(utc=False))
            
            if st == st_learn:
                t1 = str2dt(a)
                t = (t2 - t1) if t2 > t1 else (t1 - t2)
                tp = ('orange', 'learn', nr2t(t.seconds))
            
            elif st == st_rest:
                t1 = str2dt(b)
                t = (t2 - t1) if t2 > t1 else (t1 - t2)
                tp = ('green', 'rest', nr2t(t.seconds))
            
            else:
                tp = ('red', '?', '')
        else:
            tp = ('red', '?', '')
       
        self.update_stb([
            ('stw', '<font color="purple">%s</font>' % (nr2t(self.stw.cnt / 10) if st == st_learn else '')),
            ('aux', '<font color="%s">%s&nbsp;&nbsp; %s</font>' % tp if tp != ('red', '?', '') else ''),])
        
    def prepare(self, to=500, s=''): 
        def f():
            self.busy = False
        QTimer.singleShot(to, f)
    
    def alarm(self, s):
        d = json.loads(s)
        for k, v in d.items():
            setattr(self, k, v)

        self.busy = True
        
        st = self.state
        if st == st_learn:
            self.prepare(to=2000)

        elif st == st_rest:
            self.close()

        elif st == st_none:
            self.close()

    def rev(self, d):
        for i in self.l_stw:
            getattr(self, i).reset()
    
        i = self.interval
        if i:
            i = map(utcstr, i)
        day = (today(), tomorrow())
        n_span_period = nr2t(n_span(cr, i))
        n_span_today = nr2t(n_span(cr, day))
       
        tl = []
        tl.append(('n_span', ('&nbsp;' * 3).join([
            '<font color="blue">%s</font>' % n_span_period,
            '<font color="purple">%s</font>' % n_span_today,
            ])))

        tl.append(('info', '<font color="blue"> %s </font>' % ellipsis(('&nbsp;' * 3).join(['test']))))
        
        self.update_stb(tl)
    
    def key(self):
        return f_no_ext(unicode(self.b.url().path()))

    def update_stb(self, tl):
        for sct, s in tl:
            self.msg({'msg': s}, sct)
    
    def msg(self, d, sct='info'):
        lbl = getattr(self, 'lbl_%s' % sct)
        msg = d.get('msg', '')
        to = d.get('to', 0)
        lbl.setText(msg)
        
        if to:
            QTimer.singleShot(to, partial(lbl.setText, ''))

    def send(self, **d):
        self.msg_win_htm.emit(d)

    def cls(self):
        n = self.n()
        if not self.isFullScreen() and not self.isMaximized():
            sts.setValue('%s/size' % n, QVariant(self.size()))
        sts.setValue('%s/state' % n, QVariant(self.saveState()))     

    def n(self):
        return self.__class__.__name__

    def timerEvent(self, e):
        if self.busy:
            return
        self.busy = True
        #self.mgr.go()

    def closeEvent(self, e):
        self.cls()

    def event(self, e):
        try:
            typ = e.type()
            if typ == QEvent.WindowActivate:
                for i in self.l_stw:
                    getattr(self, i).start() 
            
            elif typ == QEvent.WindowDeactivate:
                for i in self.l_stw:
                    getattr(self, i).stop() 
        finally:
            return QMainWindow.event(self, e) 

if __name__ == '__main__':

    DBusQtMainLoop(set_as_default=True) 
    argv = sys.argv
    app = QApplication(argv)
    app.setApplicationName('htm')
    app.setFont(QFont('Microsoft JhengHei'))

    argc = len(argv)
    w = win_htm()
    w.showMaximized()
    
    bus = dbus.SessionBus()
    bus.add_signal_receiver(w.alarm, dbus_interface=ifc, signal_name='alarm')
    try:
        w.alarm(bus.get_object(ifc, '/').state())
    except:
        pass 
    app.exec_()
