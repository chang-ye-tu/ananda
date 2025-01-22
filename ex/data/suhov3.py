from books import *

class suhov3(book):
    
    def __init__(self):
        super(suhov3, self).__init__()

        self.src = "/home/cytu/usr/doc/math/prob/th/Kelbert M., Suhov Y. Information Theory and Coding by Example.pdf"

        self.pgs = range(14, 514)

        self.morph0 = 'c150.6'

        self.tokens.update({
            'chapter': {'class': 'top',
                        'ocr': r'^\d+$',
                        },

            'thm': {'class': 'indent0',
                    'ocr': r'^((Lemma|Theorem) (\d+\.\d+\.\d+))',
                   },

            'section': {'class': 'centerh',
                        'ocr': r'^\d+\.\d+',
                        },

            'question': {'class': 'indent0',
                         'ocr': r'^(Question (\d+\.\d+\.\d+))',
                        },

            'sol':  {'class': 'indent0', 
                     'ocr': r'^Solution',
                      },

            'proof': {'class': 'indent0',
                      'ocr': r'^Proof',
                      },

            'def': {'class': 'indent0', 
                    'ocr': r'^((Deﬁnition|Definition) (\d+\.\d+\.\d+))',
                   },

            'remark': {'class': 'indent0',
                       'ocr': r'^(Remark (\d+\.\d+\.\d+))',
                      },

            'worked_ex': {'class': 'indent0',
                           'ocr': r'^(Worked Example (\d+\.\d+\.\d+))',
                       },
            
            'prob': {'class': 'indent0',
                          'ocr': r'^(Problem (\d+\.\d+))',
                       },

            'example': {'class': 'indent0',
                        'ocr': r'^(Example (\d+\.\d+\.\d+))',
                       },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['question', 'thm', 'sol', 'proof', 'worked_ex', 'prob']:
            if tk in ['question', 'thm', 'worked_ex', 'prob']:
                d['q_or_a'] = 'q'
                d['k'] = k
            else:
                d['q_or_a'] = 'a'

        else:
            b_skip = True

        return b_skip, d
