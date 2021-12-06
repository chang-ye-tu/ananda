# -*- coding: utf-8 -*-

from books import *

class tu_manifolds(book):

    def __init__(self):
        super(tu_manifolds, self).__init__()

        self.src = u'/home/cytu/usr/doc/math/geo/Tu W.-L. An Introduction to Manifolds 2ed.pdf'
        self.pgs = range(21, 402)
        self.tokens.update({
            'chap':  {'class': 'indent0', 
                      'ocr': r'^(Chapter|Appendix) ',
                     },

            'sec':  {'class': 'indent0', 
                     'ocr': r'^§(( )?(\d+|[A-E])) ',
                    },

            'subsec_sol':  {'class': 'indent0', 
                            'ocr': r'^((\d+|[A-E])\.\d+)(\*)? ',
                           },
            
            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition ((\d+|[A-E])\.\d+))',
                    },

            'ex': {'class': 'indent0',      
                   'ocr': r'^(Exercise ((\d+|[A-E])\.\d+))(\*)?',
                  },

            'prob': {'class': 'indent0',      
                     'ocr': r'^((\d+|[A-E])\.\d+)\.',
                    },

            'remark': {'class': 'indent0',      
                       'ocr': r'^(Remark ((\d+|[A-E])\.\d+))',
                      },
            
            'remarks': {'class': 'indent0',      
                         'ocr': r'^(Remarks)\.',
                        },

            'example': {'class': 'indent0',      
                        'ocr': r'^(Example ((\d+|[A-E])\.\d+))',
                       },

            'examples': {'class': 'indent0',      
                         'ocr': r'^(Examples|Example)\.',
                        },
            
            'notation': {'class': 'indent0',      
                         'ocr': r'^(NOTATION)\.',
                        },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Theorem|Corollary|Proposition) ((\d+|[A-E])\.\d+))',
                   },

            'proof': {'class': 'indent0',      
                      'ocr': r'^(Proof|Solution)', 
                     },
            
            'prob_begin': {'class': 'indent0',      
                           'ocr': r'^Problems$',
                          },

            'ex_sol_begin': {'class': 'indent0',      
                             'ocr': r'^Solutions to Selected',
                            },
            
            'prob_sol_begin': {'class': 'indent0',      
                                'ocr': r'^Hints and Solutions to ',
                               },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        if tk in ['thm', 'ex', 'prob', 'example', 'proof']:
            if tk in ['thm', 'ex', 'prob', 'example']:
                d['q_or_a'] = 'q'
                d['k'] = k
            
            else:
                d['q_or_a'] = 'a'
        
        elif tk in ['subsec_sol']:
            if d.get('ex_sol_begin', False):
                d['q_or_a'] = 'a'
                d['k'] = k if d.get('prob_sol_begin', False) else ('Exercise ' + k)
            
            else:
                b_skip = True
        
        else:
            if tk == 'ex_sol_begin':
                d['ex_sol_begin'] = True

            elif tk == 'prob_sol_begin':
                d['prob_sol_begin'] = True
            
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
