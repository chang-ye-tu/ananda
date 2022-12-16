# -*- coding: utf-8 -*-

from books import *

class kadison_sol(book):

    def __init__(self):
        super(kadison_sol, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Kadison R., Ringrose J. Fundamentals of the Theory of Operator Algebras Volume III Elementary Theory An Exercise Approach.djvu' 
        self.pgs = range(14, 276)
        self.range_indent1 = (0.065, 0.078)
        self.morph0 = 'c80.4'
        self.tokens.update({
            'prob': {'class': 'indent1',      
                     'ocr': r'^\d+\.\d+\.\d+', 
                     },

            'sol': {'class': 'indent1',
                    'ocr': r'^Solution',
                    },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk == 'sol':
            d['q_or_a'] = 'a'
        elif tk == 'prob':
            d['k'] = trim(k)
            d['q_or_a'] = 'q' 
        else:
            b_skip = True

        return b_skip, d
    
    def ym(self, bx):
        return self.ymin_line(bx), sys.maxsize 
