#!/usr/bin/env python3

import sys, logging, webbrowser
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import * 

#os.chdir(os.path.dirname(__file__))
#cat = os.path.join

ip = '192.168.0.105'
port = 8082 
cam_ip = '192.168.0.106'
cam_port = 8081

ico = '/home/cytu/usr/src/py/ananda/res/img/motion_detector.ico'
fname = '/home/cytu/usr/src/py/ananda/tmp/md_log.txt'

logging.basicConfig(filename=fname, format='%(asctime)s %(message)s', level=logging.INFO)

#for i in open(fname, 'rb'):
#    date, time, typ = i.strip().split(' ')
#    hms, ms = time.split(',')
#    # get on-off pairs; note that there exists incomplete on-off pairs
#sys.exit()

#'''<html>
#  <frameset cols="50%,50%">
#    <frame src="http://192.168.0.106:8081">
#    <frame src="http://192.168.0.106:8081">
#  </frameset>
#</html>'''

class socket(QTcpSocket):
    
    msg_socket = pyqtSignal(str)

    def __init__(self, parent=None):
        super(socket, self).__init__(parent)
        self.readyRead.connect(self.readRequest)
        self.disconnected.connect(self.deleteLater)

    def readRequest(self):
        msg = self.read(self.bytesAvailable()).encode('utf-8')
        self.msg_socket.emit(msg)

class receiver(QTcpServer):
    
    msg_receiver = pyqtSignal(str)

    def __init__(self, parent=None):
        super(receiver, self).__init__(parent)
        self.s = {}
        
    def incomingConnection(self, socketId):
        sid = str(socketId)
        self.s[sid] = socket(self)
        self.s[sid].setSocketDescriptor(socketId)
        self.s[sid].msg_socket.connect(self.handler)

    def handler(self, s):
        self.msg_receiver.emit(s)

class indicator(QWidget):

    def __init__(self, par=None):
        super(indicator, self).__init__(par)
        self.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint|Qt.SplashScreen)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFixedSize(80, 40)
        self.timer = self.startTimer(250)
        self.reset(False)

    def timerEvent(self, e):
        if not self.isVisible():
            return
        if self.cnt % 2 == 0:
            self.setStyleSheet('QWidget{background-color: rgb(255, 0, 0);}')   
        else:
            self.setStyleSheet('QWidget{background-color: rgb(0, 0, 0);}')  
        self.cnt += 1
        if self.cnt >= 4:
            self.txt = str(self.cnt / 4)
        self.update()      
    
    def paintEvent(self, e):
        p = QPainter()
        p.begin(self)
        p.setPen(QColor(255, 255, 255))
        p.setFont(QFont('Microsoft JhengHei', 14))
        p.drawText(e.rect(), Qt.AlignCenter, self.txt)      
        p.end()
    
    def reset(self, b_hide=True):
        self.txt = ''
        self.cnt = 0
        if b_hide:
            self.hide()

class motion_detector(QWidget):
    
    pic = ico
    
    def __init__(self, par=None):
        super(motion_detector, self).__init__(par)

        self.ti = ti = QSystemTrayIcon(self)
        ti.setIcon(QIcon(self.pic))
        ti.show()
        
        mn = QMenu(self)
        for i in ['listen', 'quit']:#'audio',]:
            setattr(self, 'act_%s' % i, QAction(i, self))
            a = getattr(self, 'act_%s' % i)
            a.triggered.connect(getattr(self, i)) 
            mn.addAction(a)        
        
        ti.setContextMenu(mn)
        ti.activated.connect(self.act)

        self.b_pass, self.b_audio = False, True 
        self.set_tp()

        self.receiver = receiver(self)
        if not self.receiver.listen(QHostAddress(ip), port):
            QMessageBox.critical(self, 'Building Services Server', 'Failed to start server: %s' % (self.receiver.errorString(), ))
            self.close()
            return
        self.receiver.msg_receiver.connect(self.handler_receiver)
        self.clicked.connect(self.close)

        self.ind = indicator(self)
        g = qApp.desktop().availableGeometry()
        self.ind.move(g.width() / 2, g.height() / 40)

        # XXX optional sound playback
        try:
            self.av = av = wdg_a(self)
            av.hide()

        except:
            pass

    def quit(self):
        self.ti.hide()  # Trick to cleanup the icon
        qApp.quit()
    
    def listen(self):
        self.b_pass = not self.b_pass
        if self.b_pass:
            self.ind.reset()
        self.set_tp()

    def audio(self):
        self.b_audio = not self.b_audio
        self.set_tp()
    
    def set_tp(self):
        self.ti.setToolTip('audio:%s [%s]' % ('on' if self.b_audio else 'off', 'idle' if self.b_pass else 'listening'))

    def act(self, i):
        if i == QSystemTrayIcon.Trigger:
            webbrowser.open('http://%s:%s' % (cam_ip, cam_port))

    def handler_receiver(self, s):
        if self.b_pass:
            return
        if s == 'motion_on':
            self.ind.show()
        elif s == 'motion_off':
            self.ind.reset()
        logging.info(s)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('motion_detector')
    app.setFont(QFont('Microsoft JhengHei'))
    m = motion_detector()
    app.exec_()
