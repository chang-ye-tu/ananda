# -*- coding: utf-8 -*-

from books import *

class baldi2(book):
    
    def __init__(self):
        super(baldi2, self).__init__()
        
        self.pgs = range(10, 390)
        self.morph0 = 'c150.6'
        self.range_indent0 = (0., 6e-2)

        self.src = "/home/cytu/usr/doc/math/prob/th/Baldi P. Probability An Introduction Through Theory and Exercises.pdf"
        
        self.tokens.update({
            'chap': {'class': 'top',      
                    'ocr': r'^(Chapter \d+)', 
                    },

            'ind': {'class': 'indent0',      
                    'ocr': r'^(\d+\.\d+)', 
                   },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition|Criterion) (\d+\.\d+))', 
                   },
            
            'remark': {'class': 'indent0',      
                    'ocr': r'^(Remark (\d+\.\d+))', 
                   },

            'example': {'class': 'indent0',      
                        'ocr': r'^(Example (\d+\.\d+))', 
                    },

            'defn': {'class': 'indent0',      
                     'ocr': r'^((Deﬁnition|Definition) (\d+\.\d+))', 
                    },
            
            'proof': {'class': 'indent0', 
                      'ocr': r'^Proof',
                     },

            'ex_start': {'class': 'indent0', 
                         'ocr': r'^Exercises$',
                     },
            
            'sol_start': {'class': 'first2', 
                          'ocr': r'^Solutions$',
                     },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'ind']:
            if tk in ['thm', 'ind']:
                if tk == 'thm':
                    d['q_or_a'] = 'q'
                    d['k'] = k.strip()
                elif tk == 'ind':
                    if d.get('b_ind', False):
                        d['k'] = k.strip()
                    else:
                        b_skip = True
            else:
                d['q_or_a'] = 'a'

        else:
            if tk in ['chap', 'ex_start', 'sol_start']:
                d['b_ind'] = True 
                if tk == 'ex_start':
                    d['q_or_a'] = 'q'
                elif tk == 'sol_start':
                    d['q_or_a'] = 'a'
                else:
                    d['b_ind'] = False 

            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        return self.ymin_skip1(bx), self.ymax_line(bx, w=(0.35, 0.45)) 
