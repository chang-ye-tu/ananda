# -*- coding: utf-8 -*-

from books import *

class bauschke(book):
    
    def __init__(self):
        super(bauschke, self).__init__()
        
        self.pgs = range(16, 579)
        self.morph0 = 'c150.6'

        self.src = u"/home/cytu/usr/doc/math/or/Bauschke H., Combettes P. Convex Analysis and Monotone Operator Theory in Hilbert Spaces 2ed.pdf"
        
        self.tokens.update({
            'chap': {'class': 'top',      
                    'ocr': r'^(Chapter \d+)', 
                    },

            'sec': {'class': 'indent0',
                    'ocr': '^\d+\.\d+ ',
                   },

            'ex_start': {'class': 'indent0',
                         'ocr': '^Exercises$',
                         },
            
            'ex': {'class': 'indent0',      
                    'ocr': r'^((Exercise) (\d+\.\d+))', 
                   },

            'thm': {'class': 'indent0',      
             'ocr': r'^((Lemma|Corollary|Theorem|Proposition|Fact) (\d+\.\d+))', 
                   },
            
            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+))', 
                    },
            
            'remark': {'class': 'indent0',      
                        'ocr': r'^((Remark) (\d+\.\d+))', 
                   },

            'example': {'class': 'indent0',      
                        'ocr': r'^((Example) (\d+\.\d+))', 
                   },

            'proof': {'class': 'indent0', 
                      'ocr': r'^Proof',
                     },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'example']:
            if tk in ['thm', 'example']:
                d['q_or_a'] = 'q'
                d['k'] = k.strip()
            else:
                d['q_or_a'] = 'a'
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        ml = self.ymax_line(bx, w=(0.30, 0.31))
        return self.ymin_skip1(bx), ml 
