from books import *

class schilling_bm(book):
    
    def __init__(self):
        super(schilling_bm, self).__init__()
        
        self.morph0 = 'c150.6' 

        self.pgs = list(range(15, 516)) + list(range(540, 772))

        self.src = "/home/cytu/usr/doc/math/prob/th/Schilling/schilling_bm.pdf"

        self.tokens.update({
            'section': {'class': 'indent0',
                        'ocr': r'^(\d+) ',
                       },
            
            'thm': {'class': 'indent0',      
                    'ocr': r'^(((\d+|[A])\.\d+) (Lemma|Corollary|Theorem|Proposition|Algorithm))', 
                   },

            'remark': {'class': 'indent0',      
                       'ocr': r'^(((\d+|[A])\.\d+) Remark)', 
                      },

            'def': {'class': 'indent0',      
                    'ocr': r'^(((\d+|[A])\.\d+) (Deﬁnition|Definition))',
                   },

            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                      },


            'ex': {'class': 'indent0',      
                   'ocr': r'^(((\d+|[A])\.\d+) (Example|Epilogue))', 
                  },
            
            'prob': {'class': 'indent0',
                     'ocr': r'^(\d+)\. ',
                    },
            
            'sol': {'class': 'indent0',
                    'ocr': r'^Problem (\d+\.\d+)\. Solution',
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
                d['k'] = k if tk == 'sol' else (d.get('sec', '0') + '.' + k) 
        else:
            if tk == 'section':
                d['sec'] = k
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[0]]) & myset(bxs.tiny()))
        return self.ymin_skip1(bx), self.ymax_skip1(bx) if nr else self.ymax_line(bx)
