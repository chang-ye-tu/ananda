import sys 

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from ui.wdg_tm import Ui_wdg_tm

sts = QSettings('/home/cytu/usr/src/py/ananda/res/ananda.ini', QSettings.IniFormat)
st_on, st_pause, st_off = range(3)
m_once, m_cycle = range(2)

def nr2t(nr):
    try:
        mm, ss = divmod(nr, 60)
        hh, mm = divmod(mm, 60)
        return f'{hh:02d}:{mm:02d}:{ss:02d}'
    except:
        return '00:00:00'

class splash(QLabel):

    def __init__(self, par=None, cnt=10, show_txt=True, pix=None, css='QLabel{background-color: rgb(200, 0, 0); color: rgb(255, 255, 255); font: 32pt "Microsoft JhengHei";}'):
        super(splash, self).__init__(par)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(css)   
        
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

    def display(self):
        if self.cnt:
            if self.show_txt:
                self.setText(f'Alarm !!! {nr2t(self.cnt)} Left')
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

class wdg_tm(QWidget, Ui_wdg_tm):

    def __init__(self, par=None):
        QWidget.__init__(self, par)
        self.setupUi(self)
        self.setStyleSheet('QLabel{background-color: rgb(0, 0, 0); color: rgb(0, 200, 0); font: 20pt "Microsoft JhengHei";}')       
        self.setFixedSize(260, 85)

        for s, i in [('30 seconds', 30),
                     ('1 minute',  60),
                     ('3 minute',  180),
                     ('5 minutes', 300),
                     ('7 minutes', 420),
                     ('9 minutes', 540),
                     ('11 minutes', 660),
                     ('15 minutes', 900),
                     ('30 minutes', 1800),
                     ('1 hour', 3600),]:
            self.cbo.addItem(s, QVariant(i))

        n = self.n()
        self.cbo.setCurrentIndex(sts.value(f'{n}/index', type=int))
        self.ted.setTime(sts.value(f'{n}/ted', type=QTime))
        self.move(sts.value(f'{n}/pos', type=QPoint))

        self.update_cnts()
        
        self.state = st_off
        self.mode = sts.value(f'{n}/mode', type=int)
 
        self.tm = QTimer(self)
        self.tm.timeout.connect(self.tick)

        self.cbo.activated.connect(self.update_cnts)
        self.ted.editingFinished.connect(self.update_cnts_ed) 
                
        for i, k in [('play', ('F5',)),
                     ('stop', ('Esc', 'Ctrl+Q',)), 
                    ]:

            n = f'act_{i}'
            setattr(self, n, QAction(self))
            a = getattr(self, n)
            f = getattr(self, i)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            a.triggered.connect(f)
            getattr(self, f'btn_{i}').clicked.connect(f)
            self.addAction(a)

        self.av = QMediaPlayer(self)
        
    def update_cnts(self):
        i = self.cbo.currentIndex()
        self.cnt_s = int(self.cbo.itemData(i)) 
        self.cnt = self.cnt_s
        self.show_cnt()
        sts.setValue(f'{self.n()}/index', QVariant(i))

    def update_cnts_ed(self):
        t = self.ted.time()
        self.cnt_s = t.hour() * 3600 + t.minute() * 60 + t.second()  
        if self.cnt_s:
            self.cnt = self.cnt_s
            self.show_cnt()
            sts.setValue(f'{self.n()}/ted', QVariant(t))

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
            if m == m_once:
                self.play_audio('/home/cytu/usr/src/py/ananda/res/av/alarm.mp3')
                self.splash = splash() 
                self.splash.showFullScreen()
                self.stop()

            elif m == m_cycle:
                self.play_audio('/home/cytu/usr/src/py/ananda/res/av/alarm_orig.mp3')
                self.splash = splash(cnt=2) 
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
        sts.setValue(f'{self.n()}/mode', QVariant(self.mode))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('alarm')
    app.setFont(QFont('Microsoft JhengHei'))
    w = wdg_tm()
    w.show()
    app.exec()
