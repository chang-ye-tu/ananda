# -*- coding: utf-8 -*-

from books import *

class necas(book):
    
    def __init__(self):
        super(necas, self).__init__()
        
        self.pgs = range(17, 374)
        self.morph0 = 'c150.6'

        self.src = u"/home/cytu/usr/doc/math/anly/th/Nečas J. Direct Methods in the Theory of Elliptic Equations.pdf"
        
        self.tokens.update({
            'chapter': {'class': 'first',      
                        'ocr': r'^Chapter (\d+)', 
                       },

            'sec': {'class': 'indent0',      
                    'ocr': r'^\d+\.\d+', 
                   },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition) \d+\.\d+)', 
                   },
            
            'def': {'class': 'indent0',      
                    'ocr': r'^Deﬁnition \d+\.\d+', 
                   },
            
            'example': {'class': 'indent0',      
                        'ocr': r'^Example \d+\.\d+', 
                       },

            'ex': {'class': 'indent0',      
                   'ocr': r'^Exercise \d+\.\d+', 
                  },

            'remark': {'class': 'indent0',      
                       'ocr': r'^Remark \d+\.\d+', 
                      },

            'proof': {'class': 'indent0', 
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
                d['k'] = d['chapter'] + ' ' + k.strip()
            else:
                d['q_or_a'] = 'a'
        
        else:
            if tk == 'chapter':
                d['chapter'] = k

            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx) 
