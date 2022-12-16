# -*- coding: utf-8 -*-

from books import *

class webster(book):
    
    def __init__(self):
        super(webster, self).__init__()
        
        self.pgs = range(18, 442)
        self.src = "/home/cytu/usr/doc/math/or/Webster R. Convexity.djvu"

        self.tokens.update({
            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem) (\d+\.\d+\.\d+))', 
                   },
            
            'example': {'class': 'indent0',      
                        'ocr': r'^((Example) (\d+\.\d+\.\d+))', 
                   },

            'sec': {'class': 'centerh', 
                    'ocr': r'^(\d+\.\d+) ',
                   },

            'proof': {'class': 'indent0', 
                      'ocr': r'^Pr[0o][0o]f',
                     },

            'sol': {'class': 'first2',
                    'ocr': r'^Solutions to exercises$',
                   },
            
            'ex_start': {'class': 'indent0',
                         'ocr': r'^Exercises (\d+\.\d+)$',
                          },

            'ex': {'class': 'indent0',
                   'ocr': r'^(\d+)\. ',
                    },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof',]:
            if tk == 'thm':
                d['q_or_a'] = 'q'
                d['k'] = k
            else:
                d['q_or_a'] = 'a'

        elif tk in ['ex']:
            d['k'] = 'ex ' + trim(d.get('root', '') + '.' + k)
             
        else:
            if tk == 'sol':
                d['sol'] = True
            elif tk == 'ex_start':
                d['q_or_a'] = 'a' if d.get('sol', False) else 'q'
                d['root'] = k
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx, w=(0.2, 0.4))
