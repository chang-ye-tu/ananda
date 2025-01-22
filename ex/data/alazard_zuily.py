from books import *

class alazard_zuily(book):
    
    def __init__(self):
        super(alazard_zuily, self).__init__()
        self.src = "/home/cytu/usr/doc/math/anly/th/Alazard/Alazard T., Zuily C. Tools and Problems in Partial Differential Equations.pdf"
        self.range_indent1 = (3e-2, 6e-2)
        self.pgs = range(13, 357)

        self.tokens.update({
            'chapter': {'class': 'top',
                        'ocr': r'^Chapter (\d+)',
                        },
                        
            'section': {'class': 'indent0', 
                        'ocr': r'^(\d+\.\d+) ',
                        },

            'subsection': {'class': 'indent0', 
                           'ocr': r'^(\d+\.\d+\.\d+) ',
                          },
            
            'subsubsection': {'class': 'indent0', 
                           'ocr': r'^(\d+\.\d+\.\d+\.\d+) ',
                          },
            
            'prob':  {'class': 'indent1',
                      'ocr': r'^Problem (\d+)',},

            'sol': {'class': 'indent1',
                    'ocr': r'^Solution (\d+)',
                    },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['prob', 'sol']:
            if tk == 'prob':
                d['q_or_a'] = 'q' 
            else:
                d['q_or_a'] = 'a'

            d['k'] = k

        else:
            b_skip = True
        
        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset(sort_y(bx)[-10:]) & myset(bxs.indent0r()) & myset(bxs.tiny()))
        ml = self.ymax_line(bx, w=(0.2, 0.4))
        return 0 if nr else self.ymin_skip1(bx), min(sort_y(nr)[-1][1], ml) if nr else ml 

    def post(self, d):
        self.post_func(d)
