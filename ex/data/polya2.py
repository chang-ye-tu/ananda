# -*- coding: utf-8 -*-

from books import *
from polya1 import polya1

class polya2(polya1):
    
    def __init__(self):
        super(polya2, self).__init__()
        
        self.src = u'/home/cytu/usr/doc/math/ex/Pólya G., Szegö G. Problems and Theorems in Analysis II Theory of Functions Zeros Polynomials Determinants Number Theory Geometry.pdf'
        self.pgs = range(13, 393)
        self.tokens.update({
            'chapter':  {'class': 'indent0', 
                         'ocr': r'Chapter (\d+)',
                         },

            'section':  {'class': 'indent0', 
                         'ocr': r'§([\.\d ]+)',
                         },
            })
