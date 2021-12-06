# -*- coding: utf-8 -*-

from books import *

class dixon(book):

    def __init__(self):
        super(dixon, self).__init__()

        self.src = "/home/cytu/usr/doc/math/ex/Dixon J. Problems in Group Theory.djvu"
        self.pgs = range(18, 184)
        self.range_lineh = (0, 3)
        self.morph0 = 'c100.4'

        self.tokens.update({
            'chapter': {'class': 'first2',      
                        'ocr': r'^(\d+ |Chapter)', 
                        },
            
            'sol_start': {'class': 'allbx',
                          'ocr': r'^Solutions$'
                         },
            
            'prob_start': {'class': 'allbx',
                           'ocr': r'^PROBLEMS$'
                        },

            'prob_sol': {'class': 'indent0',      
                         'ocr': r'^[*]?(\d+\.\d+)\.',
                         },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['prob_sol']:
            d['k'] = k 
        
        else:
            if tk in ['prob_start', 'sol_start']:
                d['q_or_a'] = 'a' if tk == 'sol_start' else 'q'
            b_skip = True 

        return b_skip, d
    
    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.tiny()))
        ml = self.ymax_line(bx)
        return 0 if nr else self.ymin_line(bx, w=(0.9, 1)), min(ml, sort_y(bx)[-1][1]) if nr else ml

    def post(self, d):
        self.post_func(d, l=('sol_start',))
