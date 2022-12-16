# -*- coding: utf-8 -*-

from books import *

class grafakos1(book):
    
    def __init__(self):
        super(grafakos1, self).__init__()
        
        self.pgs = range(14, 428)
        self.morph0 = 'c150.6'

        self.src = "/home/cytu/usr/doc/math/anly/th/Grafakos L. Classical Fourier Analysis 3ed.pdf"
        
        self.tokens.update({
            'chap': {'class': 'top',      
                    'ocr': r'^(Chapter \d+)', 
                    },

            'ex_start': {'class': 'indent0',
                         'ocr': 'Exercises',
                         },
            
            'sec': {'class': 'indent0',      
                    'ocr': r'^(\d+\.\d+(\.\d+)?)', 
                   },

            'thm': {'class': 'indent0',      
             'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+\.\d+\.))', 
                   },
            
            'remark': {'class': 'indent0',      
                    'ocr': r'^(Remark (\d+\.\d+\.\d+\.))', 
                   },
            'ex': {'class': 'indent0',      
                    'ocr': r'^(Example (\d+\.\d+\.\d+\.))', 
                   },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+\.\d+\.))', 
                    },
            
            'proof': {'class': 'indent0', 
                      'ocr': r'^Proof',
                     },

            'hist': {'class': 'centerh', 
                      'ocr': r'^HISTORICAL NOTES',
                     },

        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof',]:
            if tk == 'thm':
                d['q_or_a'] = 'q'
                d['k'] = k.strip()
            else:
                d['q_or_a'] = 'a'

        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        #nr = list(myset(sort_y(bx)[-3:]) & myset(bxs.tiny()) & myset(bxs.indent0r()))
        ml = self.ymax_line(bx, w=(0.30, 0.31))
        #return 0 if nr else self.ymin_skip1(bx), min(sort_y(bx)[-3][1], ml) if nr else ml 
        return self.ymin_skip1(bx), ml 

