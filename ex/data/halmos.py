# -*- coding: utf-8 -*-

from books import *

class halmos(book):

    def __init__(self):
        super(halmos, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Halmos P. A Hilbert Space Problem Book 2ed.djvu'
        self.pgs = range(18, 365)
        self.tokens.update({
            'intro': {'class': 'indent0', 
                       'ocr': r'^(\d+)\. ',
                     },

            'prob': {'class': 'allbx',
                     'ocr': r'^Problem (\d+)\.', 
                    },

            'part': {'class': 'allbx',
                     'ocr': r'^(HINTS|SOLUTIONS|PROBLEMS)$',
                    },

            'sol': {'class': 'allbx',
                    'ocr': r'^Solution (\d+)\.',
                    },

            'chapter': {'class': 'first2',
                        'ocr': r'^CHAPTER (\d+)$',
                        },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['prob', 'sol']: 
            if tk == 'sol':
                d['q_or_a'] = 'a' 
                d['k'] = k
            else:
                if d.get('part', '') == 'prob':
                    d['q_or_a'] = 'q'    
                    d['k'] = k 
                else:
                    b_skip = True
        else:
            if tk == 'part':
                if k == 'SOLUTIONS':
                    d['part'] = 'sol'
                elif k == 'HINTS':
                    d['part'] = 'hint'
                elif k == 'PROBLEMS':
                    d['part'] = 'prob'
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        try:
            # skip the first and the last lines
            y_min = min(lower(bx)) 
            y_max = sort_y(bx)[-1][1]
            
            return y_min, y_max

        except:
            return 0, sys.maxsize
    
    def post(self, d):
        self.post_func(d)
