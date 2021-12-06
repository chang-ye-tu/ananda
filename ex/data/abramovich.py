# -*- coding: utf-8 -*-

from books import *

class abramovich(book):

    def __init__(self):
        super(abramovich, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Aliprantis/Abramovich Y., Aliprantis C. An Invitation to Operator Theory.djvu' 
        self.pgs = range(15, 520)
        self.range_lineh = (0, 4)
        self.range_indent1 = (3e-2, 7e-2)
        self.range_indent0r = (0., 5e-2)
        self.tokens.update({
            'chapter':  {'class': 'first2', 
                         'ocr': r'^Chapter (\d+)$',
                         },

            'section':  {'class': 'indent0', 
                         'ocr': r'^(\d+\.\d+\.) ',
                         },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Theorem|Corollary|Lemma) (\d+\.\d+))\.?', 
                   },
            
            'example': {'class': 'indent0',      
                        'ocr': r'^(Example (\d+\.\d+))\.?', 
                       },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+))\.?',
                    },

            'proof': {'class': 'indent0',      
                      'ocr': r'^Proof', 
                     },

            'ex_start': {'class': 'indent0',
                         'ocr': r'^Exercises$',
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
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.indent0r()) & myset(bxs.tiny()))
        ml = self.ymax_line(bx)
        return (self.ymin_skip1(bx) if nr else self.ymin_line(bx), min(sort_y(bx)[-2][1], ml) if nr else ml)
