# -*- coding: utf-8 -*-

from books import *

class girault(book):
    
    def __init__(self):
        super(girault, self).__init__()
        
        self.pgs = range(10, 377)
        
        self.src = "/home/cytu/usr/doc/math/anly/appl/Girault V., Raviart P.-A. Finite Element Methods for Navier-Stokes Equations Theory and Algorithms.pdf"

        self.tokens.update({
            'chapter': {'class': 'top',
                        'ocr': r'^Chapter ([IXV]+)',
                       },
            
            'section': {'class': 'indent0', 
                        'ocr': r'^([A0-9]+\.\d+\.|§[ ]?\d+|Appendix)',
                       },

            'defn': {'class': 'indent0', 
                        'ocr': r'^(De(ﬁ|fi)nition ([A0-9]+\.\d+))\.',
                    },
            
            'hyp': {'class': 'indent0', 
                    'ocr': r'^(Hypothesis (H\d+))',
                    },
            
            'remark': {'class': 'indent0', 
                       'ocr': r'^Remark',
                      },
            
            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition) ([A0-9]+\.\d+))\.', 
                   },
            
            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                      },
            
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof']:
            if tk == 'thm':
                d['q_or_a'] = 'q'
                d['k'] = ' '.join([d['root'], k])
            else:
                d['q_or_a'] = 'a'
        else:
            if tk == 'chapter':
                d['root'] = k
            b_skip = True

        return b_skip, d

    def post(self, d):
        self.post_func(d, l=('chapter',))
