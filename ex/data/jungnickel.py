from books import *

class jungnickel(book):
    
    def __init__(self):
        super(jungnickel, self).__init__()
        
        self.pgs = range(21, 642)
        self.src = "/home/cytu/usr/doc/math/dscr/cmb/Jungnickel D. Graphs Networks and Algorithms 4ed.pdf"
        self.tokens.update({
            'chapter': {'class': 'top',
                        'ocr': r'^\d+$',
                       },
            
            'section': {'class': 'indent0', 
                        'ocr': r'^\d+\.\d+ ',
                       },

            'alg': {'class': 'indent0',      
                    'ocr': r'^((Algorithm) (\d+\.\d+\.\d+))\.?', 
                   },

            'prob': {'class': 'indent0',      
                     'ocr': r'^((Problem) (\d+\.\d+\.\d+))\.?', 
                       },

            'example': {'class': 'indent0',      
                        'ocr': r'^((Example) (\d+\.\d+\.\d+))\.?', 
                       },

            'remark': {'class': 'indent0',      
                        'ocr': r'^((Remark) (\d+\.\d+\.\d+))\.?', 
                       },

            'defn': {'class': 'indent0',      
                     'ocr': r'^((Deﬁnition) (\d+\.\d+\.\d+))\.?', 
                    },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition|Result) (\d+\.\d+\.\d+))\.?', 
                   },
            
            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                      },
            
            'ex': {'class': 'indent0',
                   'ocr': r'^Exercise (\d+\.\d+\.\d+)\.?',
                  },
            
            'sol_start': {'class': 'indent0',
                          'ocr': '^SOLUTIONS$',
                         },
            
            'sol_sec': {'class': 'indent0',
                        'ocr': r'^B\.\d+ Solutions for Chapter \d+$',
                       },

            'sol': {'class': 'indent0',
                    'ocr': r'^(\d+\.\d+\.\d+) ',
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
                    d['k'] = k
                else:
                    d['q_or_a'] = 'a'
            else:
                d['q_or_a'] = 'q' if tk == 'ex' else 'a'  
                d['k'] = k 
             
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_chap(bx), self.ymax_line(bx)
