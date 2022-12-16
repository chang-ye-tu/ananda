# -*- coding: utf-8 -*-

from books import *

class brezis(book):
    
    def __init__(self):
        super(brezis, self).__init__()

        self.src = "/home/cytu/usr/doc/math/anly/th/Brezis H. Functional Analysis Sobolev Spaces and Partial Differential Equations.pdf"
        self.pgs = range(15, 598)
        self.tokens.update({
            'chapter': {'class': 'top',
                        'ocr': r'^Chapter (\d+)',
                        },
                        
            'section': {'class': 'indent0', 
                        'ocr': r'^[0o*]?[ ]?(\d+\.\d+) ',
                        },

            'thm': {'class': 'indent0',      
                    'ocr': r'^[0o*]?[ ]?((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+))', 
                    },
            
            'example': {'class': 'indent0', 
                        'ocr': r'^[0o*]?[ ]?(Example \d+)',
                       },
            
            'nota': {'class': 'indent0', 
                     'ocr': r'^[0o*]?[ ]?Notation',
                       },

            'defn': {'class': 'indent0',      
                     'ocr': r'^[0o*]?[ ]?Deﬁnition',
                    },
            
            'remark': {'class': 'indent0', 
                       'ocr': r'^[0o*]?[ ]?Remark',
                       },

            'comment': {'class': 'indent0',
                        'ocr': r'^Comment',
                        },

            'proof':  {'class': 'indent0', 
                       'ocr': r'Proof',
                       },
            
            'ex':  { },

            'prob': {'class': 'centerh',
                     'ocr': r'^PROBLEM (\d+)',
                    },

            'prob_sol': {'class': 'centerh',
                         'ocr': r'^Problem (\d+)$',
                        },

            'ex_start': {'class': 'indent0',
                         'ocr': r'^Exercises for Chapter (\d+)',
                        },

            'prob_start': {'class': 'top',
                           'ocr': r'^Problems$',
                          },

            'ex_sol_start': {'class': 'top',
                             'ocr': r'^Solutions of Some Exercises$',
                            },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'prob', 'ex', 'prob_sol']:
            if tk == 'thm':
                d['q_or_a'] = 'q' 
                d['k'] = k

            elif tk == 'proof':
                d['q_or_a'] = 'a'

            elif tk == 'ex':
                d['k'] = ' '.join([tk, k])
            
            else:
                d['q_or_a'] = 'q' if tk == 'prob' else 'a'
                d['k'] = ' '.join(['prob', k])

        else:
            if tk == 'chapter':
                d['root'] = k
            elif tk == 'ex_start':
                d['q_or_a'] = 'q' 
            elif tk in ['ex_sol_start']:
                d['q_or_a'] = 'a'

            b_skip = True
        
        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset(sort_y(bx)[-10:]) & myset(bxs.indent0r()) & myset(bxs.tiny()))
        ml = self.ymax_line(bx, w=(0.2, 0.4))
        return 0 if nr else self.ymin_skip1(bx), min(sort_y(nr)[-1][1], ml) if nr else ml 

    def post(self, d):
        self.post_func(d)

