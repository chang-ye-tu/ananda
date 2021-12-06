# -*- coding: utf-8 -*-

from books import *

class burkill(book):
    
    def __init__(self):
        super(burkill, self).__init__()
        
        self.pgs = range(8, 529)
        self.src = "/home/cytu/usr/doc/math/anly/th/Burkill J. A Second Course in Mathematical Analysis.djvu"

        self.tokens.update({
            'thm': {'class': 'indent0',      
                    'ocr': r'^(Theorem (\d+\.\d+))', 
                   },

            'cor': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary)( \d)?)', 
                   },
            
            'sec': {'class': 'indent0',      
                    'ocr': r'^\d+\.\d+\.', 
                   },

            'ex_sec': {'class': 'centerh', 
                       'ocr': r'^Exercises (\d+[ ]?\([a-z]\))',
                      },

            'sol_sec': {'class': 'centerh', 
                        'ocr': r'^(\d+[ ]?\([a-z]\))',
                       },

            'ex_sol': {'class': 'indent0',
                       'ocr': r'^(\d+)\. ',
                      },

            'proof': {'class': 'indent1', 
                      'ocr': r'^Pr[0o][0o]f',
                     },

            'solution': {'class': 'indent1', 
                         'ocr': r'^Solution',
                        },
            
            'example': {'class': 'indent0',      
                        'ocr': r'^(Example( \d)?)', 
                       },

            'note': {'class': 'indent0',      
                     'ocr': r'^Note', 
                    },
            
            'exer': {'class': 'indent0',      
                     'ocr': r'^Exercise', 
                    },

            'illu': {'class': 'indent0',      
                     'ocr': r'^Illustration', 
                    },

            'notes': {'class': 'centerh', 
                      'ocr': r'^NOTES ON CHAPTER',
                     },

            'defn': {'class': 'indent0',      
                     'ocr': r'^Deﬁnition', 
                    },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'cor', 'example', 'illu', 'proof', 'solution']:
            if tk in ['thm',]:
                d['q_or_a'] = 'q'
                d['k'] = k
            elif tk in ['cor', 'example', 'illu']:
                d['q_or_a'] = 'q'
                d['k'] = d['sec'] + ' fact ' + str(d['idx']) 
                d['idx'] += 1
            else:
                d['q_or_a'] = 'a'
             
        elif tk == 'ex_sol':
            d['k'] = d['ex_sol_sec'] + ' ' + k

        else:
            if tk in ['ex_sec', 'sol_sec']:
                d['q_or_a'] = 'q' if tk == 'ex_sec' else 'a'
                d['ex_sol_sec'] = trim(k)
            elif tk == 'sec':
                d['idx'] = 1 
                d['sec'] = trim(k)

            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx, w=(0.2, 0.4))
