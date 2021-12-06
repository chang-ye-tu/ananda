# -*- coding: utf-8 -*-

from books import *

class schilling(book):
    
    def __init__(self):
        super(schilling, self).__init__()
        
        self.pgs = range(14, 650)

        self.src = "/home/cytu/usr/doc/math/prob/th/Schilling/all.pdf"

        self.tokens.update({
            'chapter': {'class': 'first',
                        'ocr': r'^\d+$',
                       },
            
            'thm': {'class': 'indent0',      
                    'ocr': r'^(((\d+|[A-E])\.\d+) (Lemma|Corollary|Theorem|Proposition|Properties))', 
                   },

            'prob_start': {'class': 'indent0',
                           'ocr': r'^Problems$',
                           },

            'ex': {'class': 'indent0',      
                    'ocr': r'^(((\d+|[A-E])\.\d+) Example)', 
                   },

            'remark': {'class': 'indent0',      
                    'ocr': r'^(((\d+|[A-E])\.\d+) Remark)', 
                   },

            'def': {'class': 'indent0',      
                    'ocr': r'^(((\d+|[A-E])\.\d+) (Deﬁnition|Definition))',
                   },

            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                      },
            
            'prob': {'class': 'indent0',
                     'ocr': r'^(\d+\.\d+)\. ',
                    },
            
            'sol': {'class': 'indent0',
                    'ocr': r'^Problem (\d+\.\d+)',
                   },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'prob', 'sol']:
            if tk in ['thm', 'proof']:
                if tk == 'thm':
                    d['q_or_a'] = 'q'
                    if tk == 'thm':
                        d['k'] = k
                else:
                    d['q_or_a'] = 'a'
            else:
                d['q_or_a'] = 'q' if tk == 'prob' else 'a'  
                d['k'] = k 
             
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.centerh()) & myset(bxs.tiny()))
        ml = self.ymax_line(bx)
        return 0 if nr else self.ymin_skip1(bx), min(sort_y(nr)[-1][1], ml) if nr else ml 
