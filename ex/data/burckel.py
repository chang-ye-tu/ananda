from books import *

class burckel(book):

    def __init__(self):
        super(burckel, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Burckel R. B. Classical Analysis in the Complex Plane.pdf' 
        self.pgs = range(50, 920)
        self.morph0 = 'c150.10' 
        self.tokens.update({
            'chapter':  {'class': 'indent0', 
                         'ocr': r'^Chapter ([IXV]+)',
                         },

            'section':  {'class': 'indent0', 
                         'ocr': r'^§[ ]*(\d+) ',
                         },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Theorem|Corollary|Lemma) (\d+\.\d+))', 
                   },
            
            'defn': {'class': 'indent0',      
                     'ocr': r'^(Definition (\d+\.\d+))',
                    },

            'proof': {'class': 'indent0',      
                      'ocr': r'^Proof', 
                     },
            
            'cont': {'class': 'indent0',
                     'ocr': r'^\([ivx]+\)',
                    },

            'ex': {'class': 'indent0',
                   'ocr': r'^(Exercise (\d+\.\d+))',
                  },

            'hint': {'class': 'indent0',
                     'ocr': r'^Hints',
                    },

            'remark': {'class': 'indent0',
                       'ocr': r'^Remarks?',
                      },

            'notes': {'class': 'allbx',
                      'ocr': r'^Notes to Chapter',
                     },
     })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['thm', 'proof', 'ex', 'hint', 'cont']:
            if tk in ['thm', 'ex']:
                d['q_or_a'] = 'q'
                d['root'] = 'q'
                d['k'] = k
            elif tk in ['proof', 'hint']:
                d['q_or_a'] = 'a' 
                if tk == 'proof': # don't change cont type after hint appears!
                    d['root'] = 'a'
            else:
                r = d.get('root', '')
                if r:
                    d['q_or_a'] = r
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx)
