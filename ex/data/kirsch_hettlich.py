# -*- coding: utf-8 -*-

from books import *

class kirsch_hettlich(book):

    def __init__(self):
        super(kirsch_hettlich, self).__init__()

        self.src ="/home/cytu/usr/doc/math/anly/appl/Kirsch A., Hettlich F. The Mathematical Theory of Time-Harmonic Maxwell's Equations Expansion Integral and Variational Methods.pdf" 
        self.pgs = range(14, 342)
        
        self.tokens.update({
            'chapter': {'class': 'top',      
                        'ocr': r'^(Chapter \d+|Appendix A)$', 
                        },
            
            'section': {'class': 'indent0',      
                        'ocr': r'^((\d+|[A])\.\d+)', 
                        },

            'subsection': {'class': 'indent0',      
                           'ocr': r'^(\d+\.\d+\.\d+)', 
                          },
            
            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem) ((\d+|[A])\.\d+))', 
                    },

            'defn':  {'class': 'indent0', 
                      'ocr': r'^(Deﬁnition ((\d+|[A])\.\d+))', 
                       },

            'example':  {'class': 'indent0', 
                         'ocr': r'^(Example ((\d+|[A])\.\d+))', 
                         },
            
            'ex':  {'class': 'indent0', 
                    'ocr': r'^(Exercise (\d+\.\d+))', 
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

        if tk in ['thm', 'proof']: 
            if tk == 'thm':
                d['k'] = k
                d['q_or_a'] = 'q' 

            elif tk == 'proof':
                d['q_or_a'] = 'a'
        else:
            b_skip = True
        
        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
