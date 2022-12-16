# -*- coding: utf-8 -*-

from books import *

class shao(book):

    def __init__(self):
        super(shao, self).__init__()

        self.src = '/home/cytu/usr/doc/math/prob/appl/Shao J. Mathematical Statistics 2ed.pdf'
        self.pgs = range(16, 559)
        self.tokens.update({
            'chapter':  {'class': 'top', 
                         'ocr': r'^Chapter (\d+)$',
                        },

            'section':  {'class': 'indent0', 
                         'ocr': r'^(\d+\.\d+(\.\d+)?) ',
                        },
            
            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+))',
                    },

            'example': {'class': 'indent0',      
                        'ocr': r'^(Example (\d+\.\d+))',
                       },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Theorem|Corollary|Proposition) (\d+\.\d+))',
                   },

            'proof': {'class': 'indent0',      
                     'ocr': r'^Proof', 
                     },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        if tk in ['thm', 'proof']:
            if tk == 'thm':
                d['q_or_a'] = 'q'
                d['k'] = k
            else:
                d['q_or_a'] = 'a'
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
