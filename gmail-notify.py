#!/usr/bin/env python3

# caveat: in qt-linux it is not safe to use qpixmap in threads, a naive approach is not feasible -- hence the indirect dbus call.

from base import *
import imaplib

ifc = 'gmail.ctrl'

class dso(dbus.service.Object): 
    
    def __init__(self): 
        dbus.service.Object.__init__(self, 
            dbus.service.BusName(ifc, bus=dbus.SessionBus()), '/')  

    @dbus.service.signal(ifc)
    def check(self):
        pass

user, pwd = 'changye.tu', 'Tu1106,.123' 

def channel(user=user, pwd=pwd):
    try:
        ch = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        ch.login(user, pwd)
    except: 
        ch = None
    return ch

class gmail(QWidget):

    p_on = './res/img/gmail_on.ico'
    p_off = './res/img/gmail_off.ico'

    def __init__(self, par=None):
        super(gmail, self).__init__(par)
        
        self.ch = None
        self.ti = ti = QSystemTrayIcon(self)
        #ti.setIcon(QIcon(self.p_off))
        ti.show()
        
        mn = QMenu(self)
        for i in ['check', 'listen', 'audio', 'quit']:
            setattr(self, 'act_%s' % i, QAction(i, self))
            a = getattr(self, 'act_%s' % i)
            a.triggered.connect(getattr(self, i)) 
            mn.addAction(a)        
        
        ti.setContextMenu(mn)
        ti.activated.connect(self.act)

        self.b_pass, self.b_audio = False, False 
        self.set_tp()

        def f():
            self.login()
            self.dso = dso()
            self.sched = sc = QtScheduler()
            sc.start()
            QTimer.singleShot(1000 * 3, self.dso.check)
            sc.add_job(self.dso.check, trigger='interval', minutes=1)
        # XXX
        f()
        #QTimer.singleShot(1000 * 120, f)
        
        self.av = QMediaPlayer(self)

        dbus.SessionBus().add_signal_receiver(self.check, dbus_interface=ifc, signal_name='check')
         
    def login(self):
        try:
            self.ch = channel()
        except:
            self.ti.showMessage('Login Error', 'Please Check Connection!', QSystemTrayIcon.Critical)
    def quit(self):
        self.ti.hide()  # Trick to cleanup the icon
        qApp.quit()
    
    def listen(self):
        self.b_pass = not self.b_pass
        self.set_tp()

    def audio(self):
        self.b_audio = not self.b_audio
        self.set_tp()
    
    def set_tp(self):
        self.ti.setToolTip('audio:%s [%s]' % ('on' if self.b_audio else 'off', 
                           'idle' if self.b_pass else 'listening')) 
    def act(self, i):
        if i == QSystemTrayIcon.Trigger:
            subprocess.Popen(['google-chrome', 'https://mail.google.com/mail/u/0/?shva=1#all']) 

    def check(self):
        if self.b_pass:
            return
        
        ch = self.ch 
        ti = self.ti

        if ch is None:
            ti.showMessage('Gmail Connection Error', 'Please check your network settings.', QSystemTrayIcon.Critical)
            # try to reconnect after 10 secs
            QTimer.singleShot(1000 * 10, self.login)
            return

        try:
            ch.select('"[Gmail]/All Mail"', readonly=True) 
            r, m = ch.search(None, 'UnSeen')
            msgs = m[0].split()
            n = len(msgs)
            ti.setIcon(QIcon(self.p_on if n else ''))#self.p_off))
            if n:
                ss = '' if n == 1 else 's'
                ti.showMessage('New Mail%s' % ss, "You've got %s new mail%s" % (n, ss))
              
                if self.b_audio:
                    av = self.av
                    av.setMedia(QMediaContent(QUrl.fromLocalFile('/home/cytu/usr/src/py/ananda/res/av/gmail.mp3')))
                    av.play()

        except:
            ti.showMessage('Connection Error', 'Reconnection Needed!', QSystemTrayIcon.Critical)

            # try to reconnect after 2 secs
            QTimer.singleShot(1000 * 2, self.login)

if __name__ == '__main__':
    DBusQtMainLoop(set_as_default=True) 
    
    app = QApplication(sys.argv)
    app.setApplicationName('gmail_notifier')
    app.setFont(QFont('Microsoft JhengHei'))
    app.setQuitOnLastWindowClosed(False)

    g = gmail()
    app.exec_()
