# -*- coding: utf-8 -*-

from books import *

class grisvard(book):
    
    def __init__(self):
        super(grisvard, self).__init__()
        
        self.pgs = range(12, 412)
        self.src = "/home/cytu/usr/doc/math/anly/th/Grisvard P. Elliptic Problems in Nonsmooth Domains.djvu"
        
        self.tokens.update({
            'chapter': {'class': 'indent0',
                        'ocr': r'^(\d+)$',
                       },
            
            'section': {'class': 'indent0', 
                        'ocr': r'^(\d+\.\d+(\.\d+)?) ',
                       },

            'remark': {'class': 'indent0', 
                       'ocr': r'^(Remark (\d+\.\d+\.\d+(\.\d+)?)) ',
                      },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+\.\d+(\.\d+)?)) ',
                    },
            
            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+\.\d+(\.\d+)?)) ', 
                   },
            
            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof ',
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

    def ym(self, bx):
        import sys
        return self.ymin_line(bx), sys.maxsize
