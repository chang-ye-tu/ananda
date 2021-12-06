# -*- coding: utf-8 -*-

from books import *

class boyd_sol(book):

    def __init__(self):
        super(boyd_sol, self).__init__()

        self.src = '/home/cytu/usr/doc/math/or/Boyd/Boyd S., Vandenberghe L. Convex Optimization Solutions Manual.pdf'

        self.pgs = range(1, 302)

        self.tokens.update({
            'chapter': {'class': 'top', 
                        'ocr': r'^Chapter (\d+)$',
                       },
            
            'ex': {'class': 'allbx',      
                   'ocr': r'^(\d+\.\d+)',
                  },
            
            'ex_cont': {'class': 'allbx',      
                       'ocr': r'^\(\w\)',
                  },
            
            'sol': {'class': 'allbx',
                    'ocr': r'^Solution',
                   },

            'hint': {'class': 'allbx',
                     'ocr': r'^Hint',
                     },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        if tk in ['ex', 'ex_cont', 'sol']:
            if tk == 'ex':
                d['q_or_a'] = 'q'
                d['k'] = k
            elif tk == 'ex_cont':
                d['q_or_a'] = 'q'
            else:
                d['q_or_a'] = 'a'
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_line(bx, w=(0.9, 1.0)), sys.maxsize 

    def post(self, d):
        self.post_func(d)
