# -*- coding: utf-8 -*-

from books import *

class sato(book):

    def __init__(self):
        super(sato, self).__init__()

        self.src = u'/home/cytu/usr/doc/math/prob/th/Sato K.-I. Levy Processes and Inifinitely Divisible Distributions.djvu' 
        self.pgs = range(12, 462)

        self.tokens.update({
            'defn': {'class': 'indent1',      
                     'ocr': r'^(DEFINITION (\d+\.\d+))\.?',
                    },
            
            'thm': {'class': 'indent1',      
                 'ocr': r'^((THEOREM|COROLLARY|LEMMA|PROPOSITION) (\d+\.\d+))\.?', 
                   },
            
            'proof': {'class': 'indent1',      
                      'ocr': r'^Proof', 
                     },

            'example': {'class': 'indent1',      
                        'ocr': r'^(EXAMPLE (\d+\.\d+))\.?', 
                       },

            'remark': {'class': 'indent1',      
                     'ocr': r'^(REMARK (\d+\.\d+))\.?',
                    },

            'ex': {'class': 'indent1',
                   'ocr': r'^E (\d+\.\d+)',
                  },

            'sol_start': {'class': 'first2',
                         'ocr': r'^Solutions to exercises$',
                         },
        })
        
    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['thm', 'proof', 'ex']:
            if tk in ['thm', 'ex']:
                d['k'] = k
                d['q_or_a'] = 'q'
                if d.get('sol', False):
                    d['q_or_a'] = 'a'
            else:
                d['q_or_a'] = 'a' 
        else:
            if tk == 'sol_start':
                d['sol'] = True
            b_skip = True

        return b_skip, d
    
    def ym(self, bx):
        return (self.ymin_skip1(bx), self.ymax_line(bx))
