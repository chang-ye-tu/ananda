# -*- coding: utf-8 -*-

from books import *

class yor(book):

    def __init__(self):
        super(yor, self).__init__()

        self.tokens.update({
            'comments': {'class': 'indent0',      
                         'ocr': r'Comments', 
                        },

            'exercise': {'class': 'indent0',      
                         'ocr': r'\*{0,2} (\d+\.\d+)',
                        },

            'chapter': {'class': 'top',      
                         'ocr': r'^Chapter (\d+)',
                        },
            
            'solution': {'class': 'indent0',      
                         'ocr': r'^Solution to Exercise (\d+\.\d+)', 
                         },

            'bar': {'class': 'line',},
        })

        self.src = '/home/cytu/usr/doc/math/prob/th/Yor/Chaumont L., Yor M. Exercises in Probability A Guided Tour from Measure Theory to Random Processes via Conditioning 2ed.pdf' 
        self.pgs = range(21, 289)

    def ym(self, bx):
        return self.ymin_skip1(bx), sys.maxsize

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['comments', 'bar', 'sep', 'chapter']:
            b_skip = True

        else:
            d['k'] = trim(k)
            d['q_or_a'] = 'q' if tk == 'exercise' else 'a'
        
        return b_skip, d

    def post(self, dd):
        self.post_func(dd)
