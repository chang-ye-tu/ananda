# -*- coding: utf-8 -*-

from books import *

class gasinski2(book):
    
    def __init__(self):
        super(gasinski2, self).__init__()
        
        self.pgs = range(9, 1237)
        self.morph0 = 'c150.6'
        self.b_sep_sym_before = True 

        self.src = u"/home/cytu/usr/doc/math/ex/Gasiński L., Papageorgiou N. Exercises in Analysis Part 2 Nonlinear Analysis.pdf"
        
        self.tokens.update({
            'bib': {'class': 'top',      
                    'ocr': r'^Bibliography', 
                   },

            'sec': {'class': 'indent0',      
                    'ocr': r'^(\d+\.\d+) ', 
                   },

            'subsec': {'class': 'indent0',      
                    'ocr': r'^(\d+\.\d+\.\d+) ', 
                   },
            
            'thm': {'class': 'indent0',      
                     'ocr': r'^((Theorem|Proposition|Lemma|Corollary) (\d\.\d+))', 
                   },

            'remark': {'class': 'indent0',      
                       'ocr': r'^(Remark (\d\.\d+))', 
                   },

            'example': {'class': 'indent0',      
                        'ocr': r'^(Example (\d\.\d+))', 
                   },

            'def': {'class': 'indent0',      
                    'ocr': r'^(Deﬁnition (\d\.\d+))', 
                   },

            'prob': {'class': 'indent0',      
                     'ocr': r'^Problem (\d\.\d+)', 
                   },

            'sol': {'class': 'indent0',      
                    'ocr': r'^Solution of Problem (\d+\.\d+)', 
                   },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['prob', 'sol']:
            d['q_or_a'] = 'q' if (tk in ['prob']) else 'a'
            d['k'] = k
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        return self.ymin_skip1(bx), self.ymax_line(bx, w=(0.35, 0.45)) 
