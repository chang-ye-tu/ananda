# -*- coding: utf-8 -*-

from books import *

class colton_kress(book):
    
    def __init__(self):
        super(colton_kress, self).__init__()
        
        self.pgs = range(27, 403)

        self.src = "/home/cytu/usr/doc/math/anly/appl/Colton D., Kress R. Inverse Acoustic and Electromagnetic Scattering Theory 3ed.pdf"

        self.tokens.update({
            'chapter': {'class': 'top',
                        'ocr': r'^(\d+\.) '
                        },

            'section': {'class': 'indent0',
                        'ocr': r'^(\d+\.\d+) '
                        },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+))',
                    },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem) (\d+\.\d+))', 
                   },
            
            'proof':  {'class': 'indent0', 
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
