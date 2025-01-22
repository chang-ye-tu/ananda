from books import *

class ferguson_opt(book):
    
    def __init__(self):

        super(ferguson_opt, self).__init__()
        
        self.pgs = range(142)
        self.morph0 = 'c150.8'
        self.range_indent1 = (4e-2, 7e-2)

        self.src = "/home/cytu/usr/doc/math/prob/appl/seq/ferguson/Ferguson T. S. Optimal Stopping and Applications.pdf"
        
        self.tokens.update({
            'chapter': {'class': 'first2', 
                        'ocr': r'^Chapter (\d+)',
                       },

            'ex_start': {'class': 'indent1',      
                         'ocr': r'^[\$09]\d+\.\d+ Exercises\.', 
                        },

            'sol_start': {'class': 'indent1',      
                          'ocr': r'^Solutions to the Exercises of Chapter (\d+)\.$', 
                         },

            'sec': {'class': 'indent1',      
                    'ocr': r'^[\$09](\d+\.\d+)\.? ', 
                   },

            'ex_sol': {'class': 'indent1',      
                       'ocr': r'^(\d+)\. ', 
                      },

            'def': {'class': 'indent0',      
                    'ocr': r'^Definition\.? ', 
                   },
            
            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem) \d+)\.?', 
                   },
            
            'proof': {'class': 'indent0', 
                      'ocr': r'^Proof',
                     },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof', 'ex_sol']:
            if tk == 'thm':
                d['q_or_a'] = 'q'
                d['k'] = 'Chapter %s, %s' % (d['chapter'], k.strip()) 
            elif tk == 'proof':
                d['q_or_a'] = 'a'
            else:
                d['q_or_a'] = 'q' if d.get('ex_start', False) else 'a'
                d['k'] = '.'.join([d['chapter'], k.strip()])

        elif tk in ['ex_start', 'sol_start', 'chapter']:
            if tk in ['chapter', 'sol_start']:
                d['chapter'] = k.strip()
                d['ex_start'] = False
            elif tk == 'ex_start':
                d['ex_start'] = True
            b_skip = True

        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        chap = self.bxs(bx).line(w=(0.99, 1))
        ml = self.ymax_line(bx, w=(0.14, 0.16))
        return 0 if chap else self.ymin_skip1(bx), ml#min(sort_y(bx)[-2][1], ml) if chap else ml 
