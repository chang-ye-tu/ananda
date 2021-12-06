from base import *
from ui.wdg_tm import Ui_wdg_tm

st_on, st_pause, st_off = range(3)
m_once, m_cycle = range(2)

class mysplash(splash):

    def __init__(self, par=None, cnt=10):
        splash.__init__(self, par, cnt, css='QLabel{background-color: rgb(200, 0, 0); color: rgb(255, 255, 255); font: 32pt "Microsoft JhengHei";}')
    
    def display(self):
        if self.cnt:
            if self.show_txt:
                self.setText('Alarm !!!  %s Left' % nr2t(self.cnt))
            self.cnt -= 1
        else:
            self.close()
            
    def closeEvent(self, e):
        set_audio(audio_ear, 2**15)

class wdg_tm(QWidget, Ui_wdg_tm):

    def __init__(self, par=None):
        QWidget.__init__(self, par)
        self.setupUi(self)
        self.setStyleSheet('QLabel{background-color: rgb(0, 0, 0); color: rgb(0, 200, 0); font: 20pt "Microsoft JhengHei";}')       
        self.setFixedSize(260, 85)

        for s, i in [('30 seconds', 30),
                     ('100 seconds', 100),
                     ('1 minute',  60),
                     ('5 minutes', 300),
                     ('7 minutes', 420),
                     ('8 minutes', 480),
                     ('10 minutes', 600),
                     ('15 minutes', 900),
                     ('30 minutes', 1800),
                     ('1 hour', 3600),]:
            self.cbo.addItem(s, QVariant(i))

        n = self.n()
        self.cbo.setCurrentIndex(sts.value('{}/index'.format(n), type=int))
        self.ted.setTime(sts.value('%s/ted' % n, type=QTime))
        self.move(sts.value('%s/pos' % n, type=QPoint))

        self.update_cnts()
        
        # XXX set minimum 0 seconds
        #self.ted.setMinimumTime(QTime(0, 0, 0))

        self.state = st_off
        self.mode = sts.value('%s/mode' % n, type=int)
 
        self.tm = QTimer(self)
        self.tm.timeout.connect(self.tick)

        self.cbo.activated.connect(self.update_cnts)
        self.ted.editingFinished.connect(self.update_cnts_ed) 
                
        for i, k in [('play', ('F5',)),
                     ('stop', ('Esc', 'Ctrl+Q',)), 
                    ]:

            n = 'act_%s' % i
            setattr(self, n, QAction(self))
            a = getattr(self, n)
            f = getattr(self, i)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            a.triggered.connect(f)
            getattr(self, 'btn_%s' % i).clicked.connect(f)
            self.addAction(a)

        self.av = QMediaPlayer(self)
        
    def update_cnts(self):
        i = self.cbo.currentIndex()
        self.cnt_s = int(self.cbo.itemData(i)) 
        self.cnt = self.cnt_s
        self.show_cnt()
        sts.setValue('%s/index' % self.n(), QVariant(i))

    def update_cnts_ed(self):
        t = self.ted.time()
        self.cnt_s = t.hour() * 3600 + t.minute() * 60 + t.second()  
        if self.cnt_s:
            self.cnt = self.cnt_s
            self.show_cnt()
            sts.setValue('%s/ted' % self.n(), QVariant(t))

    def play(self):
        if self.state == st_off or self.state == st_pause:
            if self.state == st_off:
                self.cnt = self.cnt_s 
            self.show_cnt()
            self.tm.start(1000)
            self.state = st_on
            self.btn_play.setIcon(QIcon(':/res/img/media_playback_pause.png'))

        elif self.state == st_on:
            self.tm.stop()
            self.state = st_pause
            self.btn_play.setIcon(QIcon(':/res/img/media_playback_start.png'))
       
        for w in [self.cbo, self.ted]:
            w.setEnabled(False)
        
    def stop(self):
        self.tm.stop()
        self.btn_play.setIcon(QIcon(':/res/img/media_playback_start.png'))
        self.show_cnt()
        self.state = st_off
    
        self.cnt = self.cnt_s 
        self.show_cnt()
        for w in [self.cbo, self.ted]:
            w.setEnabled(True)

    def show_cnt(self):
        self.lbl.setText(nr2t(self.cnt))

    def tick(self):
        if self.cnt > 1:
            self.cnt -= 1

        else:
            m = self.mode
            set_audio(audio_pc, 2**15)
            if m == m_once:
                self.play_audio('/home/cytu/usr/src/py/ananda/res/av/alarm.mp3')
                self.splash = mysplash() 
                self.splash.showFullScreen()
                self.stop()

            elif m == m_cycle:
                self.play_audio('/home/cytu/usr/src/py/ananda/res/av/alarm_orig.mp3')
                self.splash = mysplash(cnt=2) 
                self.splash.showFullScreen()
                self.cnt = self.cnt_s

        self.show_cnt()
    
    def play_audio(self, s):
        av = self.av
        av.setMedia(QMediaContent(QUrl.fromLocalFile(s)))
        av.play()
    
    def n(self):
        return self.__class__.__name__
    
    def closeEvent(self, e):
        sts.setValue('%s/mode' % self.n(), QVariant(self.mode))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('alarm')
    app.setFont(QFont('Microsoft JhengHei'))
    w = wdg_tm()
    w.show()
    app.exec_()
