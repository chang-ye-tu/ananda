# -*- coding: utf-8 -*-
from books import *

class torchinsky1(book):

    def __init__(self):
        super(torchinsky1, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Torchinsky A. Problems in Real and Functional Analysis.djvu'
        self.pgs = range(13, 474)
        self.tokens.update({
            'chapter':  {'class': 'first2', 
                         'ocr': r'^Chapter (\d+)$',
                        },

            'ex_sol': {'class': 'indent1',      
                       'ocr': '^(\d+)', 
                        },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['chapter', 'sep']:
            if tk == 'chapter':
                d['root'] = k
            b_skip = True

        else:
            if int(d['root']) > 10:
                chapter = str(int(d['root']) - 10)
                d['q_or_a'] = 'a'
            else:
                chapter = d['root']
                d['q_or_a'] = 'q' 
            d['k'] = '.'.join([chapter, trim(k)])
        
        return b_skip, d

    def ym(self, bx):
        return self.ymin_line(bx), self.ymax_line(bx)
