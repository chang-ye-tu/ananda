# -*- coding: utf-8 -*-

from books import *

class milman(book):
    
    def __init__(self):
        super(milman, self).__init__()
        
        self.pgs = range(18, 329)
        self.morph0 = 'c150.8'
        self.src = "/home/cytu/usr/doc/math/anly/th/Eidelman Y., Milman V., Tsolomitis A. Functional Analysis An Introduction.djvu"
        self.tokens.update({
            'chapter': {'class': 'indent0',
                        'ocr': r'^Chapter',
                       },
                        
            'section': {'class': 'indent0', 
                        'ocr': r'^\d+\.\d+[a-z]? ',
                       },

            'defn': {'class': 'indent0',      
                     'ocr': r'^Deﬁnition \d+\.\d+\.\d+',
                    },

            'remark': {'class': 'indent0', 
                       'ocr': r'^Remark \d+\.\d+\.\d+',
                      },

            'example': {'class': 'indent0', 
                        'ocr': r'^Example',
                       },

            'comment': {'class': 'indent0',
                        'ocr': r'^Comment',
                       },

            'thm': {'class': 'indent0',      
                    'ocr': r'((Lemma|Corollary|Theorem|Proposition|Property) (\d+\.\d+\.\d+))', 
                   },
            
            'proof':  {'class': 'indent1', 
                       'ocr': r'^Proof',
                      },
            
            'ex_start': {'class': 'indent0',
                         'ocr': r'^(\d+)\.\d+ Exercises',
                        },

            'sol_start': {'class': 'indent0',
                          'ocr': r'^A\.(\d+) Solutions to the exercises',
                         },
            
            'ex_sol': {'class': 'allbx',
                       'ocr': r'^(\d+)\.( |$)',
                      },
        })
        
        self.w_line = 0.9

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'ex_sol']:
            if tk == 'thm':
                d['q_or_a'] = 'q' 
                d['k'] = k
            
            elif tk == 'proof':
                d['q_or_a'] = 'a'
            
            else:
                s = d.get('ex_or_sol', '')
                if s:
                    d['q_or_a'] = 'q' if s == 'ex' else 'a'
                    d['k'] = 'ex ' + '.'.join([d['root'], k]) 

        else:
            if tk in ['ex_start', 'sol_start']:
                d['ex_or_sol'] = 'ex' if tk == 'ex_start' else 'sol'
                d['root'] = k

            b_skip = True
        
        return b_skip, d

    def ym(self, bx):
        return self.ymin_line(bx), sys.maxsize
