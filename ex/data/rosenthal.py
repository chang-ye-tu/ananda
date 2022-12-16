# -*- coding: utf-8 -*-

from books import *

class rosenthal(book):
    
    def __init__(self):
        super(rosenthal, self).__init__()
        
        self.pgs = range(17, 224)
        self.morph0 = 'c150.6'

        self.src = u"/home/cytu/usr/doc/math/prob/th/Rosenthal J. A First Look at Rigorous Probability Theory 2ed.pdf"

        self.tokens.update({
            'sec': {'class': 'indent0',      
                    'ocr': r'^((\d+|[A])(\.\d+\.))', 
                   },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition ((\d+|[A])\.\d+\.\d+))', 
                    },
            
            'thm': {'class': 'indent0',      
         'ocr': r'^((Lemma|Corollary|Theorem|Pr[0o]p[0o]sition) ((\d+|[A])\.\d+\.\d+))', 
                   },
            
            'example': {'class': 'indent0',      
                        'ocr': r'^(Example ((\d+|[A])\.\d+\.\d+))', 
                   },

            'proof': {'class': 'indent0', 
                      'ocr': r'^Proof',
                     },
            
            'ex': {'class': 'indent0',      
                   'ocr': r'^(Exercise ((\d+|[A])\.\d+\.\d+))', 
                   },

            'remark': {'class': 'indent0',      
                       'ocr': r'^(Remark(s)?[ ]?((\d+|[A])\.\d+\.\d+)?)', 
                      },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof']:
            if tk in ['thm']:
                d['q_or_a'] = 'q'
                d['k'] = k.strip()
            else:
                d['q_or_a'] = 'a'
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        ml = self.ymax_line(bx, w=(0.38, 0.41))
        return self.ymin_skip1(bx), ml 
