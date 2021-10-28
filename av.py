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

mp3gain = 'mp3gain'
lame = 'lame'
READ_CHUNK = 512
WRITE_CHUNK = 1024 
FORMAT = pyaudio.paInt16
CHANNELS = 2 
RATE = 44100
NOREALNUM = -666.24601
DEFAULT_TARGET = 100

def sha(f):
    return hashlib.sha224(open(f, 'rb').read()).hexdigest()

def adjust_vol(f, target_gain=DEFAULT_TARGET):
    if os.name == 'posix':
        call([mp3gain, '-r', '-c', '-d', '9', '-f', f])    
        return    
    
    p = Popen([mp3gain, '-o', f], bufsize=-1, universal_newlines=True, stdin=PIPE, stdout=PIPE)
    fin = p.stdout
    vl = fin.readlines()[1].strip().split('\t')
    i = mp3_info()
    i.radiodBGain = float(vl[2])
    i.currMaxAmp = float(vl[3])
    i.currMaxGain = int(vl[4])
    i.currMinGain = int(vl[5])
    i.modifydBGain = target_gain - DEFAULT_TARGET
    call([mp3gain, 
          '-g', str(i.radioMp3Gain if i.radioMp3Gain != 0 else 0), 
          '-f', f])

class mp3_info(object):
    '''Class to store MP3 Replay Gain information'''
    def __init__(self):    
        self.reset()
        self._moddB = 0

    def _getCurrMaxAmp(self):
        return self._currMaxAmp

    def _setCurrMaxAmp(self, vData):
        self._currMaxAmp = vData    

    currMaxAmp = property(_getCurrMaxAmp, _setCurrMaxAmp)
   
    def _getCurrMaxGain(self):
        return self._currMaxGain

    def _setCurrMaxGain(self, vData):
        self._currMaxGain = vData   

    currMaxGain = property(_getCurrMaxGain, _setCurrMaxGain)

    def _getCurrMinGain(self):
        return self._currMinGain

    def _setCurrMinGain(self, vData):
        self._currMinGain = vData

    currMinGain = property(_getCurrMinGain, _setCurrMinGain)
    
    def _getAlbumdBGain(self):
        if self._albumdBGain != NOREALNUM:
            return self._albumdBGain + self._moddB
        return self._albumdBGain

    def _setAlbumdBGain(self, vData):
        self._albumdBGain = vData

    albumdBGain = property(_getAlbumdBGain, _setAlbumdBGain)

    def _getModifydBGain(self):
        return self._moddB

    def _setModifydBGain(self, vData):
        self._moddB = vData

    modifydBGain = property(_getModifydBGain, _setModifydBGain)
    
    def _getRadiodBGain(self):
        if self._radiodBGain != NOREALNUM:
            return self._radiodBGain + self._moddB
        return self._radiodBGain

    def _setRadiodBGain(self, vData):
        self._radiodBGain = vData

    radiodBGain = property(_getRadiodBGain, _setRadiodBGain)

    # Read-only properties.

    def _getRawAlbumdBGain(self):
        return self._albumdBGain

    RawAlbumdBGain = property(_getRawAlbumdBGain)

    def _getRawRadiodBGain(self):
        return self._radiodBGain

    RawRadiodBGain = property(_getRawRadiodBGain)

    def _getAlbumMp3Gain(self):
        if self._albumdBGain != NOREALNUM:
            return int(round((self._albumdBGain + self._moddB) / (5 * log(2, 10))))
        return 0
    
    albumMp3Gain = property(_getAlbumMp3Gain)

    def _getRadioMp3Gain(self):
        if self._radiodBGain != NOREALNUM:
            return int(round((self._radiodBGain + self._moddB) / (5 * log(2, 10))))
        return 0
    
    radioMp3Gain = property(_getRadioMp3Gain)

    def _getMaxNoclipMp3Gain(self):
        if (self._currMaxAmp != NOREALNUM) and (self._currMaxAmp < 1000000) and  (self._currMaxAmp > 0) :
            dblAdjust = 4 * log(32767/self._currMaxAmp,2)
            if float(int(dblAdjust)) > dblAdjust:
                return int(dblAdjust) - 1
            return int(dblAdjust)
        return 0

    maxNoclipMp3Gain = property(_getMaxNoclipMp3Gain)   

    def alterDb(self, vData):    
        if self._radiodBGain != NOREALNUM:
            self._radiodBGain += vData
        if self._albumdBGain != NOREALNUM:
            self._albumdBGain += vData
    
        intGainChange = int(-vData / (5 * log(2, 10)))
        if self._currMaxAmp != NOREALNUM:
            self._currMaxAmp *= 2 ** (intGainChange / 4)
        if self._currMaxGain != -1:
            self._currMaxGain += intGainChange
        if self._currMinGain != -1:
            self._currMinGain += intGainChange
    
    def reset(self):
        self._radiodBGain = NOREALNUM
        self._albumdBGain = NOREALNUM
        self._currMaxAmp = NOREALNUM
        self._currMaxGain = -1
        self._currMinGain = -1

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
        all = []
        p = pyaudio.PyAudio()

        if os.name == 'posix':
            # manually assign input_device_index of /dev/dsp1, USB sound card
            # http://n2.nabble.com/New-script-for-recording-screencasts-on-Ubuntu-9-04-td3081264.html
            
            ix = 0
            for i in range(p.get_device_count()):
                if p.get_device_info_by_index(i)['name'] == '/dev/dsp1':
                    ix = i 
                    break
            
            stream = p.open(format=FORMAT, 
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            input_device_index=ix,
                            frames_per_buffer=WRITE_CHUNK)        
        
        else:
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=WRITE_CHUNK)
        
        def cleanup():
            stream.close()
            p.terminate()
        
        self.send(cnd='rec_start')

        while not self.is_stopped():	   
            data = stream.read(WRITE_CHUNK)
            all.append(data) 
        
        cleanup()

        # write data to wav.
        data = ''.join(all)
        ff = cat(self.td, 'rec')
        f = '%s.wav' % ff        
        f_ = '%s.mp3' % ff

        wf = wave.open(f, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()
        
        # wav -> mp3 -> mp3gain.
        call([lame, '-h', f, f_])
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
