# -*- coding: utf-8 -*-

from books import *

class mazya(book):
    
    def __init__(self):
        super(mazya, self).__init__()
        
        self.pgs = range(28, 820)
        self.morph0 = 'c150.6'

        self.src = "/home/cytu/usr/doc/math/anly/th/Maz'ya/Maz'ya V. Sobolev Spaces With Applications to Elliptic Partial Differential Equations 2ed.pdf"
        
        self.tokens.update({
            'sec': {'class': 'indent0',      
                    'ocr': r'^(\d+\.\d+(\.\d+)?)', 
                   },

            'thm': {'class': 'indent1',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition)( \d+)?)', 
                   },
            
            'remark': {'class': 'indent1',      
                    'ocr': r'^(Remark( \d+)?)', 
                   },

            'ex': {'class': 'indent1',      
                   'ocr': r'^(Example( \d+)?)', 
                   },

            'defn': {'class': 'indent1',      
                     'ocr': r'^(Deﬁnition( \d+)?)', 
                    },
            
            'proof': {'class': 'indent1', 
                      'ocr': r'^Proof',
                     },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'ex', 'proof',]:
            if tk in ['thm', 'ex']:
                d['q_or_a'] = 'q'
                d['k'] = d['sec'] + ' ' + k.strip()
            else:
                d['q_or_a'] = 'a'

        else:
            if tk == 'sec':
                d['sec'] = k
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        chap = self.bxs(bx).line(w=(0.99, 1))
        ml = self.ymax_line(bx, w=(0.14, 0.16))
        return 0 if chap else self.ymin_skip1(bx), min(sort_y(bx)[-3][1], ml) if chap else ml 
