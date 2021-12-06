# -*- coding: utf-8 -*-

from books import *

class kirsch_grinberg(book):

    def __init__(self):
        super(kirsch_grinberg, self).__init__()

        self.src ='/home/cytu/usr/doc/math/anly/appl/Kirsch A., Grinberg N. The Factorization Method for Inverse Problems.pdf' 
        self.pgs = range(15, 206)
        
        self.tokens.update({
            'chapter': {'class': 'top',      
                        'ocr': r'^(\d+)$', 
                        },
            
            'section': {'class': 'indent0',      
                        'ocr': r'^(\d+\.\d+)', 
                        },

            'subsection': {'class': 'indent0',      
                           'ocr': r'^(\d+\.\d+\.\d+)', 
                          },
            
            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem) (\d+\.\d+))', 
                    },

            'defn':  {'class': 'indent0', 
                      'ocr': r'^((Deﬁnition|Assumption) (\d+\.\d+))', 
                       },

            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                       },

            'remark':  {'class': 'indent0', 
                        'ocr': r'^Remark',
                        },
        })
     
    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['chapter', 'section', 'subsection', 'sep', 'remark', 'defn']:
            b_skip = True

        else:
            if tk == 'thm':
                d['k'] = k
                d['q_or_a'] = 'q' 

            elif tk == 'proof':
                d['q_or_a'] = 'a'
        
        return b_skip, d

    def ym(self, bx):
        return self.ymin_chap(bx), self.ymax_line(bx)
