# -*- coding: utf-8 -*-

from books import *

class medvegyev(book):

    def __init__(self):
        super(medvegyev, self).__init__()

        self.src = '/home/cytu/usr/doc/math/prob/th/Medvegyev P. Stochastic Integration Theory/Medvegyev P. Stochastic Integration Theory.pdf' 
        self.pgs = range(21, 614)
        self.morph0 = 'c100.5'
        self.tokens.update({
            'section':  {'class': 'indent0', 
                         'ocr': r'^((\d+|[ABC])\.\d+(\.\d+)?) ',
                        },

            'thm': {'class': 'indent0',      
             'ocr': r'^((Lemma|Corollary|Theorem|Proposition) ((\d+|[ABC])\.\d+))',
                   },
            
            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition ((\d+|[ABC])\.\d+))', 
                    },
            
            'proof': {'class': 'indent0', 
                      'ocr': r'^Proof',
                     },

            'example': {'class': 'indent0',
                        'ocr': r'^(Example ((\d+|[ABC])\.\d+)) ',
                        },
        })
        
    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['thm', 'proof', 'example']:
            if tk in ('thm', 'example'):
                d['q_or_a'] = 'q'
                d['k'] = k 
            else:
                d['q_or_a'] = 'a' 
        else:
            b_skip = True

        return b_skip, d
    
    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
