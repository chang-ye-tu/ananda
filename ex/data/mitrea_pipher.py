# -*- coding: utf-8 -*-

from books import *

class mitrea_pipher(book):
    
    def __init__(self):
        super(mitrea_pipher, self).__init__()
        
        self.pgs = range(5, 57)

        self.src = "/home/cytu/usr/work/thesis/paper/Mitrea D., Mitrea M., Pipher J. Vector Potential Theory on Nonsmooth Domain in $R^3$ and Applications to Electromagnetic Theory.pdf"

        self.tokens.update({
            'section': {'class': 'allbx',
                        'ocr': r'^(\d+)\.'
                        },

            'remark': {'class': 'allbx',      
                       'ocr': r'^Remark', 
                      },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem) (\d+\.\d+)\.)', 
                   },
            
            'proof':  {'class': 'allbx', 
                       'ocr': r'^Proof',
                      },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof',]:
            if tk == 'thm':
                d['q_or_a'] = 'q'
                d['k'] = k
            else:
                d['q_or_a'] = 'a'
             
        else:
            b_skip = True

        return b_skip, d
