# -*- coding: utf-8 -*-

from books import *

class aliprantis(book):

    def __init__(self):
        super(aliprantis, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Aliprantis/Aliprantis C., Burkinshaw O. Principles of Real Analysis 3ed.djvu' 
        self.pgs = range(7, 402)
        self.range_indent0 = (0., 1e-2)
        self.range_indent1 = (1e-2, 6e-2)
        self.range_lineh = (0, 3) 
        self.tokens.update({
            'chapter':  {'class': 'first2', 
                         'ocr': r'^CHAPTER (\d)',
                         },

            'section':  {'class': 'indent0', 
                         'ocr': r'^(\d+\.) ',
                         },

            'thm': {'class': 'indent1',      
                    'ocr': r'^((Theorem|Corollary|Lemma) (\d+\.\d+))\.?', 
                   },
            
            'example': {'class': 'indent0',      
                        'ocr': r'^(Example (\d+\.\d+))\.?', 
                       },

            'defn': {'class': 'indent1',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+))\.?',
                    },

            'proof': {'class': 'indent1',      
                      'ocr': r'^Proof', 
                     },

            'ex_start': {'class': 'indent0',
                         'ocr': r'^EXERCISES$',
                         },

        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['thm', 'proof']:
            if tk == 'thm':
                d['q_or_a'] = 'q'
                d['k'] = k
            else:
                d['q_or_a'] = 'a' 
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)

    def post(self, d):
        yd = d['yd']
        tkd = d['tkd']
        for pg in tkd:
            for tk in tkd[pg]:
                if tk[1] == 'chapter':
                    bx = d['bxd'][pg]
                    yd[pg] = [0, min(sort_y(bx)[-1][1], self.ymax_line(bx))]

