from books import *

class lovasz(book):

    def __init__(self):
        super(lovasz, self).__init__()

        self.pgs = list(range(12, 105)) + list(range(158, 602))
        self.src = '/home/cytu/usr/doc/math/dscr/cmb/Lovasz L. Combinatorial Problems and Exercises 2ed.djvu'
        self.tokens.update({
            'part':  {'class': 'centerh', 
                      'ocr': r'^(I. (Problems)|II. (Hints)|III. (Solutions))$',
                      },

            'section':  {'class': 'centerh', 
                         'ocr': r'§ (\d+)',
                         },

            'prob_sol': {'class': 'indent0',
                         'ocr': r'^(\d+)\**\.[^\d]', 
                         },
        })

        self.morph1 = 'c9.1'

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['part', 'section', 'sep']:
            if tk == 'section':
                d['root'] = k
            elif tk == 'part':
                if find(k, 'Problems'):
                    d['q_or_a'] = 'q' 
                elif find(k, 'Solutions'):
                    d['q_or_a'] = 'a'
            b_skip = True

        else:

            d['k'] = '.'.join([trim(d['root']), trim(k)])
        
        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx, w=(0.1, 0.2))
