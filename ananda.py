from base import *

def gmail():
    popen(['python', '/home/cytu/usr/src/py/ananda/gmail-notify.py',])

def hrv(n):
    popen(['python', '/home/cytu/usr/src/py/ananda/hrv.py', '-t', str(hrv_read_rev), '-n', n])

def hrv_temp(n):
    popen(['python', '/home/cytu/usr/src/py/ananda/hrv.py', '-t', str(hrv_read_rev), '-n', n, '-d', '/home/cytu/usr/src/py/ananda/db/ananda_temp.db'])

def rev(ns=None):
    l = ['python', '/home/cytu/usr/src/py/ananda/rev.py',]
    if ns:
        l.extend(['-n'])
        l.extend(ns)
    popen(l)

def rev_temp(ns=None):
    l = ['python', '/home/cytu/usr/src/py/ananda/rev.py', '-d', '/home/cytu/usr/src/py/ananda/db/ananda_temp.db']
    if ns:
        l.extend(['-n'])
        l.extend(ns)
    popen(l)

def word(n):
    popen(['python', '/home/cytu/usr/src/py/ananda/rev.py', '-n', n, '-d', '/home/cytu/usr/src/py/ananda/db/word.db',])

def drill(ns=None):
    l = ['python', '/home/cytu/usr/src/py/ananda/drill.py',]
    if ns:
        l.extend(['-n'])
        l.extend(ns)
    popen(l)

def null(n):
    pass

class AnandaController(QWidget):

    p_on = '/home/cytu/usr/src/py/ananda/res/img/chronometer.ico'
    p_off = '/home/cytu/usr/src/py/ananda/res/img/player_time.ico'

    def __init__(self, par=None):

        super().__init__(par)
        
        # setup dbus communication
        self.service = AnandaService(self)

        self.signal_handler = DBusSignalHandler(self)
        self.signal_handler.alarmReceived.connect(self.alarm)
        self.signal_handler.scheduleReceived.connect(self.schedule)
        self.signal_handler.showSplashReceived.connect(self.show_splash)

        # setup schedulers
        self.sched = QtScheduler()
        self.sched.start()
        self.sched_splash = QtScheduler()
        self.sched_splash.start()
        self.b_splash = True
        self.update_splash_service(self.b_splash)
        
        # setup system tray
        self.ti = ti = QSystemTrayIcon(self)
        ti.setIcon(QIcon(self.p_on))
        ti.setToolTip('ananda') 
        ti.show()
        ti.activated.connect(self.act)
        self.mn = mn = QMenu(self)
        for i in ['stat', None, 'eye', None, 'refresh', None, 'quit']:
            if i is None:
                mn.addSeparator()
            else:
                setattr(self, f'act_{i}', QAction(i, self))
                a = getattr(self, f'act_{i}')
                a.triggered.connect(getattr(self, i)) 
                mn.addAction(a)        
        ti.setContextMenu(mn)
         
        self.av = QMediaPlayer(self)
        
    def alarm(self, s):
        d = json.loads(s)
        st = d['state']
        ti = self.ti
        if st == st_learn:
            self.play_audio('/home/cytu/usr/src/py/ananda/res/av/learn.mp3')
            ti.setIcon(QIcon(self.p_on))
            
        elif st == st_rest:
            self.play_audio('/home/cytu/usr/src/py/ananda/res/av/rest.mp3')
            ti.setIcon(QIcon(self.p_off))
    
    def schedule(self, s):
        tbl = json.loads(s)
        sc = self.sched
        sc.remove_all_jobs()
        self.close_widgets()

        tic = now(utc=False)
        alarm = self.service.alarm
        for fn, arg, tl, tr in tbl:
            # This order is essential: launch the apps first, and then send the alarm
            sc.add_job(globals()[fn], trigger='date', args=[arg,], run_date=tic)
            # 01/20/25 09:34:35 A small amount of time to ensure the apps get the alarm
            tic = t_add(t_delta(seconds=2), tic)
            toc = t_add(t_delta(minutes=tl), tic)
            sc.add_job(alarm, trigger='date', args=[json.dumps({'state': st_learn, 'interval': (tic, toc)}),], run_date=tic)
            tic = toc
            toc = t_add(t_delta(minutes=tr), tic)
            sc.add_job(alarm, trigger='date', args=[json.dumps({'state': st_rest, 'interval': (tic, toc)}),], run_date=tic)
            tic = toc

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
        self.ti.setToolTip(f"{nr2t(t.seconds)} left {'' if self.b_splash else '[no splash]'}")

    def act(self, i):
        if i == QSystemTrayIcon.Trigger:
            self.mn.exec(QCursor.pos())
    
    def eye(self):
        self.b_splash = not self.b_splash
        self.update_splash_service(self.b_splash)
    
    def refresh(self):
        self.b_splash = True
        self.update_splash_service(self.b_splash)

    def show_splash(self):
        if self.b_splash:
            self.splash = splash()
            self.splash.showFullScreen()
    
    def update_splash_service(self, b_splash=True):
        sc = self.sched_splash
        sc.remove_all_jobs()
        if b_splash:
            sc.add_job(self.service.show_splash, trigger='interval', minutes=10, start_date=t_add(t_delta(minutes=9), now(utc=False)),)

    def close_widgets(self):
        # broadcasting 
        self.sched.add_job(self.service.alarm, trigger='date', args=[json.dumps({'state': st_none, 'interval': None}),],
                misfire_grace_time=2, run_date=now(utc=False))

    def play_audio(self, src):
        av = self.av
        av.setMedia(QMediaContent(QUrl.fromLocalFile(src)))
        av.play()
    
    def stat(self):
        pass

    def quit(self):
        self.close_widgets() 
        
        def f(): 
            self.sched.shutdown(wait=False) 
            self.ti.hide()   # trick to cleanup the icon
            qApp.quit()

        QTimer.singleShot(100, f)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('ananda')
    app.setQuitOnLastWindowClosed(False)
    font = QFont('Microsoft JhengHei')
    font.setPointSize(12)
    app.setFont(font)
    w = AnandaController()
    app.exec()
