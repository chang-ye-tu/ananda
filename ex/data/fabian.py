# -*- coding: utf-8 -*-

from books import *

class fabian(book):
    
    def __init__(self):
        super(fabian, self).__init__()
        
        self.pgs = range(13, 753)
        self.morph0 = 'c150.6'

        self.src = u"/home/cytu/usr/doc/math/anly/th/Fabian M., Habala P., Hájek P., Montesinos V., Zizler V. Banach Space Theory The Basis for Linear and Nonlinear Analysis.pdf"
        
        self.tokens.update({
            'chap': {'class': 'top',      
                    'ocr': r'^(Chapter \d+)', 
                    },

            'ex_start': {'class': 'indent0',
                         'ocr': '^Exercises for Chapter',
                         },
            
            'ex': {'class': 'indent0',      
                    'ocr': r'^\d+\.\d+ ', 
                   },

            'sol': {'class': 'indent0',      
                    'ocr': r'^Hint\.', 
                   },

            'thm': {'class': 'indent0',      
             'ocr': r'^((Lemma|Corollary|Theorem|Proposition|Fact) (\d+\.\d+))', 
                   },
            
            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+))', 
                    },
            
            'remark': {'class': 'indent0',      
                    'ocr': r'^Remark', 
                   },

            'example': {'class': 'indent0',      
                        'ocr': r'^Example', 
                   },

            'proof': {'class': 'indent0', 
                      'ocr': r'^Proof',
                     },
            
            'noop': {'class': 'indent0', 
                      'ocr': r'^Open Problem',
                     },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'ex', 'proof', 'sol']:
            if tk == 'thm' or (tk == 'ex' and d.get('ex_start', False)):
                d['q_or_a'] = 'q'
                d['k'] = k.strip()
            elif tk in ['proof', 'sol']:
                d['q_or_a'] = 'a'
            else:
                b_skip = True

        else:
            if tk == 'ex_start':
                d['ex_start'] = True
            elif tk == 'chap':
                d['ex_start'] = False
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        ml = self.ymax_line(bx, w=(0.30, 0.31))
        return self.ymin_skip1(bx), ml 
