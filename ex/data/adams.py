# -*- coding: utf-8 -*-
from books import *

class adams(book):
    
    def __init__(self):
        super(adams, self).__init__()
        
        self.pgs = range(15, 310)
        self.src = "/home/cytu/usr/doc/math/anly/th/Adams R., Fournier J. Sobolev Spaces 2ed.djvu"
        self.tokens.update({
            'essay': {'class': 'indent0',
                      'ocr': r'^(\d+\.\d+) ',
                      },
            
            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                       },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk == 'essay':
            d['q_or_a'] = 'q'
            d['k'] = k
        
        elif tk == 'proof':
            d['q_or_a'] = 'a'

        else:
            b_skip = True
        
        return b_skip, d

    def ym(self, bx):
        import sys
        return self.ymin_line(bx), sys.maxsize 
