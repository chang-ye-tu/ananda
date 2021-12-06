# -*- coding: utf-8 -*-

from books import *

class kirsch_angell(book):

    def __init__(self):
        super(kirsch_angell, self).__init__()

        self.src ="/home/cytu/usr/doc/math/anly/appl/Angell T., Kirsch A. Optimization Methods in Electromagnetic Radiation.pdf" 
        self.pgs = range(15, 333)
        
        self.tokens.update({
            'section': {'class': 'indent0',      
                        'ocr': r'^((\d+|[A])\.\d+)', 
                        },

            'subsection': {'class': 'indent0',      
                           'ocr': r'^((\d+|[A])\.\d+\.\d+)', 
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

        if tk in ['chapter', 'section', 'subsection', 'sep', 'remark', 'defn', 'example']:
            b_skip = True

        else:
            if tk == 'thm':
                d['k'] = k
                d['q_or_a'] = 'q' 

            elif tk == 'proof':
                d['q_or_a'] = 'a'
        
        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
