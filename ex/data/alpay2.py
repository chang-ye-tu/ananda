# -*- coding: utf-8 -*-
from books import *

class alpay2(book):

    def __init__(self):
        super(alpay2, self).__init__()

        self.src = '/home/cytu/usr/doc/math/ex/Alpay D. An Advanced Complex Analysis Problem Book Topological Vector Spaces Functional Analysis and Hilbert Spaces of Analytic Functions.pdf'
        self.pgs = range(20, 488)

        self.tokens.update({
            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+\.\d+))', 
                     },

            'remark': {'class': 'indent0',      
                     'ocr': r'^(Remark (\d+\.\d+\.\d+))', 
                     },

            'question': {'class': 'indent0',      
                     'ocr': r'^(Question (\d+\.\d+\.\d+))', 
                     },

            'example': {'class': 'indent0',      
                     'ocr': r'^(Example (\d+\.\d+\.\d+))', 
                     },

            'thm': {'class': 'indent0',      
                     'ocr': r'^((Proposition|Theorem|Corollary|Lemma) (\d+\.\d+\.\d+))', 
                     },

            'proof': {'class': 'indent0',      
                     'ocr': r'^Proof', 
                     },

            'exercise': {'class': 'indent0',      
                        'ocr': r'^Exercise (\d+\.\d+\.\d+)', 
                        },
            
            'solution': {'class': 'indent0',      
                         'ocr': r'^Solution of Exercise (\d+\.\d+\.\d+)', 
                         },
            
            'section': {'class': 'indent0',
                        'ocr': r'^(\d+\.\d+)',
                        },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['exercise', 'solution']: 
            d['k'] = k
            d['q_or_a'] = 'a' if tk == 'solution' else 'q'

        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_line(bx), sys.maxsize
