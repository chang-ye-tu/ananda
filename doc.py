import re, hashlib

from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from djvu.decode import *
from djvu.sexpr import *
from popplerqt5 import Poppler
from PIL import Image
from PIL.ImageQt import ImageQt

def sha(f):
    return hashlib.sha224(open(f, 'rb').read()).hexdigest()

# ==============================================================================
# doc backends
# ==============================================================================

# open, set_pg, set_z, fst, last, next, prev  

class doc(QWidget):
    
    msg_doc = pyqtSignal(dict)

    def __init__(self, par=None):
        QLabel.__init__(self, par)
        
        self.f = ''
        self.sha = ''
        self.pgs = 0
        self.pg = 0 
        self.z = 1.0
        self.pix = None

    def send(self, **d):
        self.msg_doc.emit(d)
    
    def n(self):
        return self.__class__.__name__

    def render(self, n, z=0):
        return None

    def render_path(self, n, p, z=0):
        try:
            i = self.render(n, z)
            return i.copy(self.matrix(n, z).mapRect(QRectF(*p).toRect()))
        except:
            return QImage()

    def matrix(self, n=0, z=0):
        return None

    def set_pg(self, n, render=True):
        is_changed = False
        if self.pg != n and 0 <= n < self.pgs:
            self.send(cnd='before_page_changed')
            self.pg = n
            is_changed = True

        im = self.render(self.pg) 
        if im is None:
            print('pp. %s not available by this moment ...' % (self.pg + 1))
        
        else:
            if render:
                self.pix = QPixmap.fromImage(im)
            if is_changed:
                self.send(cnd='page_changed', n=n)        
     
    def set_z(self, n, render=True):
        if self.z != n and n > 0:
            self.send(cnd='before_zoom_changed')
            self.z = n
            self.set_pg(self.pg, render)
            self.send(cnd='zoom_changed', n=n)

    def zoom(self, n):
        self.set_z(self.z * n)
    
    def fst(self):
        self.set_pg(0)

    def last(self):        
        self.set_pg(self.pgs - 1)
    
    def next(self):
        self.set_pg(self.pg + 1)

    def prev(self):
        self.set_pg(self.pg - 1)
    
class doc_djvu(doc):

    def __init__(self, par=None):
        doc.__init__(self, par)
    
    def open(self, f, render=True):       
        self.src = None
        try:
            self.src = Context().new_document(FileUri(f))
            self.src.get_message()
            self.f = f
            self.sha = sha(f)
            self.pgs = len(self.src.pages)
            self.pg = -1
            #self.set_pg(0, render)
            return True

        except:
            return False

    def matrix(self, n, z=0):
        pg = self.src.pages[n]
        dpi = pg.dpi
        z = z if z else self.z
        return QTransform(z * self.physicalDpiX() / dpi, 0, 0, z * self.physicalDpiY() / dpi, 0, 0)     
    
    def render(self, n, z=0):
        try:            
            pg = self.src.pages[n]
            job = pg.decode()
            dpi = pg.dpi
            z = z if z else self.z
            r = (0, 0, int(z * self.physicalDpiX() * pg.width / dpi), int(z * self.physicalDpiY() * pg.height / dpi))
            im = Image.frombytes('RGB', r[2:], job.render(RENDER_COLOR, r, r, PixelFormatRgb()))
            return ImageQt(im).mirrored()

        except:
            return None

    def dpi(self, n):
        try:
            return self.src.pages[n].dpi
        except:
            return 0
    
class doc_pdf(doc):

    def __init__(self, par=None):
        doc.__init__(self, par)

    def open(self, f, render=True):
        self.src = None
        
        try:
            self.src = Poppler.Document.load(f)
            self.src.setRenderHint(Poppler.Document.Antialiasing)
            self.src.setRenderHint(Poppler.Document.TextAntialiasing)
            self.f = f
            self.sha = sha(f)
            self.pgs = self.src.numPages()
            self.pg = -1
            #self.set_pg(0, render)
            return True
        
        except:
            return False

    def matrix(self, n=0, z=0):
        z = z if z else self.z
        return QTransform(z * self.physicalDpiX() / 72., 0, 0, z * self.physicalDpiY() / 72., 0, 0)
    
    def render(self, n, z=0):
        try:
            z = z if z else self.z
            pg = self.src.page(n)
            im = pg.renderToImage(z * self.physicalDpiX(), z * self.physicalDpiY())
            return im

        except:
            return None

    def dpi(self, n):
        return 72
