# -*- coding: utf-8 -*-

from books import *

class dacorogna0(book):
    
    def __init__(self):
        super(dacorogna0, self).__init__()

        self.src = "/home/cytu/usr/doc/math/anly/th/Dacorogna B. Introduction to the Calculus of Variations.pdf"
        self.pgs = range(22, 231)
        self.tokens.update({
            'chapter': {'class': 'top',
                        'ocr': r'^Chapter (\d+)',
                        },
                        
            'section': {'class': 'indent0', 
                        'ocr': r'^(\d+\.\d+) ',
                        },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+))', 
                    },
            
            'example': {'class': 'indent0', 
                        'ocr': r'^Example \d+\.\d+',
                       },
            
            'defn': {'class': 'indent0',      
                     'ocr': r'^Deﬁnition \d+\.\d+',
                    },
            
            'remark': {'class': 'indent0', 
                       'ocr': r'^Remark \d+\.\d+',
                       },

            'proof':  {'class': 'indent1', 
                       'ocr': r'^Proof',
                       },
            
            'ex_sol':  {'class': 'indent0',
                        'ocr': r'^Exercise \d+\.\d+\.\d+',},

            'ex_sol_start': {'class': 'indent0',
                             'ocr': r'^Solutions to the Exercises$',
                            },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'ex_sol']:
            if tk == 'thm':
                d['q_or_a'] = 'q' 
                d['k'] = k

            elif tk == 'proof':
                d['q_or_a'] = 'a'

            else:
                d['q_or_a'] = 'q' if d.get('b_ex', True) else 'a'
                d['k'] = k 

        else:
            if tk == 'ex_sol_start':
                d['b_ex'] = False 

            b_skip = True
        
        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset(sort_y(bx)[-10:]) & myset(bxs.indent0r()) & myset(bxs.tiny()))
        ml = self.ymax_line(bx, w=(0.2, 0.4))
        return 0 if nr else self.ymin_skip1(bx), min(sort_y(nr)[-1][1], ml) if nr else ml 

    def post(self, d):
        self.post_func(d)
