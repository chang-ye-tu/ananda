from books import *

class makarov(book):

    def __init__(self):
        super(makarov, self).__init__()

        self.src = "/home/cytu/usr/doc/math/ex/Makarov B. et al. Selected Problems in Real Analysis.djvu"
        self.pgs = range(10, 374)
        self.morph0 = 'c50.1'
        #self.nn_corr = (-4, 0, 4, 0)

        self.tokens.update({
            'chapter': {'class': 'top',      
                        'ocr': r'^CHAPTER ([IXV]+)$', 
                        },
            
            'sol_start': {'class': 'allbx',
                          'ocr': r'^Solutions$'
                         },
            
            'prob_start': {'class': 'allbx',
                           'ocr': r'^Problems$'
                        },

            'section':  {'class': 'allbx', 
                         'ocr': r'^§',
                        },

            'prob_sol': {'class': 'allbx',      
                         'ocr': r'^([l0-9]+[ ]?\.[ ]?[l0-9]+)\.?',
                         },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['prob_sol']:
            d['k'] = '.'.join([d['root'], trim(k).replace('l', '1')]) 
        
        else:
            if tk in ['prob_start', 'sol_start']:
                d['q_or_a'] = 'a' if tk == 'sol_start' else 'q'
            elif tk == 'chapter':
                d['root'] = k
            b_skip = True 

        return b_skip, d
    
    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.centerh()) & myset(bxs.tiny()))
        return self.ymin_skip1(bx), sort_y(bx)[-1][1] if nr else self.ymax_line(bx)

    def post(self, d):
        self.post_func(d, l=('chapter', 'prob_start', 'sol_start'))
