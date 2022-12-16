# -*- coding: utf-8 -*-

from books import *

class taocp4A(book):
    
    def __init__(self):
        super(taocp4A, self).__init__()
        
        self.pgs = range(17, 834)
        self.src = '/home/cytu/usr/doc/math/dscr/cs/Knuth/TAOCP/TAOCP 4A.pdf'
        
        self.range_indent0 = (0., 5e-2) # because of scattered stars and wedges
        self.tokens.update({
            'section': {'class': 'indent0', 
                        'ocr': r'^((\d+\.){2,4}) ',
                       },

            'alg': {'class': 'indent0',      
                    'ocr': r'^((Subroutine|Algorithm) (\w+))', 
                   },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\w+))', 
                   },
            
            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                      },
            
            'ex_sec': {'class': 'allbx',
                         'ocr': r'^EXERCISES$',
                        },
            
            'ex_ans': {'class': 'allbx',
                       'ocr': r'^[P?>]?[ ]?(\d+)\. ',
                      },

            'ans_start': {'class': 'allbx',
                          'ocr': '^ANSWERS TO EXERCISES$',
                         },

            'ans_sec': {'class': 'indent0', 
                        'ocr': '^SECTION ([.0-9]+)$',
                       },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'alg', 'ex_ans']:
            if tk in ['thm', 'proof', 'alg']:
                if tk == 'thm':
                    d['q_or_a'] = 'q'
                    d['k'] = k
                else:
                    d['q_or_a'] = 'a'
            else:
                eoa = d.get('ex_or_ans', '')
                d['q_or_a'] = 'q' if eoa == 'ex' else 'a'  
                d['k'] = '.'.join([d['root'], trim(k)]) 
             
        else:
            if tk in ['ans_sec', 'section']:
                d['root'] = trim(k)
                if tk == 'ans_sec':
                    d['ex_or_ans'] = 'ans'
            
            elif tk == 'ex_sec':
                d['ex_or_ans'] = 'ex'

            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.centerh()) & myset(bxs.tiny()))
        return (0 if nr else self.ymin_skip1(bx), sort_y(nr)[-1][1] if nr else self.ymax_line(bx))
