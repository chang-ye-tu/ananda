#!/usr/bin/env python3

# caveat: in qt-linux it is not safe to use qpixmap in threads, a naive approach is not feasible -- hence the indirect dbus call.

from base import *
ifc = 'gmail.ctrl'

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from inspect import getsourcefile
os.chdir(os.path.dirname(os.path.abspath(getsourcefile(lambda:0))))

def get_creds():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    TOKEN = 'res/token.json'
    CREDENTIALS = 'res/credentials.json'

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN, 'w') as token:
            token.write(creds.to_json())
    return creds

class dso(dbus.service.Object): 
    
    def __init__(self): 
        dbus.service.Object.__init__(self, dbus.service.BusName(ifc, bus=dbus.SessionBus()), '/')  

    @dbus.service.signal(ifc)
    def check(self):
        pass

class gmail(QWidget):

    p_on = './res/img/gmail_on.ico'
    p_off = './res/img/gmail_off.ico'

    def __init__(self, par=None):
        super(gmail, self).__init__(par)
        
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

        try:    
            creds = get_creds()
            self.service = build('gmail', 'v1', credentials=creds)

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            ti.showMessage('Error', f'An Error Occurred: {error}\nPlease Check the OAuth 2.0 Credentials !!', QSystemTrayIcon.Critical)

        self.dso = dso()
        self.sched = sc = QtScheduler()
        sc.start()
        sc.add_job(self.dso.check, trigger='interval', seconds=30)

        self.av = QMediaPlayer(self)

        dbus.SessionBus().add_signal_receiver(self.check, dbus_interface=ifc, signal_name='check')
         
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
        self.ti.setToolTip('audio:%s [%s]' % ('on' if self.b_audio else 'off', 'idle' if self.b_pass else 'listening'))

    def act(self, i):
        if i == QSystemTrayIcon.Trigger:
            subprocess.Popen(['google-chrome', 'https://mail.google.com/mail/u/0/?shva=1#all']) 

    def check(self):
        if self.b_pass:
            return
        
        ti = self.ti
        try:
            results = self.service.users().messages().list(userId='me', q='', labelIds=['UNREAD',], includeSpamTrash=False).execute()
            n = results.get('resultSizeEstimate', 0)
            ti.setIcon(QIcon(self.p_on if n else ''))#self.p_off))
            if n:
                ss = '' if n == 1 else 's'
                ti.showMessage('New Mail%s' % ss, "You've got %s new mail%s" % (n, ss))
              
                if self.b_audio:
                    av = self.av
                    av.setMedia(QMediaContent(QUrl.fromLocalFile('/home/cytu/usr/src/py/ananda/res/av/gmail.mp3')))
                    av.play()

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            ti.showMessage('Error', f'An Error Occurred: {error}\nPlease Check the OAuth 2.0 Credentials !!', QSystemTrayIcon.Critical)

if __name__ == '__main__':
    DBusQtMainLoop(set_as_default=True) 
    app = QApplication(sys.argv)
    app.setApplicationName('gmail_notifier')
    font = QFont('Microsoft JhengHei')
    font.setPointSize(12)
    app.setFont(font)
    app.setQuitOnLastWindowClosed(False)
    g = gmail()
    app.exec()
