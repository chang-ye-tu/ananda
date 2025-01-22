from books import *

def remove_last_dot(s):
    return s if s[-1] != '.' else s[:-1]

class asmar(book):
    
    def __init__(self):
        super(asmar, self).__init__()
        
        self.pgs = range(9, 1099)
        self.morph0 = 'c150.9'

        self.src = "/home/cytu/usr/doc/math/anly/th/Asmar N. H., Grafakos L. Complex Analysis with Applications_with_sol.pdf"
        
        self.tokens.update({
            'chap': {'class': 'top',      
                    'ocr': r'^(Chapter \d+)', 
                    },

            'ex_start': {'class': 'indent0',
                         'ocr': r'^Exercises (\d+\.\d+)',
                         },
            
            'ex': {'class': 'allbx',
                   'ocr': r'^\d+\.',
                },

            'ex_sol_start': {'class': 'first2',
                             'ocr': r'^Solutions to Kxercises (\d+\.\d+)',
                         },

            'sec': {'class': 'indent0',      
                    'ocr': r'^(\d+\.\d+(\.\d+)?)', 
                   },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+\.\d+\.))', 
                   },
            
            'remark': {'class': 'indent0',      
                    'ocr': r'^(Remark (\d+\.\d+\.\d+\.))', 
                   },

            'exmp': {'class': 'indent0',      
                    'ocr': r'^(Example (\d+\.\d+\.\d+\.))', 
                   },

            'exmp_sol': {'class': 'indent0',      
                    'ocr': r'^Solution\.', 
                   },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Definition (\d+\.\d+\.\d+\.))', 
                    },
            
            'proof': {'class': 'indent0', 
                      'ocr': r'^Proof',
                     },

            'hist': {'class': 'centerh', 
                      'ocr': r'^HISTORICAL NOTES',
                     },

        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'exmp', 'exmp_sol', 'ex', 'ex_sol_start', 'ex_start']:
            if tk in ['thm', 'exmp']:
                d['q_or_a'] = 'q'
                d['k'] = remove_last_dot(k.strip())
            elif tk in ['ex_sol_start', 'ex_start']:
                d['ex_prefix'] = k.strip()
                d['q_or_a'] = 'q' if tk == 'ex_start' else 'a'
                b_skip = True
            elif tk == 'ex':
                d['k'] = d.get('ex_prefix', '') + '.' + remove_last_dot(k.strip())
            else:
                d['q_or_a'] = 'a'
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        #nr = list(myset(sort_y(bx)[-3:]) & myset(bxs.tiny()) & myset(bxs.indent0r()))
        ml = self.ymax_line(bx, w=(0.30, 0.31))
        #return 0 if nr else self.ymin_skip1(bx), min(sort_y(bx)[-3][1], ml) if nr else ml 
        return self.ymin_skip1(bx), ml 
