import os, sys, wave, hashlib
from subprocess import call, Popen, PIPE
from math import log

os.chdir(os.path.dirname(__file__))
cat = os.path.join

from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

from ui.wdg_v import Ui_wdg_v
from ui.wdg_a import Ui_wdg_a

import pyaudio 

CHUNK = 1024 
FORMAT = pyaudio.paInt16
RATE = 44100
NOREALNUM = -666.24601

def sha(f):
    return hashlib.sha224(open(f, 'rb').read()).hexdigest()

def adjust_vol(f):
    exe = 'mp3gain'
    p = Popen([exe, '-o', f], bufsize=-1, universal_newlines=True, stdin=PIPE, stdout=PIPE)
    vl = p.stdout.readlines()[1].strip().split('\t')
    call([exe, '-g', str(vl[2]), '-f', f])

class thread(QThread):

    def __init__(self, par=None):
        super(thread, self).__init__(par)
        self.stopped = False
        self.mtx = QMutex()
    
    def stop(self):
        try:
            self.mtx.lock()
            self.stopped = True
        finally:
            self.mtx.unlock()

    def is_stopped(self):
        try:
            self.mtx.lock()
            return self.stopped
        finally:
            self.mtx.unlock()

    def run(self):
        self.stopped = False
        self.process()
        self.stop()

    def process(self):
        pass
 
class recorder(thread):
    
    msg_rec = pyqtSignal(dict)

    def __init__(self, td, par=None):
        super(recorder, self).__init__(par)
        self.td = td

    def process(self):
        all_data = []
        p = pyaudio.PyAudio()
        
        channels = 2
        rate = RATE
        if os.name == 'posix':
            ix = 0 
            for i in range(p.get_device_count()):
                info = p.get_device_info_by_index(i)
                # XXX select Sennheiser USB headset 
                if 'Sennheiser USB headset' in info.get('name', ''):
                    channels = info.get('maxInputChannels', 2)
                    # XXX not 44100 but 48000, very strange! 
                    rate = 48000 #int(info.get('defaultSampleRate', RATE))
                    ix = i 
                    break
            
            stream = p.open(format=FORMAT, 
                            channels=channels,
                            rate=rate,
                            input=True,
                            input_device_index=ix,
                            frames_per_buffer=CHUNK)        
        
        else:
            stream = p.open(format=FORMAT,
                            channels=channels,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
        
        def cleanup():
            stream.close()
            p.terminate()
        
        self.send(cnd='rec_start')

        while not self.is_stopped():	   
            data = stream.read(CHUNK, exception_on_overflow=False)
            all_data.append(data) 
        
        cleanup()

        # write data to wav.
        ff = cat(self.td, 'rec')
        f = '%s.wav' % ff        
        f_ = '%s.mp3' % ff

        wf = wave.open(f, 'wb')
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setnchannels(channels)
        wf.setframerate(rate)
        wf.writeframes(b''.join(all_data))
        wf.close()
        
        # wav -> mp3 -> mp3gain.
        call(['lame', '-h', f, f_])
        adjust_vol(f_)

        fn = cat(self.td, sha(f_))
        os.rename(f_, fn)
        self.send(cnd='rec_stop', f=fn)
    
    def send(self, **d):
        self.msg_rec.emit(d)

class av(QWidget):
    
    msg_av = pyqtSignal(dict)

    def __init__(self, par=None):
        super(av, self).__init__(par)
        self.td = getattr(par, 'td', '')

    def setup(self):
        self.mp = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mp.stateChanged.connect(self.state_changed)
        self.mp.positionChanged.connect(self.position_changed)
        self.mp.durationChanged.connect(self.duration_changed)

        self.sld.sliderMoved.connect(self.set_position)

        self.rc = recorder(self.td)        
        self.rc.msg_rec.connect(self.handler_rec)

        self.msg_av.connect(self.handler_av)
        self.show_play = True
        
        for i in ['play', 'stop', 'rec', 'file']:
            getattr(self, 'btn_%s' % i).clicked.connect(getattr(self, ('_' if i == 'play' else '') + i))

    def _play(self):
        if self.show_play:
            self.play()
        else:
            self.pause()

    def play(self):
        self.mp.play()

    def pause(self):
        self.mp.pause()

    def stop(self):
        self.mp.stop()

    def file(self):
        f, _ = QFileDialog.getOpenFileName(self, "Open File")
        if f:
            self.set_src(f)

    def rec(self):
        r = self.rc
        if r.isRunning():
            r.stop()
            r.wait()

        else:
            self.stop()
            r.start()

    def send(self, **d):
        self.msg_av.emit(d)

    def state_changed(self, s):
        self.tick(s)
    
    def set_position(self, s):
        self.mp.setPosition(s)
        self.tick(s)
    
    def position_changed(self, s):
        self.sld.setValue(s)
        self.tick(s)

    def duration_changed(self, s):
        self.sld.setRange(0, s) 
        self.tick(s)
        
    def handler_rec(self, d):
        c = d.get('cnd', '')
        if not c:
            return

        if c == 'rec_start':
            self.send(cnd='rec_start')
       
        elif c == 'rec_stop':
            f = d.get('f', '')
            self.set_src(f)
            self.send(cnd='rec_stop', f=f)
            self.play()

    def handler_av(self, d):
        c = d.get('cnd', '')
        if not c:
            return
       
        bn = self.btn_play
        if c == 'playing':
            bn.setIcon(QIcon(':/res/img/media_playback_pause.png')) 
            self.show_play = False
        
        elif c == 'paused':
            bn.setIcon(QIcon(':/res/img/media_playback_start.png')) 
            self.show_play = True

        elif c == 'stopped':
            bn.setIcon(QIcon(':/res/img/media_playback_start.png')) 
            self.show_play = True
        
    def set_src(self, f):
        self.mp.setMedia(QMediaContent(QUrl.fromLocalFile(f)))
    
    def time_s(self, t):
        return QTime((t // 3600000) % 24, (t // 60000) % 60, (t // 1000) % 60).toString('hh:mm:ss')
    
    def tick(self, t):
        self.lbl_t.setText(self.time_s(t))

    def time_info(self):
        m = self.mp
        ts = self.time_s
        return {'duration': ts(m.duration()), 
                'position': ts(m.position()), 
                'remaining': ts(m.duration() - m.position())}

    def closeEvent(self, e):
        self.stop()
        for i in [self.rc,]:
            i.stop()
            i.wait()

# ==============================================================================
#  gui 
# ==============================================================================

class wdg_a(av, Ui_wdg_a):

    def __init__(self, par=None):
        av.__init__(self, par)
        self.setupUi(self)
        self.setup()

class wdg_v(av, Ui_wdg_v):

    def __init__(self, par=None):
        av.__init__(self, par)
        self.setupUi(self)    
        self.setup()
        self.mp.setVideoOutput(self.vw)
       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('player')
    w = wdg_a()
    w.show()
    app.exec_()
