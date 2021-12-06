# -*- coding: utf-8 -*-

from books import *

class gelbaum(book):

    def __init__(self):
        super(gelbaum, self).__init__()

        self.src = '/home/cytu/usr/doc/math/ex/Gelbaum B. Problems in Real and Complex Analysis.pdf'
        self.pgs = range(9, 454)
        self.tokens.update({
            'prob_sol': {'class': 'indent0',
                         'ocr': r'^\d+\.\d+\.', 
                        },

            'part': {'class': 'allbx',
                     'ocr': r'^(PROBLEMS|SOLUTIONS)$',
                    },

            'chapter': {'class': 'first2',
                        'ocr': r'^\d+$',
                        },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['prob_sol', 'part']: 
            d['k'] = k
            if tk == 'part':
                if k == 'PROBLEMS':
                    d['q_or_a'] = 'q'
                else:
                    d['q_or_a'] = 'a'
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), sys.maxsize 
