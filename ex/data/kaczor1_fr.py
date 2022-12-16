# -*- coding: utf-8 -*-

from books import *

class kaczor1_fr(book):

    def __init__(self):
        super(kaczor1_fr, self).__init__()

        self.src = "/home/cytu/usr/doc/math/ex/Kaczor W., Nowak M. Problemes d'analyse I.pdf"
        self.pgs = range(11, 374)
        self.w_line = 0.85
        self.morph0 = 'c150.10'
        self.nn_corr = (-4, 0, 4, 0)

        self.tokens.update({
            'chapter': {'class': 'allbx',      
                        'ocr': r'^[IXV]+$', 
                        },
            
            'sol_start': {'class': 'allbx',
                          'ocr': r'^Solutions'
                         },
            
            'prob_start': {'class': 'allbx',
                           'ocr': r'^Énoncés$'
                        },

            'section': {'class': 'allbx',      
                        'ocr': r'^([IXV]+\.\d+\.) ', 
                        },

            'prob_sol': {'class': 'allbx',      
                         'ocr': r'^([1IXV]+\.\d+\.\d+)\.?',  # I --> 1 
                         },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['prob_sol']:
            kl = k.split('.')
            t = [kl[0].replace('1', 'I')]
            t.extend(kl[1:])
            d['k'] = trim('.'.join(t)).replace('[', 'I')
        
        else:
            if tk in ['prob_start', 'sol_start']:
                d['q_or_a'] = 'a' if tk == 'sol_start' else 'q'
            b_skip = True 

        return b_skip, d
    
    def ym(self, bx):
        bxs = self.bxs(bx)
        foot = list(myset(bxs.line(w=(0.1, 0.3))))
        return self.ymin_line(bx), sort_y(foot)[0][1] if foot else self.ymax_skip1(bx)
