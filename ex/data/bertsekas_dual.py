from books import *

class bertsekas_dual(book):
    
    def __init__(self):
        super(bertsekas_dual, self).__init__()
        
        self.pgs = range(11, 252)
        self.morph0 = 'c150.6'
        self.range_indent0 = (0., 1.2e-1)

        self.src = '/home/cytu/usr/doc/math/or/Bertsekas/Convex Optimization/Bertsekas D. P. Convex Optimization Theory.pdf'

        self.tokens.update({
            'chap': {'class': 'top',      
                    'ocr': r'^(\d+)', 
                    },

            'ind': {'class': 'indent0',      
                    'ocr': r'^(\d+\.\d+) ', 
                   },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+\.\d+))', 
                   },
            
            'remark': {'class': 'indent0',      
                       'ocr': r'^(Remark (\d+\.\d+\.\d+))', 
                      },

            'example': {'class': 'indent0',      
                        'ocr': r'^(Example (\d+\.\d+\.\d+))', 
                       },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Definition (\d+\.\d+\.\d+))', 
                    },
            
            'proof': {'class': 'indent0', 
                      'ocr': r'^Proof',
                     },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'defn', 'example']:
            if tk not in ['proof',]: 
                d['q_or_a'] = 'q'
                d['k'] = k.strip()
            else:
                d['q_or_a'] = 'a'
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        return self.ymin_skip1(bx), self.ymax_line(bx, w=(0.35, 0.45)) 
