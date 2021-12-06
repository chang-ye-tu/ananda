# -*- coding: utf-8 -*-

from books import *

class knapp_basic_real(book):
    
    def __init__(self):
        super(knapp_basic_real, self).__init__()
        
        self.pgs = range(20, 660)

        self.src = "/home/cytu/usr/doc/tech/me/Lebedev/Lebedev L., Cloud M., Eremeyev V. Tensor Analysis with Applications in Mechanics.pdf"

        self.tokens.update({
            'chapter': {'class': 'centerh',
                        'ocr': r'^C[Hh][Aa][Pp][Tt][Ee][Rr] (\w+)$',
                       },
            
            'app_start': {'class': 'top',
                           'ocr': r'^APPENDIX',
                        },
            
            'section': {'class': 'centerh', 
                        'ocr': r'^(A?\d+)\. ',
                       },

            'remark': {'class': 'indent1', 
                       'ocr': r'^REMARK',
                      },
            
            'example': {'class': 'indent1', 
                        'ocr': r'^EXAMPLE',
                       },

            'thm': {'class': 'indent1',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+))\.?', 
                   },

            'proof':  {'class': 'indent1', 
                       'ocr': r'^PROOF',
                      },
            
            'prob_start': {'class': 'centerh',
                           'ocr': r'^\d+\. Problems',
                          },

            'prob': {'class': 'indent0',
                     'ocr': r'^(\d+)\. ',
                    },
            
            'sol': {'class': 'indent1',
                    'ocr': r'^(\d+)\. ',
                   },

            'sol_start': {'class': 'centerh',
                          'ocr': '^HINTS FOR SOLUTIONS OF PROBLEMS$',
                          },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'prob', 'sol']:
            if tk in ['thm', 'proof']:
                if tk == 'thm':
                    d['q_or_a'] = 'q'
                    d['k'] = k if tk == 'thm' else (d.get('app', '') + ' ' + k)
                else:
                    d['q_or_a'] = 'a'
            else:
                pos = d.get('prob_or_sol', '')
                d['q_or_a'] = 'q' if pos == 'prob' else 'a'  
                d['k'] = '.'.join([d['root'], trim(k)]) 
             
        else:
            if tk == 'chapter':
                d['root'] = k
            elif tk == 'section':
                if k[0] == 'A':
                    d['app'] = k
            elif tk == 'prob_start':
                d['prob_or_sol'] = 'prob'

            elif tk == 'sol_start':
                d['prob_or_sol'] = 'sol'

            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.centerh()) & myset(bxs.tiny()))
        ml = self.ymax_line(bx)
        return 0 if nr else self.ymin_skip1(bx), min(sort_y(nr)[-1][1], ml) if nr else ml 
