# -*- coding: utf-8 -*-

from books import *

class abramovich_sol(book):

    def __init__(self):
        super(abramovich_sol, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Aliprantis/Abramovich Y., Aliprantis C. Problems in Operator Theory.djvu' 
        self.pgs = range(13, 388)
        self.morph0 = 'c100.4'
        self.tokens.update({
            'chapter': {'class': 'indent0r',      
                        'ocr': r'^Chapter \d+$', 
                        },
            
            'section': {'class': 'indent0',      
                        'ocr': r'^\d+\.\d+\. ', 
                        },

            'prob': {'class': 'indent0',      
                     'ocr': r'Problem (\d+\.\d+\.\d+)', 
                     },

            'sol': {'class': 'indent0',
                    'ocr': r'^Solution',
                    },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['chapter', 'section', 'sep']:
            b_skip = True 

        else:
            if tk == 'sol':
                d['q_or_a'] = 'a'
            else:
                d['k'] = trim(k)
                d['q_or_a'] = 'q' 
        
        return b_skip, d
    
    def ym(self, bx):
        return self.ymin_line(bx), self.ymax_line(bx) 
