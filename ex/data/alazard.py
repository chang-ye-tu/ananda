from books import *

class alazard(book):
    
    def __init__(self):
        super().__init__()
        
        self.pgs = range(15, 425)
        self.morph0 = 'c100.8'

        self.src = "/home/cytu/usr/doc/math/anly/th/Alazard/Alazard T. Analysis and Partial Differential Equations.pdf"
        
        self.tokens.update({
            'chap': {'class': 'top',      
                    'ocr': r'^(Chapter \d+)', 
                    },

            'section': {'class': 'indent0',      
                        'ocr': r'^(\d+\.\d+) ', 
                       },

            'subsection': {'class': 'indent0',      
                           'ocr': r'^(\d+\.\d+\.\d+) ', 
                          },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+))', 
                   },
            
            'remark': {'class': 'indent0',      
                    'ocr': r'^(Remark (\d+\.\d+))', 
                   },

            'example': {'class': 'indent0',      
                        'ocr': r'^(Example (\d+\.\d+))', 
                    },

            'defn': {'class': 'indent0',      
                     'ocr': r'^((Deﬁnition|Definition) (\d+\.\d+))', 
                    },
            
            'proof': {'class': 'indent0', 
                      'ocr': r'^Proof',
                     },

            'ex': {'class': 'indent0', 
                   'ocr': r'^(Exercise (\(solved\))? (\d+\.\d+))',
                  },
            
            'sol': {'class': 'indent0', 
                    'ocr': r'^Solution \d+ \(Solution to Exercise (\d+\.\d+)\)',
                   },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'ex', 'sol']:
            if tk == ['thm', 'ex']:
                d['q_or_a'] = 'q'
                d['k'] = k.strip() if tk == 'thm' else k.replace('(solved)', '').strip()

            elif tk == 'proof':
                d['q_or_a'] = 'a'

            elif tk == 'sol':
                d['q_or_a'] = 'a'
                d['k'] = 'Exercise ' + k

        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        return self.ymin_skip1(bx), self.ymax_line(bx, w=(0.35, 0.45)) 
