# -*- coding: utf-8 -*-
from books import *

class totik(book):

    def __init__(self):
        super(totik, self).__init__()

        self.src = '/home/cytu/usr/doc/math/ex/Komjath P., Totik V. Problems and Theorems in Classical Set Theory.pdf'
        self.pgs = range(13, 504)
        
        self.range_linew = (0.9, 1)

        self.replace_title = 1
        self.morph1 = 'c6.2'
        self.tokens.update({
            'problems': {'class': 'first2',      
                         'ocr': r'^Part I$',},
            
            'solutions': {'class': 'first2',      
                          'ocr': r'^Part II$',},

            'appendix': {'class': 'first2',      
                          'ocr': r'^Part III$',},

            'chapter': {'class': 'first2',      
                        'ocr': r'^(\d+)$',},
            
            'prob_sol': {'class': 'allbx', 
                         'ocr': r'^(\d+)\. ',}, # space is important

            'sep1': {'class': 'allbx',
                     'ocr': r'^>[Il]<$'}
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk == 'prob_sol': 
            d['k'] = '.'.join([d['root'], trim(k)])

        else:
            if tk == 'problems':
                d['q_or_a'] = 'q'
            
            elif tk == 'solutions':
                d['q_or_a'] = 'a'

            elif tk == 'chapter': 
                d['root'] = k

            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_line(bx), sys.maxsize
