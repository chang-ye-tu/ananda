import os, sys
from doc import doc_djvu, doc_pdf

# =============================================================================
#
#  recognize 
#    1. page structure/elements
#    2. numbering conventions: part/chapter/section/subsection 
#       most books have redundancies (eg. section 1.3 under chapter 1)
#    3. def/eg/prop/cor/th/proof/note/re/prob/ex/sol region 
#    4. meaningful y range: ym
#    5. parser: tk_action
#
# =============================================================================

zo = 6.00

def span(bx):
    try:
        px, py = [], []
        for b in bx: 
            px.append(b[0])
            px.append(b[0] + b[2])
            py.append(b[1])
            py.append(b[1] + b[-1])
        px, py = sorted(px), sorted(py)
        return (px[0], py[0], px[-1] - px[0], py[-1] - py[0])

    except:
        return None 
    
def lower(bx):
    return [(b[1] + b[-1]) for b in bx]

def sort_y(bx):
    return sorted(bx, key=lambda b: b[1])

def find(k, s):
    if isinstance(s, str):
        return k.find(s) != -1
    elif isinstance(s, list):
        b = False
        for ss in s:
            if k.find(ss) != -1:
                b = True
                break
        return b
    return False
            
def trim(s, b_space=False):
    if not b_space:
        s = s.replace(' ', '')
    i = len(s) - 1
    while s[i] == '.':
        s = s[0:i]
        i -= 1
    return s

def myset(i):
    return set([tuple(b) for b in i])

class bxs(object):
    
    def __init__(self, bx, book):
        self.bx = bx
        self.book = book
        self.x, self.y, self.w, self.h = span(bx)
    
    def allbx(self):
        return self.bx

    def first(self):
        return self.sort_y()[0:1] 

    def first2(self):
        return self.sort_y()[0:2]

    def indent0(self):
        c0, c1 = self.book.range_indent0
        c00, c01 = self.book.range_top
        y = self.y
        return [b for b in self.bx if ((c0 <= (b[0] - self.x) * 1. / self.w < c1) and not ((c00 <= (b[1] * 1. - y) / y < 3 * c01) if y else 0))]  

    def indent1(self):
        c0, c1 = self.book.range_indent1
        return [b for b in self.bx if c0 <= (b[0] - self.x) * 1. / self.w < c1]
    
    def indent0r(self):
        c0, c1 = self.book.range_indent0r
        return [b for b in self.bx if c0 <= (self.x + self.w - b[0] - b[2]) * 1. / self.w < c1]
        
    def centerh(self):            
        c0, c1 = self.book.range_centerh
        w = self.w
        return [b for b in self.bx if (c0 <= (b[0] - self.x + b[2] / 2.) / w < c1) and b[2] <= self.book.w_centerh * w]
        
    def centerv(self): 
        c0, c1 = self.book.range_centerv
        return [b for b in self.bx if c0 <= (b[1] - self.y + b[-1] / 2.) / self.h < c1]
            
    def top(self):
        c0, c1 = self.book.range_top
        y = self.y
        return [b for b in self.bx if c0 <= (b[1] * 1. - y) / y < c1] if y else self.sort_y()[0:1]
                
    def bottom(self):
        c0, c1 = self.book.range_bottom
        h = self.h
        return [b for b in self.bx if c0 <= (self.y + h - b[1] - b[-1]) * 1. / h < c1] if h else self.sort_y()[-1:]

    def line(self, h=None, w=None):
        c0h, c1h = h if h else self.book.range_lineh 
        c0w, c1w = w if w else self.book.range_linew 
        return [b for b in self.bx if (c0h * zo < b[-1] <= c1h * zo) and (c0w * self.w <= b[2] <= c1w * self.w)]

    def sort_y(self):
        return sort_y(self.bx) 
    
    def tiny(self):
        c0, c1 = self.book.range_tinyw
        return [b for b in self.bx if c0 <= (b[2] * 1. / self.w) < c1]
    
    def dots(self):
        return [b for b in self.bx if b[2] * b[-1] < self.book.dot * self.w * self.h]

class book(object):
    
    def __init__(self):
        # replace title in render result?
        self.replace_title = 0 
        # max horizontal centered element width wrt page width
        self.w_centerh = 0.9
        # max blemish area wrt page  
        self.dot = 2e-5
        
        self.nn_corr = (-1, 0, 1, 0)
        self.range_top = (0., 4e-3)
        self.range_bottom = (0., 2e-3)
        self.range_indent0 = (0., 3e-2)
        self.range_indent1 = (3e-2, 6e-2)
        self.range_indent0r = (0., 3e-2)
        self.range_centerh = (0.49, 0.51)
        self.range_centerv = (0.49, 0.51)
        self.range_tinyw = (1e-2, 5e-2)
        self.range_linew = (0.8, 1.0)
        self.range_lineh = (0, 2)
        self.morph0 = 'c150.6' 
        self.morph1 = 'c4.1'
        self.morph_sym = 'c3.1' 
       
        self.src = ''
        self.pgs = []
        self.tokens = {'sep': {}}
        
    def bxs(self, bx):
        return bxs(bx, self)

    def ymin_chap(self, bx):
        bxs = self.bxs(bx)
        chap = list(myset(bxs.top()) & myset(bxs.tiny()))
        return 0 if chap else self.ymin_skip1(bx)
    
    def ymin_skip1(self, bx):
        try:
            y = min(lower(bx))
        
        except:
            y = 0
        
        return y

    def ymin_line(self, bx, w=None):
        try:
            lines = self.bxs(bx).line(w=w)
            y = min(lower(lines)) if lines else min(lower(bx))
        
        except:
            y = 0
        
        return y
    
    def ymax_skip1(self, bx):
        try:
            y = sort_y(bx)[-1][1]
    
        except:
            y = sys.maxsize
        
        return y

    def ymax_r_nr(self, bx):
        i = sys.maxsize
        try:
            bxs = self.bxs(bx)
            nr = list(myset(bxs.indent0r()) & myset(bxs.tiny()))
            y = sort_y(nr)[-1][1] if nr else i 

        except:
            y = i
        
        return y

    def ymax_line(self, bx, w=(0.1, 0.35)):
        i = sys.maxsize
        try:
            bxs = self.bxs(bx)
            foot = list(myset(bxs.line(w=w)) & myset(bxs.indent0()))
            y = sort_y(foot)[-1][1] if foot else i

        except:
            y = i

        return y

    def ym(self, bx):
        return self.ymin_skip1(bx), sys.maxsize

    def sieve(self, bx, y1=0, y2=sys.maxsize, ym=None):
        bb = bx
        try:
            y_min, y_max = ym if ym else self.ym(bx) 
            bb = [b for b in bx if ((y1 if y1 > y_min else y_min) <= b[1] and ((b[1] + b[-1]) <= (y2 if y2 < y_max else y_max)))]

        finally:
            return self.despeckle(bb)

    def doc(self):
        try:
            ext = os.path.splitext(os.path.split(self.src)[1])[1][1:]
            if ext == 'pdf':
                d = doc_pdf()

            elif ext == 'djvu':
                d = doc_djvu()
            
            if d.open(self.src):
               return d
        
        except:
            return None

    def post_func(self, d, l=('chapter',)):
        yd = d['yd']
        tkd = d['tkd']
        for pg in tkd:
            for tk in tkd[pg]:
                if tk[1] in l:
                    y0, y1 = yd[pg]
                    yd[pg] = [0, y1]
 
    def post(self, d):
        pass

    def despeckle(self, bx):
        return [b for b in bx if b[2] > 3 and b[-1] > 3] 
