from books import *

class schilling_mims(book):
    
    def __init__(self):
        super(schilling_mims, self).__init__()
        
        self.morph0 = 'c150.6' 
        self.range_centerh = (0.48, 0.51)
        self.range_tinyw = (1e-2, 6e-2)

        self.pgs = list(range(20, 485)) + list(range(504, 842))

        self.src = "/home/cytu/usr/doc/math/prob/th/Schilling/schilling_mims.pdf"

        self.tokens.update({
            'chapter': {'class': 'first',
                        'ocr': r'^\d+$',
                       },
            
            'thm': {'class': 'indent0',      
                    'ocr': r'^((\*?[ ]?)(Lemma|Corollary|Theorem|Proposition|Properties|Scholium) ((\d+|[A-I])\.\d+))', 
                   },

            'remark': {'class': 'indent0',      
                       'ocr': r'^(Remark ((\d+|[A-I])\.\d+))', 
                      },

            'def': {'class': 'indent0',      
                    'ocr': r'^((Deﬁnition|Definition) ((\d+|[A-I])\.\d+))',
                   },

            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                      },

            'prob_start': {'class': 'indent0',
                           'ocr': r'^Problems$',
                          },

            'ex': {'class': 'indent0',      
                   'ocr': r'^((Example|Epilogue) ((\d+|[A-I])\.\d+))', 
                  },
            
            'prob': {'class': 'indent0',
                     'ocr': r'^(\d+\.\d+)\. ',
                    },
            
            'sol': {'class': 'indent0',
                    'ocr': r'^Problem (\d+\.\d+) Solution',
                   },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'prob', 'sol']:
            if tk in ['thm', 'proof']:
                if tk == 'thm':
                    d['q_or_a'] = 'q'
                    if tk == 'thm':
                        d['k'] = k
                else:
                    d['q_or_a'] = 'a'
            else:
                d['q_or_a'] = 'q' if tk == 'prob' else 'a'  
                d['k'] = k 
             
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.centerh()) & myset(bxs.tiny()))
        ml = self.ymax_line(bx)
        return 0 if nr else self.ymin_skip1(bx), min(sort_y(nr)[-1][1], ml) if nr else ml 
