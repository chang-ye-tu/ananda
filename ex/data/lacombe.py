# -*- coding: utf-8 -*-

from books import *

class lacombe(book):

    def __init__(self):
        super(lacombe, self).__init__()

        self.src = "/home/cytu/usr/doc/math/ex/Lacombe G., Mallat P. Analyse Fonctionnelle Exercices Corriges.djvu"
        self.pgs = range(7, 346)

        self.range_linew = (0.85, 1.0)
        self.range_lineh = (0, 4) 

        self.tokens.update({
            'chapter': {'class': 'top',      
                        'ocr': r'^(Chapitre|Prologue)', 
                        },
            
            'section': {'class': 'indent0',      
                        'ocr': r'^(\d+\.\d+)', 
                        },

            'sol_start': {'class': 'indent0',
                          'ocr': r'^Solutions$'
                         },

            'ex_sol': {'class': 'indent0',      
                       'ocr': r'^Exerci[sc]e (\d+\.\d+\.\d+)',
                         },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['ex_sol']:
            d['k'] = k
        
        else:
            if tk == 'sol_start':
                d['q_or_a'] = 'a'

            elif tk == 'section':
                d['q_or_a'] = 'q'
            
            b_skip = True 

        return b_skip, d
    
    def ym(self, bx):
        lines = self.bxs(bx).line()
        return min(lower(lines)) if lines else 0, sys.maxsize 
