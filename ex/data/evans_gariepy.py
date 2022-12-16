# -*- coding: utf-8 -*-

from books import *

class evans_gariepy(book):

    def __init__(self):
        super(evans_gariepy, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Evans/Evans L., Gariepy R. Measure Theory and Fine Properties of Functions rev.ed.pdf' 
        self.pgs = range(16, 304)
        self.range_tinyw = (1e-2, 5e-2)
        self.range_indent0r = (0., 8e-2)
        #self.range_lineh = (0, 3)
        self.morph0 = 'c100.5'
        self.tokens.update({
            'chapter':  {'class': 'first2', 
                         'ocr': r'^Chapter (\d+)$',
                        },

            'section':  {'class': 'indent0', 
                         'ocr': r'^(\d+[ ]?\.[ ]?\d+[ ]?(\.[ ]?\d+)?)',
                        },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((THEOREM|LEMMA) \d+\.\d+)', 
                   },
            
            'example': {'class': 'indent0',      
                        'ocr': r'^EXAMPLE', 
                       },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(DEFINITION \d+\.\d+)',
                    },

            'notation': {'class': 'indent0',      
                         'ocr': r'^NOTATION', 
                        },

            'warning': {'class': 'indent0',      
                         'ocr': r'^Warning', 
                        },

            'remark': {'class': 'indent0',
                       'ocr': r'^Remarks?',
                      },
            
            'proof': {'class': 'indent0',      
                      'ocr': r'^Proof', 
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
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.indent0r()) & myset(bxs.tiny()))
        return 0 if nr else self.ymin_skip1(bx), self.ymax_skip1(bx) if nr else sys.maxsize
