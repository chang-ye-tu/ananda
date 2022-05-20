from books import *

class zastawniak(book):
    
    def __init__(self):
        super(zastawniak, self).__init__()
        
        self.pgs = range(9, 225)

        self.src = u"/home/cytu/usr/doc/econ/Capiński-Kopp/Brzezniak Z., Zastawniak T. Basic Stochastic Processes A Course Through Exercises.pdf"

        self.tokens.update({
            'chapter': {'class': 'first',
                        'ocr': r'^\d+$',
                       },
            
            'section': {'class': 'indent0',      
                        'ocr': r'^\d+\.\d+ ', 
                       },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+))', 
                   },

            'ex': {'class': 'indent0',      
                    'ocr': r'^Exercise (\d+\.[ ]?\d+)', 
                   },

            'sol': {'class': 'indent0',      
                    'ocr': r'^Solution (\d+\.[ ]?\d+)', 
                   },

            'remark': {'class': 'indent0',      
                       'ocr': r'^(Remark (\d+\.\d+))',
                   },

            'example': {'class': 'indent0',      
                        'ocr': r'^(Example (\d+\.\d+))',
                   },
            
            'def': {'class': 'indent0',      
                    'ocr': r'^((Deﬁnition|Definition) (\d+\.\d+))',
                   },

            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                      },
            
            'hint':  {'class': 'indent0', 
                       'ocr': r'^Hint',
                     },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'ex', 'sol']:
            if tk in ['thm', 'proof']:
                if tk == 'thm':
                    d['q_or_a'] = 'q'
                    if tk == 'thm':
                        d['k'] = k
                else:
                    d['q_or_a'] = 'a'
            else:
                d['q_or_a'] = 'q' if tk == 'ex' else 'a'  
                d['k'] = trim(k) 
             
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.centerh()) & myset(bxs.tiny()))
        ml = self.ymax_line(bx)
        return 0 if nr else self.ymin_line(bx), min(sort_y(nr)[-1][1], ml) if nr else ml 
