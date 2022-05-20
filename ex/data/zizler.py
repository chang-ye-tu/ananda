from books import *

class zizler(book):
    
    def __init__(self):
        super(zizler, self).__init__()
        
        self.pgs = range(27, 853)
        self.morph0 = 'c100.6'
        self.range_indent1 = (0., 0.045)

        self.src = u"/home/cytu/usr/doc/math/anly/th/Montesinos V., Zizler P., Zizler V. An Introduction to Modern Analysis.pdf"
        
        self.tokens.update({
            'sec': {'class': 'indent0',      
                    'ocr': r'^(\d+\.\d+\.\d+(\.\d+)? )', 
                   },

            'ex': {'class': 'indent0',      
                    'ocr': r'^13\.\d+', 
                   },

            'sol': {'class': 'indent1',      
                    'ocr': r'^H[ ]?int\.', 
                   },

            'thm': {'class': 'indent0',      
             'ocr': r'^((Lemma|Corollary|Theorem|Proposition|Fact) (\d+)) ', 
                   },
            
            'defn': {'class': 'indent0',      
                     'ocr': r'^(Definition (\d+)) ', 
                    },
            
            'remark': {'class': 'indent0',      
                    #'ocr': r'^(Remark (\d+))', 
                    'ocr': r'^Remark ', 
                   },

            'example': {'class': 'indent0',      
                        'ocr': r'^(Example (\d+)) ', 
                   },

            'proof': {'class': 'indent0', 
                      'ocr': r'^Proof',
                     },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'ex', 'proof', 'sol']:
            if tk in ['thm', 'ex']:
                d['q_or_a'] = 'q'
                d['k'] = k.strip()
            else:
                d['q_or_a'] = 'a'

        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        ml = self.ymax_line(bx, w=(0.30, 0.31))
        return self.ymin_skip1(bx), ml 
