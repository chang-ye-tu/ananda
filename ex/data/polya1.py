# -*- coding: utf-8 -*-

from books import *

class polya1(book):
    
    def __init__(self):
        super(polya1, self).__init__()

        self.src = u'/home/cytu/usr/doc/math/ex/Pólya G., Szegö G. Problems and Theorems in Analysis I Series Integral Calculus Theory of Functions.pdf'
        self.pgs = range(22, 406)
        self.morph0 = 'c150.5'

        self.tokens.update({
            'problems':  {'class': 'first',
                          'ocr': r'^Problems$'},
            
            'solutions': {'class': 'first',
                          'ocr': r'^Solutions$'},

            'part': {'class': 'first2',
                     'ocr': r'^Part ((One|Two|Three|Four|Five|Six|Seven|Eight|Nine))',},

            'chapter':  {'class': 'centerh', 
                         'ocr': r'^Chapter (\d+)',
                        },

            'section':  {'class': 'centerh', 
                         'ocr': r'^§([\.\d ]+)',
                        },

            'prob_sol': {'class': 'indent1',      
                         'ocr': r'^\*?(\d[\.\d ]+)', 
                        },
            })   

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk == 'prob_sol':
            d['k'] = '.'.join([trim(d['root']), trim(k)])
        
        else:
            if tk == 'problems':
                d['q_or_a'] = 'q'

            elif tk == 'solutions':
                d['q_or_a'] = 'a'
            
            elif tk == 'part':
                if find(k, 'One'):
                    d['root'] = '1'
                elif find(k, 'Two'):
                    d['root'] = '2'
                elif find(k, 'Three'):
                    d['root'] = '3'
                elif find(k, 'Four'):
                    d['root'] = '4'
                elif find(k, 'Five'):
                    d['root'] = '5'
                elif find(k, 'Six'):
                    d['root'] = '6'
                elif find(k, 'Seven'):
                    d['root'] = '7'
                elif find(k, 'Eight'):
                    d['root'] = '8'
                elif find(k, 'Nine'):
                    d['root'] = '9'
                elif find(k, 'Appendix'):
                    d['root'] = 'A'
            b_skip = True
        
        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx) 

    def post(self, d):
        self.post_func(d, l=('part',))
