# -*- coding: utf-8 -*-

from books import *

class grimmett_sol(book):

    def __init__(self):
        super(grimmett_sol, self).__init__()

        self.src = '/home/cytu/usr/doc/math/prob/th/Grimmett/Grimmett G. R., Stirzaker D. R. One Thousand Exercises in Probability 3ed.pdf'
        self.replace_title = 0 
        self.pgs = range(13, 579)

        self.tokens.update({
            'section':  {'class': 'centerh', 
                         'ocr': r'(\d+\.\d+ (Solution|Exercise|Problem))',
                         },

            'prob_sol': {'class': 'indent0',      
                         'ocr': r'(\d+)\.', 
                         },
            
            'bar': {'class': 'line',},
        })
    
    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['section', 'bar', 'sep']:
            if tk == 'section':
                d['q_or_a'] = 'a' if find(k, 'Solution') else 'q'
                d['root'] = k.split(' ')[0].strip()
            b_skip = True 

        else:
            d['k'] = '.'.join([trim(d['root']), trim(k)])
        
        return b_skip, d
    
    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
