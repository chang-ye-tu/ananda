# -*- coding: utf-8 -*-

from books import *

class costara(book):

    def __init__(self):
        super(costara, self).__init__()

        self.src = '/home/cytu/usr/doc/math/ex/Costara C., Popa D. Exercises in Functional Analysis.pdf'
        self.pgs = range(11, 451)
        self.tokens.update({
            'chapter':  {'class': 'top', 
                         'ocr': r'Chapter (\d+)',
                         },

            'section':  {'class': 'indent0', 
                         'ocr': r'^\d+\.\d+ (Exercises|Solutions)$',
                         },
            
            'prob_sol': {'class': 'indent1',
                         'ocr': r'^(\d+)\.', 
                         },

            'caption': {} # placeholder
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['chapter', 'section', 'caption', 'sep']:
            if tk == 'chapter':
                d['root'] = k
            elif tk == 'section':
                d['q_or_a'] = 'a' if find(k, 'Solutions') else 'q'

            b_skip = True

        else:
            d['k'] = '.'.join([trim(d['root']), trim(k)])
        
        return b_skip, d

    def ym(self, bx):
        return self.ymin_line(bx), sys.maxsize
