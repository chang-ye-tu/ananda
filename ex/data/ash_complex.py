# -*- coding: utf-8 -*-

from books import *

class ash_complex(book):

    def __init__(self):
        super(ash_complex, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Ash/Complex Variables.pdf' 
        self.pgs = range(4, 208)
        self.morph0 = 'c100.5'
        self.tokens.update({
            'chapter': {'class': 'indent0', 
                        'ocr': r'^Chapter (\d+)$',
                       },

            'section': {'class': 'indent0', 
                        'ocr': r'^((\d+\.\d+) |Section (\d+\.\d+)$)',
                       },

            'subsection': {'class': 'indent0', 
                           'ocr': r'^(\d+\.\d+\.\d+) ',
                          },

            'proof': {'class': 'indent0',      
                      'ocr': r'^Proof', 
                     },

            'remark': {'class': 'indent0',      
                       'ocr': r'^Remark$', 
                      },
            
            'ref': {'class': 'indent0',      
                    'ocr': r'^References$', 
                   },

            'prob_start': {'class': 'indent0',      
                           'ocr': r'^Problems$', 
                          },
            
            'sol_start': {'class': 'indent0',      
                          'ocr': r'^Solutions$', 
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
            if tk == 'section':
                d['root'] = trim(k.replace('Section', ''))
            elif tk == 'sol_start':
                d['q_or_a'] = 'a'
            elif tk == 'prob_start':
                d['q_or_a'] = 'q'
            b_skip = True

        return b_skip, d
