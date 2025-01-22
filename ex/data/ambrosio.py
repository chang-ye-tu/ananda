from books import *

class ambrosio(book):

    def __init__(self):
        super(ambrosio, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Ambrosio/Ambrosio L., Da Prato G., Mennucci A. Introduction to Measure Theory and Integration.pdf' 
        self.pgs = range(12, 189)
        self.range_indent0 = (0, 5e-2)
        self.range_indent1 = (6e-2, 8e-2) 
        self.range_lineh = (5, 7)

        self.tokens.update({
            'thm': {'class': 'indent0',      
                    'ocr': r'^((Theorem|Corollary|Lemma|Proposition) (\d+\.\d+))\.?', 
                   },
            
            'example': {'class': 'indent0',      
                        'ocr': r'^(Example (\d+\.\d+))', 
                       },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition (\d+\.\d+))',
                    },

            'remark': {'class': 'indent0',      
                     'ocr': r'^(Remark (\d+\.\d+))',
                    },

            'proof': {'class': 'indent0',      
                      'ocr': r'^Proof', 
                     },

            'ex': {'class': 'indent0',      
                   'ocr': r'^(\d+\.\d+)[^.]', 
                  },

            'sol': {'class': 'indent0',      
                   'ocr': r'^Exercise (\d+\.\d+)', 
                  },

        })
        
    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['thm', 'ex',]:
            d['q_or_a'] = 'q'
            d['k'] = k
        elif tk in ['proof', 'sol']:
            d['q_or_a'] = 'a'
            if tk == 'sol':
                d['k'] = k
        else:
            b_skip = True

        return b_skip, d
