# -*- coding: utf-8 -*-
from books import *

class torchinsky(book):
    
    def __init__(self):
        super(torchinsky, self).__init__()
        
        self.pgs = range(13, 457)
        self.src = "/home/cytu/usr/doc/math/anly/th/Torchinsky A. Real-Variable Methods in Harmonic Analysis.djvu"
        self.tokens.update({
            'chapter': {'class': 'first2',      
                     'ocr': r'^((X|V|I)+)',
                    },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+)\.?)',
                    },

            'remark': {'class': 'indent0', 
                       'ocr': r'^(Remark (\d+\.\d+)\.?)',
                      },
            
            'example': {'class': 'indent0', 
                        'ocr': r'^(Example (\d+\.\d+)\.?)',
                       },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+)\.?)', 
                   },
            
            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                      },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk == 'thm':
            d['q_or_a'] = 'q'
            d['k'] = '.'.join([d['chap'], k])
        
        elif tk == 'proof':
            d['q_or_a'] = 'a'

        else:
            if tk == 'chapter':
                d['chap'] = k
            b_skip = True
        
        return b_skip, d

    #def ym(self, bx):
    #    import sys
    #    return self.ymin_line(bx), sys.maxsize 
