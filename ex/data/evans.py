# -*- coding: utf-8 -*-

from books import *

class evans(book):

    def __init__(self):
        super(evans, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Evans/Evans L. Partial Differential Equations 2ed.djvu' 
        self.pgs = range(18, 743)
        self.range_tinyw = (3e-2, 5e-2)
        self.range_indent0r = (0., 8e-2)
        self.range_lineh = (0, 3)
        self.morph0 = 'c100.5'
        self.tokens.update({
            'chapter':  {'class': 'first2', 
                         'ocr': r'^Chapter (\d+)$',
                        },

            'section':  {'class': 'indent0', 
                         'ocr': r'^((\d+|[A-E])[ ]?\.[ ]?\d+[ ]?\.[ ]?(\d+\.)?)',
                        },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((THEOREM|COROLLARY|LEMMA) (\d+)?)\.?', 
                   },
            
            'example': {'class': 'indent0',      
                        'ocr': r'^(Example (\d+))\.?', 
                       },

            'defn': {'class': 'indent0',      
                     'ocr': r'^DEFINITIONS?',
                    },

            'notation': {'class': 'indent0',      
                         'ocr': r'^NOTATION', 
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
                d['k'] = ' '.join([d['root'], k])
            else:
                d['q_or_a'] = 'a' 
        else:
            if tk == 'section':
                d['root'] = trim(k)
            b_skip = True

        return b_skip, d
    
    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.indent0r()) & myset(bxs.tiny()))
        return self.ymin_skip1(bx) if nr else self.ymin_line(bx), sort_y(bx)[-2][1] if nr else self.ymax_line(bx)
