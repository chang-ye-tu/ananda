#!/usr/bin/env python3
from base import *

# tasks def
def gmail():
    popen(['python3', '/home/cytu/usr/src/py/ananda/gmail-notify.py'])

def hrv(n):
    popen(['python3', '/home/cytu/usr/src/py/ananda/hrv.py', '-t', str(hrv_read_rev), '-n', n])

def hrv_temp(n):
    popen(['python3', '/home/cytu/usr/src/py/ananda/hrv.py', '-t', str(hrv_read_rev), '-n', n, '-d', '/home/cytu/usr/src/py/ananda/db/ananda_temp.db'])

def rev(ns=None):
    if ns:
        l = ['python3', '/home/cytu/usr/src/py/ananda/rev.py', '-n']
        l.extend(ns)
    else:
        l = ['python3', '/home/cytu/usr/src/py/ananda/rev.py',]

    popen(l)

def rev_temp(ns=None):
    if ns:
        l = ['python3', '/home/cytu/usr/src/py/ananda/rev.py', '-d', '/home/cytu/usr/src/py/ananda/db/ananda_temp.db', '-n']
        l.extend(ns)
    else:
        l = ['python3', '/home/cytu/usr/src/py/ananda/rev.py', '-d', '/home/cytu/usr/src/py/ananda/db/ananda_temp.db']

    popen(l)

def word(n):
    popen(['python3', '/home/cytu/usr/src/py/ananda/rev.py', '-n', n, 
           '-d', '/home/cytu/usr/src/py/ananda/db/word.db',])

def drill(ns=None):
    l = ['python3', '/home/cytu/usr/src/py/ananda/drill.py',]
    if ns:
        l.extend(['-n'])
        l.extend(ns)
    popen(l)

def null(n):
    pass

class ananda(QWidget):

    p_on = './res/img/chronometer.ico'
    p_off = './res/img/player_time.ico'

    def __init__(self, par=None):
        super(ananda, self).__init__(par)
        
        self.td = tempfile.mkdtemp(prefix='%s_' % now().replace(':', ''), 
                                   dir=cat(os.getcwd(), tmp)) 
        self.ti = ti = QSystemTrayIcon(self)
        ti.setIcon(QIcon(self.p_on))
        ti.setToolTip('ananda') 
        ti.show()
        ti.activated.connect(self.act)
        
        self.cn = sqlite3.connect(cat('db', 'ananda.db'))

        self.mn = mn = QMenu(self)
        for i in ['stat', None, 'eye', None, 'quit']:
            if i is None:
                mn.addSeparator()
            else:
                setattr(self, 'act_%s' % i, QAction(i, self))
                a = getattr(self, 'act_%s' % i)
                a.triggered.connect(getattr(self, i)) 
                mn.addAction(a)        
        
        ti.setContextMenu(mn)
        
        self.d_job = {} # use for storing job_id: job_name
        self.sched = sc = QtScheduler()
        sc.add_listener(self.listen, EVENT_JOB_EXECUTED) 
        sc.start()
        
        self.dso = dso()

        self.i_fix = 0
        
        # add dbus signal receiver
        for f, s in [(self.show_splash, 'show_splash'),
                     (self.schedule, 'schedule'),
                     (self.notify, 'alarm'),
                    ]:
            dbus.SessionBus().add_signal_receiver(f, dbus_interface=ifc,
                                                  signal_name=s)
        self.av = QMediaPlayer(self)
        
        self.b_splash = True
        
        # firing gmail after 1 secs 
        QTimer.singleShot(1000, gmail)
        
        # default null after 1 secs
        QTimer.singleShot(1000, 
                partial(self.schedule, json.dumps([['null', '', 10000, 1],])))

        # XXX dimming after 10 secs
        #QTimer.singleShot(10000, partial(popen, 'xcalib -co 70 -a'.split()))

    def notify(self, s):
        d = json.loads(s)

        ti = self.ti
        st = d['state'] 
        if st == st_learn:
            self.play_audio('/home/cytu/usr/src/py/ananda/res/av/learn.mp3')
            ti.setIcon(QIcon(self.p_on))
            
        elif st == st_rest:
            self.play_audio('/home/cytu/usr/src/py/ananda/res/av/rest.mp3')
            ti.setIcon(QIcon(self.p_off))
    
    def timerEvent(self, e):
        t0 = str2dt(now(utc=False))
        t1 = str2dt(self.tic) 
        t2 = str2dt(self.toc) 
        if t0 <= t1:
            t = t1 - t0
        elif t1 < t0 <= t2:
            t = t2 - t0
        else:
            t = t_delta()

        self.ti.setToolTip('%s left %s' % (nr2t(t.seconds), 
                           '' if self.b_splash else '[no splash]'))

    def act(self, i):
        if i == QSystemTrayIcon.Trigger:
            self.mn.exec_(QCursor.pos())
    
    def add_session(self):
        if (self.cnt + 1) > len(self.tbl):
            return

        sc = self.sched
        st = self.state
        
        fn, arg, tlrn, trst = self.tbl[self.cnt]
        self.tic = now(utc=False) if self.first else self.toc
        self.toc = t_add(t_delta(minutes=(tlrn if st == st_learn else trst)), self.tic) 
        name = 'learn' if st == st_learn else 'rest' 
        job = sc.add_job(self.dso.alarm, 
            args=[json.dumps({'state': st, 'interval': (str(self.tic), str(self.toc))}),], 
            trigger='date', run_date=str(self.tic), misfire_grace_time=2, name=name)
        self.d_job[job.id] = name

        if st == st_learn:
            ff = globals()[fn]
            sc.add_job(ff, args=[arg,], trigger='date', run_date=str(self.tic), 
                       misfire_grace_time=2)
        else:
            self.cnt += 1

        self.first = False
        self.state = st_learn if st == st_rest else st_rest
    
    def listen(self, e):
        if self.d_job.get(e.job_id, '') in ('learn', 'rest'):
            self.add_session()
    
    def stat(self):
        pass

    def eye(self):
        self.b_splash = not self.b_splash
    
    def show_splash(self):
        if self.b_splash:
            self.splash = splash()
            self.splash.showFullScreen()
    
    def schedule(self, s):
        ti = self.ti
        tbl = json.loads(s)
        sc = self.sched
        
        self.close_widgets()

        def f():
            # clear all scheduled jobs
            for j in sc.get_jobs():
                sc.remove_job(j.id)
            
            # add splash service 
            sc.add_job(self.dso.show_splash, trigger='interval', minutes=10, 
                start_date=str(t_add(t_delta(minutes=9), now(utc=False))),
                name='splash')
        
            self.state, self.first, self.cnt = st_learn, True, 0
            self.tbl = tbl
            self.add_session()

        QTimer.singleShot(3000, f)
    
    def play_audio(self, src):
        av = self.av
        av.setMedia(QMediaContent(QUrl.fromLocalFile(src)))
        av.play()
    
    def close_widgets(self):
        # broadcasting 
        self.sched.add_job(self.dso.alarm, 
            args=[json.dumps({'state': st_none, 'interval': None}),], 
            trigger='date', misfire_grace_time=2, run_date=str(now(utc=False)),
            name='close')

    def quit(self):
        self.close_widgets() 
        
        def f(): 
            self.sched.shutdown(wait=False) 
            self.ti.hide()  # trick to cleanup the icon
            shutil.rmtree(self.td)
            qApp.quit()

        QTimer.singleShot(3000, f)

if __name__ == '__main__':
    DBusQtMainLoop(set_as_default=True) 
    
    app = QApplication(sys.argv)
    app.setApplicationName('ananda')
    app.setFont(QFont('Microsoft JhengHei'))
    app.setQuitOnLastWindowClosed(False)
    
    l = []
    p = re.compile(r'\d{4}-\d{2}-\d{2} \d{6}_')
    for root, dirs, files in os.walk(tmp):
        for d in dirs:
            if p.match(d):
                l.append(cat(root, d))
    for ll in l:
        shutil.rmtree(ll)
    
    w = ananda()
    app.exec_()
