# -*- coding: utf-8 -*-

from books import *

class lam1(book):
    
    def __init__(self):
        super(lam1, self).__init__()

        self.src = "/home/cytu/usr/doc/math/alg/Lam/Lam T.-Y. A First Course in Noncommutative Rings 2ed.djvu"
        self.pgs = range(18, 390)

        self.morph0 = 'c100.5'

        self.tokens.update({
            'chapter':  {'class': 'top',
                         'ocr' : r'^CHAPTER \d+$',
                         },
            
            'section':  {'class': 'indent0', 
                         'ocr': r'^§(\d+\.) ',
                        },

            'thm': {'class': 'indent0', 
                     'ocr': r'^((\(\d+\.\d+\)) (Proposition|Theorem|Corollary|Lemma))',
                    },
            
            'defn': {'class': 'indent0', 
                     'ocr': r'^((\(\d+\.\d+\)) Deﬁnition)',
                    },

            'remark': {'class': 'indent0', 
                       'ocr': r'^((\(\d+\.\d+\))? Remark)',
                       },
            
            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                      },

            'ex_start': {'class': 'indent0',
                         'ocr': r'^Exercises for §',
                        },

        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['thm', 'proof']: 
            if tk == 'proof':
                d['q_or_a'] = 'a'
            else:
                d['k'] = trim(k)
                d['q_or_a'] = 'q'

        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
