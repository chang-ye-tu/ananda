# -*- coding: utf-8 -*-

from books import *

class simon_convex(book):
    
    def __init__(self):
        super(simon_convex, self).__init__()
        
        self.pgs = range(12, 298)
        self.morph0 = 'c150.6'

        self.src = "/home/cytu/usr/doc/math/anly/th/Simon/Simon B. Convexity An Analytic Viewpoint.pdf"
        
        self.tokens.update({
            'thm': {'class': 'indent0',      
             'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+))', 
                   },
            
            'remark': {'class': 'indent0',      
                    'ocr': r'^(Remark[s]? )', 
                   },

            'ex': {'class': 'indent0',      
                    'ocr': r'^(Example (\d+\.\d+))', 
                   },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition )', 
                    },
            
            'proof': {'class': 'indent0', 
                      'ocr': r'^(Pr[0oO][0oO]f)',
                     },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof']:
            if tk in ['thm',]:
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
