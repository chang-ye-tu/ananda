# -*- coding: utf-8 -*-

from books import *

class ash_ca(book):

    def __init__(self):
        super(ash_ca, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Ash/Commutative Algebra.pdf' 
        self.pgs = range(4, 99)
        self.morph0 = 'c100.5'
        self.tokens.update({
            'chapter': {'class': 'indent0', 
                        'ocr': r'^Chapter (\d+)$',
                       },

            'section': {'class': 'indent0', 
                        'ocr': r'^(\d+\.\d+) ',
                       },

            'subsection': {'class': 'indent0', 
                           'ocr': r'^(\d+\.\d+\.\d+) ',
                          },

            'proof': {'class': 'indent0',      
                      'ocr': r'^Proof', 
                     },

            'prob_start': {'class': 'first2',      
                           'ocr': r'^Exercises$', 
                          },
            
            'sol_start': {'class': 'first2',      
                          'ocr': r'^Solutions to Problems$', 
                         },

            'prob_sol': {'class': 'indent0',
                         'ocr': r'^(\d+)\. ',
                        },
        })
        
    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['prob_sol', 'subsection', 'proof']:
            if tk == 'prob_sol':
                d['k'] = ' '.join([d['root'], k])
            elif tk == 'subsection':
                d['q_or_a'] = 'q'
                d['k'] = k
            elif tk == 'proof':
                d['q_or_a'] = 'a'

        else:
            if tk == 'chapter':
                d['root'] = trim(k)
            elif tk == 'sol_start':
                d['q_or_a'] = 'a'
            elif tk == 'prob_start':
                d['q_or_a'] = 'q'
            b_skip = True

        return b_skip, d
