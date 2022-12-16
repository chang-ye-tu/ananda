# -*- coding: utf-8 -*-

from books import *

class lin_pde(book):

    def __init__(self):
        super(lin_pde, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Han Q., Lin F.-H. Elliptic Partial Differential Equations.djvu'
        self.pgs = range(9, 130)
        
        self.tokens.update({
            'chapter':  {'class': 'top', 
                         'ocr': r'^CHAPTER (\d+)$',
                        },

            'section':  {'class': 'centerh', 
                         'ocr': r'^(\d+\.\d+)\. ',
                        },
            
            'thm': {'class': 'indent1',      
                    'ocr': r'^((LEMMA|THEOREM|COROLLARY|PROPOSITION) (\d+\.\d+))\.?',
                   },

            'proof': {'class': 'indent1',      
                     'ocr': r'^PROOF', 
                     },

            'remark': {'class': 'indent1',      
                       'ocr': r'^(REMARK (\d+\.\d+))\.?',
                      },

            'defn': {'class': 'indent1',      
                     'ocr': r'^(DEFINITION (\d+\.\d+))\.?',
                    },

            'example': {'class': 'indent1',      
                        'ocr': r'^(EXAMPLE|APPLICATION)',
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
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.centerh()) & myset(bxs.tiny()))
        return (0 if nr else self.ymin_skip1(bx), sort_y(nr)[-1][1] if nr else self.ymax_line(bx))
