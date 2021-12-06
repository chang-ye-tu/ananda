# -*- coding: utf-8 -*-

from books import *

class zuily(book):

    def __init__(self):
        super(zuily, self).__init__()

        self.tokens.update({
            'exercise': {'class': 'indent0',      
                         'ocr': r'^Exercise (\d+)',
                        },

            'solution': {'class': 'indent0',      
                         'ocr': r'^Solution (\d+)', 
                         },

            'bar': {'class': 'line',},
        })

        self.src = '/home/cytu/usr/doc/math/anly/th/Zuily C. Problems in Distributions and Partial Differential Equations.pdf'

        self.pgs = range(5, 224)

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_skip1(bx)

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['bar', 'sep',]:
            b_skip = True

        else:
            d['k'] = trim(k)
            d['q_or_a'] = 'q' if tk == 'exercise' else 'a'
        
        return b_skip, d

    def post(self, dd):
        self.post_func(dd)
