# -*- coding: utf-8 -*-
from books import *

class shao_sol(book):

    def __init__(self):
        super(shao_sol, self).__init__()

        self.src = '/home/cytu/usr/doc/math/prob/appl/Shao J. Mathematical Statistics Exercises and Solutions.pdf'
        self.pgs = range(25, 376)
        self.tokens.update({
            'chapter':  {'class': 'top', 
                         'ocr': r'^Chapter (\d+)$',
                        },

            'exercise': {'class': 'indent0',      
                         'ocr': r'Exercise (\d+)', 
                        },
            
            'note': {'class': 'indent0',      
                     'ocr': r'Note\.', 
                     },

            'solution': {'class': 'indent0',      
                         'ocr': r'Solution\.', 
                         },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['chapter', 'note', 'sep']:
            if tk == 'chapter':
                d['root'] = k
            b_skip = True

        else:
            if tk == 'solution':
                d['q_or_a'] = 'a'
            else:
                d['k'] = '.'.join([trim(d['root']), trim(k)])
                d['q_or_a'] = 'q' 
        
        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
