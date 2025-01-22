from books import *

class dreyfus(book):
    
    def __init__(self):
        super(dreyfus, self).__init__()
        
        self.pgs = range(17, 297)
        self.range_indent0 = (0, 5e-2)
        self.range_indent1 = (5e-2, 0.13)
        self.src = "/home/cytu/usr/doc/math/or/Dreyfus S., Law A. The Art and Theory of Dynamic Programming.pdf"
        self.tokens.update({
            'chapter': {'class': 'first2',      
                     'ocr': r'^Chapter (\d+)',
                    },

            'section': {'class': 'indent0', 
                       'ocr': r'^(\d+)\. ',
                      },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem) (\d+\.\d+))\.', 
                   },

            'proof': {'class': 'indent1', 
                      'ocr': r'^Pr[o0][o0]f',
                     },
            
            'prob': {'class': 'indent1',      
                     'ocr': r'^Prob[li]em (\d+\.\d+)\. ', 
                    },

            'prob_sol': {'class': 'indent0',      
                         'ocr': r'^(\d+\.\d+)\. ', 
                        },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'prob']:
            d['q_or_a'] = 'q'
            d['k'] = k 
        
        elif tk in ['proof', 'prob_sol']:
            d['q_or_a'] = 'a'
            if tk == 'prob_sol':
                d['k'] = k

        else:
            b_skip = True
        
        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.centerh()) & myset(bxs.tiny()))
        ml = self.ymax_line(bx)
        return 0 if nr else self.ymin_line(bx), min(sort_y(nr)[-1][1], ml) if nr else ml 
