from books import *

class zalinescu(book):
    
    def __init__(self):
        super(zalinescu, self).__init__()
        
        self.pgs = range(20, 368)
        self.morph0 = 'c150.6'

        #self.src = u"/home/cytu/usr/doc/math/or/Zălinescu C. Convex Analysis in General Vector Spaces.djvu"
        self.src = u"/home/cytu/usr/doc/math/or/Zalinescu C. Convex Analysis in General Vector Spaces.djvu"

        self.tokens.update({
            'chap': {'class': 'top',      
                    'ocr': r'^(Chapter \d+)', 
                    },

            'sol_start': {'class': 'top',
                         'ocr': '^Exercises ',
                         },
            
            'sec': {'class': 'indent0',      
                    'ocr': r'^\d+\.\d+ ', 
                   },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+\.\d+))', 
                    },
            
            'thm': {'class': 'indent0',      
         'ocr': r'^((Lemma|Corollary|Theorem|Pr[0o]p[0o]sition) (\d+\.\d+\.\d+))', 
                   },
            
            'example': {'class': 'indent0',      
                        'ocr': r'^(Example (\d+\.\d+\.\d+))', 
                   },

            'proof': {'class': 'indent0', 
                      'ocr': r'^Proof',
                     },
            
            'ex_sol': {'class': 'indent0',      
                        'ocr': r'^(Exercise (\d+\.\d+))', 
                   },

            'remark': {'class': 'indent0',      
                       'ocr': r'^(Remark (\d+\.\d+\.\d+))', 
                   },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'ex_sol', 'proof']:
            if tk in ['thm']:
                d['q_or_a'] = 'q'
                d['k'] = k.strip()

            elif tk == 'proof':
                d['q_or_a'] = 'a'

            elif tk == 'ex_sol':
                d['q_or_a'] = 'a' if d.get('sol_start', False) else 'q'
                d['k'] = k.strip()
        else:
            if tk == 'sol_start':
                d['sol_start'] = True
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        ml = self.ymax_line(bx, w=(0.30, 0.31))
        return self.ymin_skip1(bx), ml 
