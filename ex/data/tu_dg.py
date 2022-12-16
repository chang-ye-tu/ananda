# -*- coding: utf-8 -*-

from books import *

class tu_dg(book):

    def __init__(self):
        super(tu_dg, self).__init__()

        self.src = u'/home/cytu/usr/doc/math/geo/Tu W.-L. Differential Geometry Connections Curvature and Characteristic Classes.pdf'
        self.pgs = range(17, 340)
        self.tokens.update({
            'chap':  {'class': 'indent0', 
                      'ocr': r'^(Chapter|Appendix) ',
                     },

            'sec':  {'class': 'indent0', 
                     'ocr': r'^§(( )?(\d+|[AB])) ',
                    },

            'subsec_sol':  {'class': 'indent0', 
                            'ocr': r'^((\d+|[AB])\.\d+)(\*)? ',
                           },
            
            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition ((\d+|[AB])\.\d+))',
                    },

            'ex': {'class': 'indent0',      
                   'ocr': r'^(Exercise ((\d+|[AB])\.\d+))(\*)?',
                  },

            'prob': {'class': 'indent0',      
                     'ocr': r'^((\d+|[AB])\.\d+)\.',
                    },

            'remark': {'class': 'indent0',      
                       'ocr': r'^(Remark ((\d+|[AB])\.\d+))',
                      },
            
            'example': {'class': 'indent0',      
                        'ocr': r'^(Example ((\d+|[AB])\.\d+))',
                       },

            'example_plain': {'class': 'indent0',      
                              'ocr': r'^(Example)\.',
                             },
            
            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Theorem|Corollary|Proposition) ((\d+|[AB])\.\d+))',
                   },

            'proof': {'class': 'indent0',      
                      'ocr': r'^Proof', 
                     },
            
            'prob_begin': {'class': 'indent0',      
                           'ocr': r'^Problems$',
                          },

            'prob_sol_begin': {'class': 'indent0',      
                               'ocr': r'^Hints and Solutions to ',
                              },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        if tk in ['thm', 'ex', 'prob', 'proof']:
            if tk in ['thm', 'ex', 'prob']:
                d['q_or_a'] = 'q'
                d['k'] = k
            
            else:
                d['q_or_a'] = 'a'
        
        elif tk in ['subsec_sol']:
            if d.get('prob_sol_begin', False):
                d['q_or_a'] = 'a'
                d['k'] = k 
            
            else:
                b_skip = True
        
        else:
            if tk == 'prob_sol_begin':
                d['prob_sol_begin'] = True
            
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
