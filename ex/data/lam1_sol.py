# -*- coding: utf-8 -*-

from books import *

class lam1_sol(book):
    
    def __init__(self):
        super(lam1_sol, self).__init__()

        self.src = "/home/cytu/usr/doc/math/alg/Lam/Lam T.-Y. Exercises in Classical Ring Theory 2ed.pdf"
        self.pgs = range(21, 369)

        self.morph0 = 'c100.6'

        self.tokens.update({
            'chapter':  {'class': 'indent0',
                         'ocr' : r'^Chapter \d+$',
                         },

            'ex_start': {'class': 'indent0',
                         'ocr': r'^Exercises for §\d+',
                        },

            'ex': {'class': 'indent0',
                   'ocr': '^EX\. (\d+\.\d+[A-Z*]?)\. ',
                   },

            'sol':  {'class': 'indent0', 
                     'ocr': r'^Solution',
                      },

            'comment': {'class': 'indent0',
                        'ocr': r'^Comment',
                       },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['ex', 'sol']:
            if tk == 'ex':
                d['q_or_a'] = 'q'
                d['k'] = trim(k)
            else:
                d['q_or_a'] = 'a'

        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
