from books import *

class bertsekas_dual_sol(book):

    def __init__(self):
        super(bertsekas_dual_sol, self).__init__()

        self.src = '/home/cytu/usr/doc/math/or/Bertsekas/Convex Optimization/convexdualitysol.pdf'
        self.pgs = range(168)
        self.tokens.update({
            'section': {'class': 'indent0',      
                        'ocr': r'^(CHAPTER|SECTION|SRHCTION) ', 
                        },

            'ref': {'class': 'indent0',      
                        'ocr': r'^REFERENCES', 
                        },

            'ex': {'class': 'indent0',      
                   'ocr': r'^(\d+\.\d+)', 
                  },
            
            'sol': {'class': 'indent0',      
                    'ocr': r'^Solution', 
                   },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['ex', 'sol']: 
            if tk == 'sol':
                d['q_or_a'] = 'a'
            else:
                d['k'] = trim(k)
                d['q_or_a'] = 'q' 
        
        else: 
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return 0, self.ymax_line(bx, w=(0.3, 0.49)) 
