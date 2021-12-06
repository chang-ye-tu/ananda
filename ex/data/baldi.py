# -*- coding: utf-8 -*-

from books import *

class baldi(book):

    def __init__(self):
        super(baldi, self).__init__()

        self.src = '/home/cytu/usr/doc/math/prob/th/Baldi P., Mazliak L., Priouret P. Martingales and Markov Chains Solved Exercises and Elements of Theory.djvu'

        self.pgs = range(8, 195)
        self.tokens.update({
            'ex': {'class': 'indent0',      
                   'ocr': r'^((Problem|Exercise) \d+\.\d+)',
                  },

            'sol': {'class': 'indent0',      
                    'ocr': r'^((P|E)\d+\.\d+)', 
                   },

            'chap': {'class': 'first2',      
                     'ocr': r'^CHAPTER (\d+)',
                    },            
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['sep', 'chap']:
            b_skip = True

        else:
            d['k'] = trim(k).replace('Problem', 'P').replace('Exercise', 'E').replace(' ', '')
            d['q_or_a'] = 'q' if tk == 'ex' else 'a'
        
        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), sys.maxsize 
