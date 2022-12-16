# -*- coding: utf-8 -*-

from books import *

class kolk(book):
    
    def __init__(self):
        super(kolk, self).__init__()
        
        self.pgs = range(17, 449)
        self.morph0 = 'c150.6'

        self.src = "/home/cytu/usr/doc/math/anly/th/Duistermaat J. J., Kolk J. A. C. Distributions Theory and Applications.pdf"
        
        self.tokens.update({
            'thm': {'class': 'indent0',      
             'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+))', 
                   },
            
            'remark': {'class': 'indent0',      
                    'ocr': r'^(Remark (\d+\.\d+))', 
                   },

            'example': {'class': 'indent0',      
                    'ocr': r'^(Example (\d+\.\d+))', 
                   },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+))', 
                    },
            
            'proof': {'class': 'indent0', 
                      'ocr': r'^(Pr[0oO][0oO]f)',
                     },
            
            'ex': {'class': 'indent0',      
                   'ocr': r'^(\d+\.\d+)\.', 
                  },

            'sol': {'class': 'indent0',      
                    'ocr': r'^(\d+\.\d+) ', 
                   },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'ex', 'sol']:
            if tk in ['thm', 'ex']:
                d['q_or_a'] = 'q' 
                d['k'] = k
            else:
                d['q_or_a'] = 'a'
                if tk in ['sol',]:
                    d['k'] = k
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        return self.ymin_skip1(bx), self.ymax_line(bx, w=(0.3, 0.45)) 
