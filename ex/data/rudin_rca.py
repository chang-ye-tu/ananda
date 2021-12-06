# -*- coding: utf-8 -*-

from books import *

class rudin_rca(book):

    def __init__(self):
        super(rudin_rca, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Rudin/Rudin W. Real and Complex Analysis 3ed.djvu' 
        self.pgs = range(19, 409)
        self.morph_sym = 'c12.2'
        self.tokens.update({
            'thm': {'class': 'allbx',      
                    'ocr': r'^((\d+\.\d+) (Theorem|Corollar|Lemma|Proposition))', 
                   },
            
            'proof': {'class': 'allbx',      
                      'ocr': r'^PROOF', 
                     },
            
            'defn': {'class': 'allbx',      
                     'ocr': r'^((\d+\.\d+) Deﬁnition)',
                    },

            'ex': {'class': 'indent0',
                   'ocr': r'^Exercises',
                  },
     })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['thm',]:
            d['q_or_a'] = 'q'
            d['k'] = k
        elif tk in ['proof',]:
            d['q_or_a'] = 'a' 
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx, w=(0.1, 0.2))
