# -*- coding: utf-8 -*-

from books import *

class aliprantis_sol(book):

    def __init__(self):
        super(aliprantis_sol, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Aliprantis/Aliprantis C., Burkinshaw O. Problems in Real Analysis 2ed.djvu' 
        self.pgs = range(5, 404)
        self.tokens.update({
            'chapter':  {'class': 'first2', 
                         'ocr': r'^CHAPTER (\d)',
                         },

            'section':  {'class': 'indent0', 
                         'ocr': r'^(\d+\.)',
                         },

            'problem': {'class': 'indent0',      
                        'ocr': r'^Problem (\d+\.\d+)\.?', 
                        },
            
            'solution': {'class': 'indent0',      
                         'ocr': r'^Solution\.', 
                         },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['chapter', 'section', 'sep']:
            b_skip = True 

        else:
            if tk == 'solution':
                d['q_or_a'] = 'a'
            else:
                d['q_or_a'] = 'q' 
                d['k'] = trim(k) 
        
        return b_skip, d
    
    def post(self, d):
        yd = d['yd']
        tkd = d['tkd']
        for pg in tkd:
            for tk in tkd[pg]:
                if tk[1] == 'chapter':
                    bx = d['bxd'][pg]
                    yd[pg] = [0, min(sort_y(bx)[-1][1], self.ymax_line(bx))]
