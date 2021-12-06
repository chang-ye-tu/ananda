# -*- coding: utf-8 -*-

from books import *

class suhov1(book):
    
    def __init__(self):
        super(suhov1, self).__init__()

        #self.src = "/home/cytu/usr/doc/math/prob/th/Suhov Y., Kelbert M. Probability and Statistics by Example I Basic Probability and Statistics 2ed.pdf"
        self.src = "/home/cytu/usr/doc/math/prob/th/Suhov Y., Kelbert M. Probability and Statistics by Example 1 Basic Probability and Statistics.pdf"
        self.pgs = range(15, 358)

        self.morph0 = 'c150.8'

        self.tokens.update({
            'chapter': {'class': 'top',
                        'ocr' : r'^\d+ ',
                       },

            'section': {'class': 'indent0',
                        'ocr': r'^\d+\.\d+',
                        },

            'prob': {'class': 'indent0',
                     'ocr': '^Problem (\d+\.\d+)',
                    },
            
            'sol':  {'class': 'indent0', 
                     'ocr': r'^Solution',
                      },

            'ans':  {'class': 'indent1', 
                     'ocr': r'^Answer',
                    },
            
            'remark': {'class': 'indent0',
                       'ocr': r'^Remark',
                      },
            
            'example': {'class': 'indent0',
                        'ocr': '^(Example (\d+\.\d+))',
                       },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['prob', 'sol', 'ans']:
            if tk == 'prob':
                d['q_or_a'] = 'q'
                d['k'] = k
            else:
                d['q_or_a'] = 'a'

        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
