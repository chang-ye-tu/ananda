# -*- coding: utf-8 -*-

from books import *

class gilbarg(book):
    
    def __init__(self):
        super(gilbarg, self).__init__()
        
        self.pgs = range(25, 506)
        
        self.range_indent0 = (0., 3e-2)
        self.src = "/home/cytu/usr/doc/math/anly/th/Gilbarg D., Trudinger N. Elliptic Partial Differential Equations of Second Order 2ed.djvu"
        self.tokens.update({
            'chapter': {'class': 'top',
                        'ocr': r'Chapter \d+',
                       },
            
            'section': {'class': 'indent0', 
                        'ocr': r'^(\d+\.\d+)\. ',
                       },

            'note': {'class': 'indent0', 
                       'ocr': r'^Notes$',
                      },

            'example': {'class': 'indent0', 
                        'ocr': r'^Examples?\.',
                       },
            
            'defn': {'class': 'indent0', 
                        'ocr': r'^Deﬁnitions?',
                    },

            'remark': {'class': 'indent0', 
                       'ocr': r'^Remark',
                      },
            
            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem) (\d+\.\d+))\.', 
                   },
            
            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                      },
            
            'prob_start': {'class': 'indent0',
                           'ocr': r'^Problems$',
                          },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof']:
            if tk == 'thm':
                d['q_or_a'] = 'q'
                d['k'] = k
            else:
                d['q_or_a'] = 'a'
        else:
            b_skip = True

        return b_skip, d
