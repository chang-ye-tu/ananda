# -*- coding: utf-8 -*-

from books import *

class falmagne(book):
    
    def __init__(self):
        super(falmagne, self).__init__()
        
        self.pgs = range(17, 374)
        self.morph0 = 'c150.4'

        self.src = "/home/cytu/usr/src/py/ananda/theory/Falmagne J.-C., Doignon J.-P. Learning Spaces.pdf"
        
        self.tokens.update({
            'sec': {'class': 'indent0',      
                    'ocr': r'^\d+\.\d+ ', 
                   },

            'thm': {'class': 'indent0',      
                    'ocr': r'^(\d+\.\d+\.\d+ (Lemma|Corollary|Theorem))', 
                   },
            
            'other': {'class': 'indent0',      
                    'ocr': r'^(\d+\.\d+\.\d+ (Algorithm|Example|Deﬁnition))', 
                   },
            
            'proof': {'class': 'indent0', 
                      'ocr': r'^PROOF',
                     },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof',]:
            if tk == 'thm':
                d['q_or_a'] = 'q'
                d['k'] = k.strip() 
            else:
                d['q_or_a'] = 'a'

        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        chap = self.bxs(bx).line(w=(0.99, 1))
        ml = self.ymax_line(bx, w=(0.14, 0.16))
        return 0 if chap else self.ymin_skip1(bx), min(sort_y(bx)[-2][1], ml) if chap else ml 
