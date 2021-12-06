# -*- coding: utf-8 -*-

from books import *

class casella(book):

    def __init__(self):
        super(casella, self).__init__()

        self.src = '/home/cytu/usr/doc/math/prob/appl/Casella/Casella G., Berger R. Statistical Inference 2ed.pdf'
        self.pgs =  range(28, 883)#range(219, 231) + range(732, 745)
        self.tokens.update({
            'prob_sol':  {'class': 'indent0', 
                         'ocr': r'^(\d+\.\d+) ',
                         },
            
            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+\.\d+))',
                    },

            'example': {'class': 'indent0',      
                        'ocr': r'^(Example (\d+\.\d+\.\d+))',
                       },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Theorem|Corollary|Proposition) (\d+\.\d+\.\d+))',
                   },

            'proof': {'class': 'indent0',      
                     'ocr': r'^Proof', 
                     },

            'sol_start': {'class': 'first2',
                'ocr': r'^Solutions Manual for$',
                },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        if tk in ['thm', 'proof', 'prob_sol']:
            if tk == 'thm':
                d['q_or_a'] = 'q'
                d['k'] = k
            elif tk == 'prob_sol':
                d['q_or_a'] = d.get('sol', 'q')
                d['k'] = k
            else:
                d['q_or_a'] = 'a'
        else:
            if tk in ['sol_start']:
                d['sol'] = 'a'

            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
