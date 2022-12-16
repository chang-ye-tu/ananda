# -*- coding: utf-8 -*-

from books import *

class rudin_fa(book):

    def __init__(self):
        super(rudin_fa, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Rudin/Rudin W. Functional Analysis 2ed.djvu' 
        self.pgs = range(21, 404)
        self.range_indent1 = (6e-2, 9e-2)
        self.morph_sym = 'c12.2'
        self.tokens.update({
            'thm': {'class': 'indent0',      
                    'ocr': r'^((\d+\.\d+) (Theorem|Corollar|Lemma))', 
                   },
            
            'proof': {'class': 'indent1',      
                      'ocr': r'^PROOF\.', 
                     },
            
            'defn': {'class': 'indent0',      
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
