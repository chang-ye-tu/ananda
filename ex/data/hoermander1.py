from books import *

class hoermander1(book):
    
    def __init__(self):
        super(hoermander1, self).__init__()
        
        self.pgs = range(14, 427)
        self.src = u"/home/cytu/usr/work/thesis/essential/Hoermander L. The Analysis of Linear Partial Differential Operators 1 Distribution Theory and Fourier Analysis 2ed.djvu"
        self.b_sep_heu = True

        self.tokens.update({
            'chapter': {'class': 'first2',      
                     'ocr': r'^((X|V|I)+)',
                    },

            #'section': {'class': 'indent0', 
            #            'ocr': r'^\d+\.\d+\.',
            #           },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+\.\d+)\.?)',
                    },

            'remark': {'class': 'indent0', 
                       'ocr': r'^Remark',
                      },
            
            'example': {'class': 'indent0', 
                        'ocr': r'^(Example (\d+\.\d+\.\d+)\.?)',
                       },

            'thm': {'class': 'indent0',      
                    'ocr': ur"^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+\.\d+[']?)\.?)", 
                   },
            
            'proof':  {'class': 'indent0', 
                       'ocr': r'^Proof',
                      },
            
            'notes': {'class': 'indent0', 
                      'ocr': r'^Notes',
                     },

            'ex': {'class': 'indent0', 
                   'ocr': r'^Exercise (\d+\.\d+\.\d+|\d+\.\d+)\.?',
                  },

            'ans_start': {'class': 'first2',      
                          'ocr': r'^Answers and Hints',
                    },
            
            'ex_sec': {'class': 'indent0', 
                       'ocr': r'^(Chapter|Section)',
                      },

            'ans': {'class': 'indent0', 
                   'ocr': r'^(\d+\.\d+\.\d+|\d+\.\d+)\.?',
                  },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ('thm', 'ex', 'ans'):
            d['q_or_a'] = 'a' if tk == 'ans' else 'q' 
            d['k'] = trim(k, True)
        
        elif tk in ('proof', ):
            d['q_or_a'] = 'a'

        else:
            b_skip = True
        
        return b_skip, d
