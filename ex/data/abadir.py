# -*- coding: utf-8 -*-

from books import *

class abadir(book):

    def __init__(self):
        super(abadir, self).__init__()

        self.src = '/home/cytu/usr/doc/math/ex/Abadir K., Magnus J. Matrix Algebra.pdf'
        self.pgs = range(32, 427)
        self.tokens.update({
            'notes':  {'class': 'indent0', 
                       'ocr': r'^Notes$',
                       },

            'section':  {'class': 'centerh', 
                         'ocr': r'^\d+\.\d+',
                         },

            'exercise': {'class': 'indent0',      
                        'ocr': r'\**Exercise (\d+\.\d+)', 
                        },
            
            'solution': {'class': 'indent0',      
                         'ocr': r'^Solution$', 
                         },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['section', 'notes', 'sep']:
            b_skip = True

        else:
            if tk == 'solution':
                d['q_or_a'] = 'a'
            else:
                d['k'] = trim(k)
                d['q_or_a'] = 'q' 
        
        return b_skip, d
