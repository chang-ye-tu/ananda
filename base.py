import os, sys, math, re, base64, datetime, subprocess, shutil, tempfile, codecs, atexit, bisect, copy, traceback, logging, hashlib, time, argparse
from random import choice, uniform, shuffle
from functools import partial
from fnmatch import fnmatch

try: 
    import simplejson as json
except ImportError: 
    import json

import dbus
import dbus.service
from dbus.mainloop.pyqt5 import DBusQtMainLoop

os.chdir(os.path.dirname(__file__))
cat = os.path.join
call = subprocess.call
popen = subprocess.Popen
pipe = subprocess.PIPE

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtNetwork import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from pathlib import Path

from apscheduler.schedulers.qt import QtScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from doc import * 
from db.db import * 
from db.dt import *
from av import wdg_a

cwd = '/home/cytu/usr/src/py/ananda/ex/data'
sys.path.insert(0, cwd)
tmp = 'tmp'
sts = QSettings(cat('res', 'ananda.ini'), QSettings.IniFormat)

ifc = 'ananda.ctrl'
st_none, st_learn, st_rest = range(3)
rev_normal, rev_drill = range(2) 
hrv_edt, hrv_read, hrv_read_rev = [1 << i for i in range(3)]

w_desktop = int(re.compile(r'current (\d+) x').search(os.popen('xrandr -q -d :0').readlines()[0]).groups()[0])
im_width = .945 * w_desktop

#_ = QApplication.instance()
#screen = _.screens()[0]
#dpi = screen.physicalDotsPerInch()
#_.quit()

# XXX
logging.basicConfig(filename='/home/cytu/usr/src/py/ananda/tmp/log.txt', 
                    format='%(asctime)s %(levelname)s: %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S', 
                    level=logging.INFO)
logger = logging.getLogger('cytu')

def log(s, b_file=False):
    print(s)
    #if b_file:
    #    logger.info(s) 
    #else:
    #    print(s)

def attrs_from_dict(d):
    self = d.pop('self')
    for k, v in d.items():
        setattr(self, k, v)

def ellipsis(s, n=90, typ='middle'):
    ns = len(s)
    if ns <= n:
        return s
    else:
        if typ == 'front':
            return '...%s' % s[:n]
        elif typ == 'last':
            return '%s...' % s[:n]
        elif typ == 'middle':
            return '%s...%s' % (s[:n//2], s[-n//2:]) 

def is_lang(s):
    return s.split('_')[0] in ['de', 'en', 'jp', 'fr', 'ru', 'tw', 'cs', 'gen']
                                                                   #XXX cs, gen
def f_ana(n):
    return cat(cwd, n if is_lang(n) else ('%s.ana' % n))

def f_no_ext(n):
    return os.path.splitext(os.path.split(n)[1])[0] 

def get_ana(n):
    try:
        return json.loads(open(f_ana(n), 'r').read())
    except:
        return None

def save_ana(d):
    try:
        s = json.dumps(d, sort_keys=True, indent=2)
        open(cat(cwd, f_ana(d['name'])), 'w').write(s)
        return True
    except:
        return False

# reference ~~
def htm(s, css='', b_math=False):
    css = css if css else '/home/cytu/usr/src/py/ananda/res/ananda.css'
    
    s_math = r'''<script type='text/javascript'>
window.MathJax = {
  tex: {
    inlineMath: [ ['$','$'], ["\\(","\\)"] ],
    displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
    processEscapes: true,
    packages: ['base', 'ams']
  },
  options: {
    ignoreHtmlClass: 'tex2jax_ignore',
    processHtmlClass: 'tex2jax_process'
  }
};
</script>
<script type='text/javascript' src="/home/cytu/bin/mathjax/tex-chtml.js" id="MathJax-script"></script>
''' if b_math else ''

    return r'''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 
    'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<meta http-equiv='X-UA-Compatible' content='IE=EmulateIE7' >
<head>
<link rel='stylesheet' type='text/css' href='%s' media='screen, projection'/>
%s
</head>
<body>
<div id='outer'><div id='middle'><div id='inner'>
%s
</div></div></div>
</body>
</html>
''' % (css, s_math, s) 

# XXX generalized to ks = {'keys': [], 'key': '...'}
def fact_key(ks, d, klist=None):
    name = d['name']
    l = []
    b_str = False
    if isinstance(ks, str):
        ks_orig = ks
        ks = {'keys': [ks]}
        b_str = True

    if is_lang(name): # languages
        for k in ks['keys']:
            for qa_ in d['qa'][k]:
                dd = {} 
                for j in ['q', 'a']:
                    dd[j] = [{'txt': qa_[j]}]
                l.append(dd)
    else:
        qa = d['qa']
        sha = d['sha'] 
        
        for k in ks['keys']:
            if klist is not None and k in klist:
                dd = klist[k][0]

            else:
                dd = {}
                for j in ['q', 'a']:
                    dd[j] = [{'sha':sha,'pg':n_pg,'path':a} for n_pg, a in qa[j][k]]
                
            l.append(dd)
    
    return json.dumps({'qas': l, 'meta': {'name': name, 'key': ks_orig if b_str else ks['key']}})

def get_name_key(fact_id, cr):
    try:
        m = json.loads(fact(fact_id, cr)[0])['meta']
        return m['name'], m['key']

    except:
        return '', ''

def item_data(i, k=None):
    # XXX different with doc ??
    da = i.data(Qt.UserRole, 0) if isinstance(i, QTreeWidgetItem) else i.data(Qt.UserRole)
    d = json.loads(da) # XXX toString()?
    if k is None:
        return d
    return d[k]

def confine(n, tp):
    floor, cap = min(tp), max(tp)
    nn = int(n)
    if nn < floor:
        n = floor
    elif nn > cap:
        n = cap
    else:
        n = nn
    return n

def parse_range(s, tp):
    floor, cap = min(tp), max(tp)
    # allowed str: 
    alpha = '0123456789,-eo '
    for i in s:
        if i not in alpha:
            return False, []
    # discard all spaces; tokens are separated by comma    
    tks = [i.replace(' ', '') for i in s.split(',') if i.replace(' ', '')]
    n = []

    # eg. -e, 1-20o  
    p = re.compile(r'^\d*-?\d*[eo]?$') 

    def even_odd(l, f):
        if not f:
            return l
        return [i for i in l if i % 2 == (0 if f == 'e' else 1)] 
    
    for t in tks:
        if p.match(t):
            f = ''
            if t[-1] in 'eo':
                f = t[-1] 
                t = t[:-1]

            l = t.split('-')
            final = []
            if len(l) == 1:
                try:
                    i = int(l[0])
                    if floor <= i <= cap:
                        final = [i]     
                except:
                    return False, []

            elif len(l) == 2:
                a, b = l
                a = confine(a, tp) if a else floor
                b = confine(b, tp) if b else cap
                final = range(min(a, b), max(a, b) + 1)

            else:
                return False, []       
            
            n.extend(even_odd(final, f))

        else:
            return False, []

    return True, sorted(list(set(n))) 

# XXX image width should be determined by both q & a 
def combine(li, w, space=15):
    lh = [i.height() for i in li]
    im = QImage(QSize(w, sum(lh) + (len(li) - 1) * space), QImage.Format_RGB32)
    im.fill(QColor('white').rgb())
    p = QPainter(im)
    for ii, i in enumerate(li):
        # only adjust width when it's too big XXX hardcoded dpix 102 on acer 10/27/21 11:06:47
        j = i.scaledToWidth(w_desktop * 96 / 102, Qt.SmoothTransformation) if i.width() > w_desktop else i
        p.drawImage(QPoint(0, sum(lh[:ii]) + ii * space), j)
    p.end()
    return im

def bin_dumps(b):
    return base64.b64encode(b)

def bin_loads(s):
    return base64.b64decode(s)

def dt_now():
    return datetime.datetime.now()

def lapse(dlt):
    n = (1 if dlt.microseconds > 5e5 else 0) + dlt.seconds + dlt.days * 24 * 3600 
    mm, ss = divmod(n, 60)
    hh, mm = divmod(mm, 60)
    return '%02d:%02d:%02d' % (hh, mm, ss)

def prefab_fact(name, cn):
    cr = cn.cursor()
    try:
        keys = json.loads(cr.execute('select keys from prefab where name = ?', (name,)).fetchone()[0])
        if not keys:
            return False, None
    except:
        return False, None
    
    kk = keys.pop(0)
    # XXX used in 'compound' review:
    #   prepare for something like ['1.1', 'aliprantis'] instead of standard '1.1'
    k, n = kk if isinstance(kk, (tuple, list)) else (kk, name)

    cr.execute('update prefab set keys = ? where name = ?', (json.dumps(keys), name))
    cn.commit()

    return True, fact_key(k, get_ana(n)) 

# XXX 09/10/15 
def width_qa(l):
    return max([i.width() for i in l]) 

# XXX best sched algorithm? 
def compute_sched(fact_id, grade, cr):
    h = history(fact_id, cr)     
    created = h['created']
    all_at = h['all_at']
    last_at = h['last_at']
    n_at = h['n_at']
    last_grade = h['last_grade']
    all_fail = h['all_fail']
    last_fail = h['last_fail']
    n_fail = h['n_fail']  
    que = h['que']
    age = str2dt(now()) - str2dt(created)
    
    # "Climbing the Ladder: Road to Perfection" 07/12/12 12:58:27
    #
    # [review algorithm considerations]
    #
    # language vs. math
    #first review?
    #recurrent events frequency?
    #  fixed interval
    #
    #incorporate due/work queue info
    #allocate new / old distributions soundly: smooth, even learning flow
    #
    #long (math) items occupy much time. how to compensate? 
    #disturbance: not too many new facts in a period of time
    #  first 
    #  average item learning time is so different
    # 
    #distinction: short-term and long-term behaviour
    #  long-term: unperturbed 
    #  short-term: volatile     
    #
    #how to treat once remembered but now forgetted facts?
    #  short-term:
    #  long-term:
    #
    #hardness:
    #  hard items should pop up often, but easy items shouldn't 
    #  ** inconceivable items ? 
    #     defer first
    #     do it at 'suitable' time, eg. after well performed reviews, at sober times

    #b_longterm = (age >= t_delta(days=21) and n_at >= 4)
    avg = sum(grade) / len(grade)        
    #if avg < last_grade:
    #    t_d = t_delta(minutes=30)

    #else:
    if n_at == 0:
        t_d = t_delta(days=1)  #t_d = t_delta(minutes=30)

    elif n_at == 1:
        t_d = t_delta(days=2)
        
    elif n_at == 2:
        t_d = t_delta(days=6)
    
    else:
        if avg < 3:
            td = t_delta(days=1)

        else:
            if 3 <= avg < 3.5:
                n = uniform(1.8, 2.0)

            elif 3.5 <= avg < 4:
                n = uniform(2.0, 2.2)
            
            elif 4 <= avg < 4.5:
                n = uniform(2.2, 2.4)
            
            else:
                n = uniform(2.4, 2.6)
        
            t_d = t_delta_mult(str2dt(now()) - str2dt(last_at), n)

    return t_add(t_d, now())

class dso(dbus.service.Object): 
    
    def __init__(self): 
        dbus.service.Object.__init__(self, dbus.service.BusName(ifc, bus=dbus.SessionBus()), '/')  
        self.s = json.dumps({'state': st_rest, 'interval': None}) 

    @dbus.service.signal(ifc)
    def alarm(self, s):
        self.s = s

    @dbus.service.signal(ifc)
    def show_splash(self):
        pass

    @dbus.service.signal(ifc)
    def schedule(self, s):
        pass 
    
    @dbus.service.signal(ifc)
    def auto(self):
        pass

    @dbus.service.method(ifc, in_signature='', out_signature='s')
    def state(self):
        return self.s

class stopwatch(QTimer):

    def __init__(self, par):
        super(stopwatch, self).__init__(par)
        self.cnt = 0
        self.setInterval(100)
        self.timeout.connect(self.tic)

    def tic(self):
        self.cnt += 1
    
    def elapsed(self):
        return self.cnt

    def reset(self):
        self.cnt = 0

class thread(QThread):

    msg_thread = pyqtSignal(dict)

    def __init__(self, par=None):
        super(thread, self).__init__(par)
     
    def send(self, **d):
        self.msg_thread.emit(d)
    
    def n(self):
        return self.__class__.__name__

    def go(self, **kw):
        self.end()
        d = locals()
        self = d.pop('self')
        for k, v in d['kw'].items():
            setattr(self, k, v)
        self.start()

    def end(self):
        if self.isRunning():
            self.wait()

    def run(self):
        pass
    
class mgr_due(thread):
    
    def __init__(self, par, db, names=None):
        super(mgr_due, self).__init__(par)
        self.db = db
        self.td = getattr(par, 'td')
        self.cache = {}
        self.names = names

    def p2f(self, p):
        td = self.td
        f = cat(td, 'combine.png')
        p.save(f)
        fn = cat(td, sha(f))
        if not os.path.isfile(fn):
            shutil.copy(f, fn)
        return fn

    def get_d_rect(self, d, cr):
        td = self.td
        sha = d['sha']
        doc, meta = None, {}

        if sha in self.cache:
            c = self.cache[sha]
            doc = c['doc']
            meta = c['meta']
        
        else:
            f = cat(td, sha)
            if not os.path.isfile(f):
                f, meta = load_f(sha, td, cr)
            
            typ = test_f(f)
            if typ == PDF:
                doc = doc_pdf()

            elif typ == DJV:
                doc = doc_djvu()
            
            if doc.open(f, render=False):
                z = meta.get('z', 2.7) * w_desktop / 1366 * 0.97
                doc.set_z(z, render=False)
                meta['z'] = z
                self.cache[doc.sha] = {'doc': doc, 'meta': meta}
        
        zo = meta['zo']
        z = meta['z']
        # XXX 12/13/21 23:22:14
        zz = 2. * z / zo * 102 / 96
        mm = QTransform(zz, 0, 0, zz, 0, 0)
        return doc.render(d['pg']).copy(mm.mapRect(QRectF(*d['path'])).toRect())

    def combine_p(self, dl, cr, w_pl):
        return combine([self.get_d_rect(d, cr) for d in dl], w_pl)

    def fact_to_htm(self, fact_id, cr, css='', b_math=False, b_hr=False, b_all=True):
        b_txt = False
        td = self.td
        dd = json.loads(fact(fact_id, cr)[0])
        qas = dd['qas']
        all_s, preview_s = [], []
        for jj in qas:
            hl = ['', '']
            a = ['', '']
            
            # XXX 09/10/15 'unnatural' two-steps enumeration
            pl, al, tl, xl = [[], []], [[], []], [[], []], [[], []]
            pls = []
            for i, part in enumerate([jj['q'], jj['a']]):
                for d in part:
                    t = test(d)
                    if t == TXT:
                        tl[i].append(d)
                    
                    elif t == EBK:
                        pl[i].append(d)
                        pls.append(d)
                    
                    elif t == AV:
                        al[i].append(d)
                    
                    elif t == PIX:
                        xl[i].append(d)
            
            # determine w_pl from pls
            w_pl = width_qa([self.get_d_rect(d, cr) for d in pls]) 

            for i in range(2): 
                if tl[i]:
                    hl[i] += ''.join([d['txt'] for d in tl[i]]) 
                    b_txt = True

                if pl[i]:
                    hl[i] += '<img src="%s">' % self.p2f(self.combine_p(pl[i], cr, w_pl))
                
                if al[i]:
                    # XXX only the first of recs
                    f = load_f(al[i][0]['sha'], td, cr)[0]
                    a[i] = '<audio src="%s" autoplay></audio>' % f if f else ''
                
                hl[i] += ''.join(['<img src="%s">' % load_f(xx['sha'], td, cr)[0] for xx in xl[i]]) 
                   
            b = b_math and b_txt
            s = ['<div class="%s">%s</div>' % (('answer' if ii else 'question') + ('' if b_all else '_pre'), h) \
                 if h else '' for ii, h in enumerate(hl)] 
            all_s.append([
            htm((a[0] + 'Listen to the Question ...') if (a[0] and hl[0] == '') \
                else (a[0] + s[0]), css, b),  
            htm((a[1] + 'Listen to the Answer ...') if (a[1] and hl == ['', '']) \
                else (a[1] + ('<hr />' if b_hr else '').join(s)), css, b)
            ])
            preview_s.append((a[1] + 'Listen to the Answer ...') if (a[1] and hl == ['', '']) else (a[1] + ('<hr />' if b_hr else '').join(s)))

        return all_s if b_all else htm('\n'.join(['<div class="fact">%s</div>' % s for s in preview_s]), css, b)

    def run(self):
        cn = sqlite3.connect(self.db)
        cn.create_function('meta_name', 1, meta_name)
        cn.create_function('meta_key', 1, meta_key)
        cr = cn.cursor()
        
        # check due rev
        r = due_rev(cr, names=self.names)
        if r:
            rev_id, fact_id = r[:2]

        else:
            l = self.names if self.names else [i[0] for i in cr.execute('select name from prefab').fetchall()]
            if not l:
                self.send(cnd='none: no active categories')
                return
            
            name = choice(l)
            b, fa = prefab_fact(name, cn)
            if not b:
                self.send(cnd='none: all done')
                return
            fact_id, rev_id = insert_new_fact(fa, cr)
            cn.commit()
        
        b = is_lang(get_name_key(fact_id, cr)[0]) 
        # language contents are rendered with hr, bigger font and no frames
        self.send(cnd='rev', rev_id=rev_id, fact_id=fact_id, qas=self.fact_to_htm(fact_id, cr, b_hr=b, b_math=(not b),
                  css=('/home/cytu/usr/src/py/ananda/res/ananda_noframe.css' if b else ''),))

class overlay(QWidget):

    def __init__(self, par, b_dyn=True):
        
        QWidget.__init__(self, par)
        p = QPalette(self.palette())
        p.setColor(p.Background, Qt.transparent)
        self.setPalette(p)
        self.b_dyn = b_dyn

    def paintEvent(self, e):
        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(e.rect(), QBrush(QColor(0, 0, 0, 30)))
        
        if self.b_dyn:
            p.setPen(QPen(Qt.NoPen))
            n = 8 
            for i in range(n):
                if (self.cnt / (n - 1)) % n == i:
                    p.setBrush(QBrush(QColor(127 + (self.cnt % (n - 1)) * 128 / (n - 1), 127, 127)))
                else:
                    p.setBrush(QBrush(QColor(127, 127, 127)))

                p.drawEllipse(self.width() / 2 + 30 * math.cos(2 * math.pi * i / (n * 1.)) - 10,
                              self.height() / 2 + 30 * math.sin(2 * math.pi * i / (n * 1.)) - 10,
                              14, 14)
        p.end()
    
    def showEvent(self, e):
        app = QApplication.instance()
        self.setGeometry(app.desktop().availableGeometry(0))
        if self.b_dyn:
            self.timer = self.startTimer(30)
            self.cnt = 0
    
    def timerEvent(self, e):
        self.update()        
        self.cnt += 1

    def hideEvent(self, e):
        try:
            self.killTimer(self.timer)
        except:
            pass

class browser(QWebEngineView):

    def __init__(self, par=None):
        super(browser, self).__init__(par)

    def set_htm(self, h='', ref='/home/cytu/sample.html', b_raw=False):
        self.setHtml(h if b_raw else htm(h), QUrl.fromLocalFile(str(Path(__file__).resolve().parent)))

class win_b(QMainWindow):
    
    def __init__(self, par=None, htm='', nb_name=''):
        QMainWindow.__init__(self, par)
        self.setWindowTitle(u'Preview')
        self.setWindowIcon(QIcon(':/res/img/tex.png'))
        #self.setAttribute(Qt.WA_DeleteOnClose)

        self.b = b = browser(self)
        self.setCentralWidget(b)
        b.setFocusPolicy(Qt.NoFocus)
        b.set_htm(htm)

        self.nb_name = nb_name

        for i, k in [#('pg_up', ('PgUp', 'Up')),
                     #('pg_dn', ('PgDown', 'Down')),
                     ('quit',  ('Esc', 'Ctrl+Q',)),
                     ('vim',   ('F12',)),
                     ]:
            n = 'act_%s' % i
            setattr(self, n, QAction(self))
            a = getattr(self, n)
            a.setShortcuts([QKeySequence(kk) for kk in k])

            #if i in ('pg_dn', 'pg_up'):
            #    f = partial(b.page().currentFrame().scroll, 
            #                0, (1 if i == 'pg_dn' else -1) * 50)
            #else:
            f = partial(self.handler, {'cnd': i})
            a.triggered.connect(f)

            self.addAction(a)
    
        n = self.n()
        self.restoreState(sts.value('%s/state' % n, type=QByteArray))        
        self.resize(sts.value('%s/size' % n, type=QSize))

    def set_htm(self, htm):
        self.b.set_htm(htm)

    def handler(self, d):
        c = d['cnd']
        if c == 'quit':
            self.close()
        elif c == 'vim':
            focus(all_w(self.nb_name.upper())['vim'])

    def closeEvent(self, e):
        n = self.n()
        if not self.isFullScreen() and not self.isMaximized():
            sts.setValue('%s/size' % n, QVariant(self.size()))
            sts.setValue('%s/state' % n, QVariant(self.saveState()))        
    
    def n(self):
        return self.__class__.__name__

class splash(QLabel):
    
    def __init__(self, par=None, cnt=60, show_txt=True, pix=None, css=''):
        super(splash, self).__init__(par)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(css if css else 'QLabel{background-color: rgb(0, 200, 0); color: rgb(255, 255, 255); font: %spt "Microsoft JhengHei";}' % (int(28),))   
        
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        sz = QApplication.desktop().size()
        if pix is not None:
            # Resize the image if it's bigger than the screen
            if pix.size().height() > sz.height(): 
                pix = pix.scaledToHeight(sz.height() - 30, Qt.SmoothTransformation)
                
            if pix.size().width() > sz.width():   
                pix = pix.scaledToWidth(sz.width() - 30, Qt.SmoothTransformation)

            self.setPixmap(pix)

        self.show_txt = show_txt
        self.cnt = cnt
        self.display()
        self.startTimer(1000)
        
        try:
            o = dbus.SessionBus().get_object('ananda.loci', '/loci')
        except:
            p = self.cursor().pos()
            #QTimer.singleShot(1000, partial(click, (p.x(), p.y())))

    def display(self):
        if self.cnt:
            if self.show_txt:
                self.setText('Time to Take a Break and Do Eye Exercises!  %s Left' % nr2t(self.cnt))
            self.cnt -= 1
        else:
            self.close()
    
    def keyPressEvent(self, e):
        k = e.key()
        if k == Qt.Key_Escape:
            self.close()
        else:
            QLabel.keyPressEvent(self, e)

    def timerEvent(self, e):
        self.display()

# ==============================================================================
#  vim netbeans interface 
# ==============================================================================

class sck(QTcpSocket):
    
    msg_sck = pyqtSignal(str)
    killed = pyqtSignal()

    def __init__(self, par=None):
        super(sck, self).__init__(par)
        self.readyRead.connect(self.get)
        self.disconnected.connect(self.kill)

    def get(self):
        self.msg_sck.emit(str(self.readAll()))

    def kill(self):
        self.killed.emit()
        self.deleteLater()

    def send(self, d):
        self.write(d)
        
class nb(QTcpServer):

    msg_vim = pyqtSignal(dict)

    def __init__(self, par=None):
        super(nb, self).__init__(par)
        self.s = None

    def incomingConnection(self, id):
        if self.s is None:
            self.s = s = sck(self)
            s.setSocketDescriptor(id)
            s.msg_sck.connect(self.handler)
            s.killed.connect(self.kill)
        else:
            print('decline connection')

    def kill(self):
        try:
            self.s.close()
        except:
            pass        
        self.s = None

    def handler(self, s):
        rs = [i.strip() for i in s.split('\n') if i.strip()]
        
        def send(**d):
            self.msg_vim.emit(d)

        for r in rs:
            d = {}
            if r.find('keyCommand=') != -1:
                # eg. 1:keyCommand=3 "F11"
                k = r.split(' ')[-1].strip().replace('"', '')
                if k:
                    send(cnd='key', keycode=k)

            elif r.find('killed=') != -1:
                # vim incidentally closed
                send(cnd='killed')

            elif r.find('insert=') != -1:
                k = r.split(' ')[-1].strip().replace('"', '') 
                # '   ' is nonempty
                #if k:
                #    send(cnd='nonempty')
                send(cnd='insert', txt=k)

    def send(self, s):
        if self.s is None:
            return
        self.s.send(s)
    
    def close(self):
        if self.s is None:
            return
        self.s.close()

def args(l, name):
    a = ['gvim', '--servername', name]
    a.extend(l)
    return a

def vim_gui(name):
    call(args(['-geom', '200x5+0+0', #'20x25+1100', 
               '-c', 'set gfn=DejaVu\ Sans\ Mono\ 18', 
             ], name))

def vim_mv(name):
    call(args(['--remote-send', r'<c-\><c-n>:winpos 0 560<cr>'], name))

def vim_nb(name, port):
    call(args(['--remote-send', r'<c-\><c-n>:nbs :localhost:%s:cytu<cr>' % port], name))

def vim_buf(name, td, src):
    f = cat(td, 'hrv.vim')
    open(f, 'w').write(src)
    call(args(['--remote-send', r'<c-\><c-n>:so %s<cr>GA' % f], name))  

def vim_cls(name):   
    call(args(['--remote-send', r'<c-\><c-n>ggVGxi'], name))

def vim_kill(name):
    call(args(['--remote-send', r'<c-\><c-n>:q!<cr>'], name))

def vim_get(name):
    expr = '--remote-expr'
    p = popen(args([expr, 'getbufline("%", 1, "$")'], name), stdout=pipe)
    return p.communicate()[0].decode('utf-8').strip()

def vim_set(name, s, b_append=False):
    expr = '--remote-expr'
    sl = json.dumps(s.encode('utf-8').split('\n'))
    if b_append:
        call(args([expr, 'append(line("$"), %s)' % sl], name))
    
    else:
        #vim_cls()
        call(args([expr, 'setline(0, %s)' % sl], name))

# ==============================================================================
#  xlib focus 
# ==============================================================================

import Xlib.display
from Xlib import X

dpy = Xlib.display.Display()
root = dpy.screen().root

def all_w(name_vim):
    try:   
        w_hrv, w_rev, w_vim, w_prv = [], [], [], [] 
        for w in root.query_tree()._data['children']:
            n = w.get_wm_name()
            c = w.get_wm_class()
            #width = w.get_geometry()._data['width']
            #height = w.get_geometry()._data['height']

            if n is None or c not in (('gvim', 'Gvim'), 
                                      ('hrv.py', 'Hrv.py'), 
                                      ('rev.py', 'Rev.py')):
                continue

            if n.find(name_vim) != -1 and c == ('gvim', 'Gvim'):
                w_vim.append(w)
            
            elif c == ('hrv.py', 'Hrv.py'):
                if n.find('Ebook Harvester') != -1:
                    w_hrv.append(w)
                elif n.find('Review') != -1:
                    w_rev.append(w)
                elif n.find('Preview') != -1:
                    w_prv.append(w) 

            elif c == ('rev.py', 'Rev.py'):
                if n.find('Review') != -1:
                    w_rev.append(w)
                elif n.find('Preview') != -1:
                    w_prv.append(w) 

        return {'vim': w_vim, 'hrv': w_hrv, 'rev': w_rev, 'prv': w_prv}
    
    except:
        return {'vim': [], 'hrv': [], 'rev': [], 'prv': []}
    
def focus(lw):
    if not lw:
        return 
    root.send_event(Xlib.protocol.event.ClientMessage(window=lw[0], client_type=dpy.intern_atom('_NET_ACTIVE_WINDOW'), data=(32, [0, 0, 0, 0, 0])), event_mask=X.SubstructureRedirectMask|X.SubstructureNotifyMask)
    dpy.flush()

# ==============================================================================
#  pulseaudio 
# ==============================================================================

audio_pc, audio_ear = range(2)

def set_audio(audio=audio_pc, vol=2**16/100*40):
    #n = 'alsa_output.usb-Sennheiser_Communications_Sennheiser_USB_Headset-00-Headset.analog-stereo' if audio else 'alsa_output.pci-0000_00_1b.0.analog-stereo'
    #call(['pacmd', 'set-default-sink', n])
    #call(['pacmd', 'set-sink-volume', n, str(vol)])
    pass

# ==============================================================================
#  rebuild database 
# ==============================================================================

## XXX 03/08/14
#def update_doc(cn):
#    cr = cn.cursor()
#    d = get_ana('ash_real')
#    src = d['src']
#    qa = d['qa']
#    z = d['z']
#    zo = d['zo']
#    sha = d['sha'] 
#    r = cr.execute('select data from res where sha = ?', (sha,)).fetchone()
#    if not r:
#        cr.execute('insert into res (data, sha, meta) values (?, ?, ?)', 
#            (sqlite3.Binary(open(src, 'rb').read()), sha, 
#            json.dumps({'fn': os.path.basename(src), 'z': z, 'zo': zo})))
#    
#    #all_i = []
#    #sha_old = '"d81ba83b2597d1e507e6bbb7145f475fb976b49d2a5712cc9eaa6d8c"'
#    #sha_new = '"26e07bd720ab03d4d822f7054eb2b63beaeb622c3776960fa9f239f9"' 
#    #r = cr.execute('select id, data from fact').fetchall()
#    #for i, d in r:
#    #    if d.find(sha_old) != -1:
#    #        all_i.append(i)
#    #for i in all_i:
#    #    d = cr.execute('select data from fact where id = ?', (i,)).fetchone()[0]
#    #    cr.execute('update fact set data = ? where id = ?', (d.replace(sha_old, sha_new), i))
#    cn.commit() 

def fact_order(fact): 
    q0 = json.loads(fact)['qas'][0]['q'][0]
    return (q0['pg'], q0['path'][1])

def revamp(name, dbf):
    # 1. find all existing facts of 'name'
    # 2. delete all DUE reviews; reschedule  
    cn = sqlite3.connect(dbf)
    cn.create_function('fact_order', 1, fact_order)
    cn.create_function('meta_name', 1, meta_name)
    cr = cn.cursor()
    ids = cr.execute('select id from fact where meta_name(data) = ? order by fact_order(data)', (name,)).fetchall()
    for ii, i in enumerate(ids):
        cr.execute('update rev set sched = ? where at = "" and fact_id = ?', (t_add(t_delta(seconds=ii), now()), i[0]))
    cn.commit()

def rebuild_db(name, dbf):
    # 1. find all existing facts of 'name'
    # 2. delete all corresponding facts AND reviews
    # 3. reinsert fact AND reschedule  
    cn = sqlite3.connect(dbf)
    cn.create_function('fact_order', 1, fact_order)
    cn.create_function('meta_name', 1, meta_name)
    cr = cn.cursor()
    all_data = cr.execute('select data from fact where meta_name(data) = ? order by fact_order(data)', (name,)).fetchall()
    cr.execute('delete from rev where rev.fact_id in (select id from fact where meta_name(fact.data) = ?)', (name,))
    cr.execute('delete from fact where meta_name(data) = ?', (name,))
    cr.execute('vacuum')
    for da in all_data:
        insert_new_fact(da[0], cr)
    cn.commit()

#rebuild_db('kirsch_grinberg', os.path.join(os.path.dirname(__file__), 'db', 'ananda_temp.db'))

#cn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'db', 'ananda.db'))
#update_doc(cn[0])
