# -*- coding: utf-8 -*-

from books import *

class amrouche(book):
    
    def __init__(self):
        super(amrouche, self).__init__()
        
        self.pgs = range(2, 40)

        self.src = u"/home/cytu/usr/doc/math/paper/Amrouche C., Bernardi C., Dauge M., Girault V. Vector Potentials in Three-dimensional Non-smooth Domains.pdf"

        self.tokens.update({
            'section': {'class': 'indent0',
                        'ocr': r'^(\d+\.(\d+\.)?)'
                        },

            'def': {'class': 'indent0',
                    'ocr': r'^((Deﬁnition|Notation) (\d+\.\d+))'
 
                   },

            'remark': {'class': 'indent0',      
                       'ocr': r'^(Remark (\d+\.\d+))', 
                      },

            'hyp': {'class': 'indent0',      
                       'ocr': r'^(Hypothesis (\d+\.\d+))', 
                      },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+)\.)', 
                   },
            
            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                      },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof',]:
            if tk == 'thm':
                d['q_or_a'] = 'q'
                d['k'] = k
            else:
                d['q_or_a'] = 'a'
             
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_skip1(bx)
