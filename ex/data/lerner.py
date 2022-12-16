# -*- coding: utf-8 -*-

from books import *

class lerner(book):
    
    def __init__(self):
        super(lerner, self).__init__()
        
        self.pgs = range(19, 493)
        self.morph0 = 'c150.6'

        self.src = "/home/cytu/usr/doc/math/anly/th/Lerner N. A Course on Integration Theory.pdf"
        
        self.tokens.update({
            'chap': {'class': 'top',      
                    'ocr': r'^(Chapter \d+)', 
                    },

            'sec': {'class': 'indent0',      
                    'ocr': r'^(\d+\.\d+) ', 
                   },

            'thm': {'class': 'indent0',      
             'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+\.\d+))', 
                   },
            
            'remark': {'class': 'indent0',      
                    'ocr': r'^(Remark (\d+\.\d+\.\d+)|N.B.)', 
                   },
            'ex': {'class': 'indent0',      
                    'ocr': r'^(Exercise (\d+\.\d+\.\d+))', 
                   },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+\.\d+))', 
                    },
            
            'proof': {'class': 'indent0', 
                      'ocr': r'^(Proof|Answer)',
                     },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'ex']:
            if tk in ['thm', 'ex']:
                d['q_or_a'] = 'q'
                d['k'] = k.strip()
            else:
                d['q_or_a'] = 'a'

        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        return self.ymin_skip1(bx), self.ymax_line(bx, w=(0.35, 0.45)) 
