# -*- coding: utf-8 -*-

from books import *

class suhov2(book):
    
    def __init__(self):
        super(suhov2, self).__init__()

        self.src = "/home/cytu/usr/doc/math/prob/th/Suhov Y., Kelbert M. Probability and Statistics by Example 2 Markov Chains A Primer in Random Processes and their Applications.pdf"

        self.pgs = range(12, 490)

        self.morph0 = 'c150.6'

        self.tokens.update({
            'chapter': {'class': 'top',
                        'ocr': r'^\d+$',
                        },

            'thm': {'class': 'indent0',
                    'ocr': r'^((Lemma|Theorem) (\d+\.\d+\.\d+))',
                   },

            'section': {'class': 'centerh',
                        'ocr': r'^\d+\.\d+',
                        },

            'question': {'class': 'indent0',
                         'ocr': r'^(Question (\d+\.\d+\.\d+))',
                        },

            'sol':  {'class': 'indent0', 
                     'ocr': r'^Solution',
                      },

            'proof': {'class': 'indent0',
                      'ocr': r'^Proof',
                      },

            'def': {'class': 'indent0', 
                    'ocr': r'^(Deﬁnition (\d+\.\d+\.\d+))',
                   },

            'remark': {'class': 'indent0',
                       'ocr': r'^(Remark (\d+\.\d+\.\d+))',
                      },

            'worked_ex': {'class': 'indent0',
                           'ocr': r'^(Worked Example (\d+\.\d+\.\d+))',
                       },

            'example': {'class': 'indent0',
                        'ocr': r'^(Example (\d+\.\d+\.\d+))',
                       },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['question', 'thm', 'sol', 'proof', 'worked_ex']:
            if tk in ['question', 'thm', 'worked_ex']:
                d['q_or_a'] = 'q'
                d['k'] = k
            else:
                d['q_or_a'] = 'a'

        else:
            b_skip = True

        return b_skip, d
