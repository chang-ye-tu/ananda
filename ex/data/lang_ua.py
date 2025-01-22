from books import *

class lang_ua(book):
    
    def __init__(self):

        super().__init__()
        self.src = "/home/cytu/usr/doc/math/alg/Lang/Lang S. Undergraduate Analysis 2ed.pdf"
        self.pgs = range(16, 645)

        self.morph0 = 'c100.5'

        self.tokens.update({
            'chapter':  {'class': 'indent0',
                         'ocr' : r'^CHAPTER (\w+)$',
                        },
            
            'section':  {'class': 'indent0', 
                         'ocr': r'^\w+, [8\$§](\d+)\. ',
                        },

            'thm': {'class': 'indent1', 
                     'ocr': r'^((Proposition|Theorem|Corollary|Lemma) (\d+\.\d+))',
                    },
            
            'proof': {'class': 'indent1', 
                      'ocr': r'^Proof',
                     },
            
            'example': {'class': 'indent1', 
                        'ocr': r'^(Example( (\d+)\.|[s]?\.)) ',
                       },

            'remark': {'class': 'indent1', 
                       'ocr': r'^Remark\.',
                      },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['thm', 'example', 'proof']: 
            if tk == 'proof':
                d['q_or_a'] = 'a'
            else:
                d['k'] = d.get('chapter', '0') + '.' + d.get('section', '0') + ' ' + k 
                d['q_or_a'] = 'q'

        else:
            if tk == 'chapter':
                d['chapter'] = k
            elif tk == 'section':
                d['section'] = k
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
