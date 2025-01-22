from books import *

class tkachuk_1(book):

    def __init__(self):
        super(tkachuk_1, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/gt/Tkachuk V. A C_p-Theory Problem Book Topological and Function Spaces.pdf'
        self.pgs = range(69, 450)
        
        self.tokens.update({
            'problem': {'class': 'indent0',      
                         'ocr': r'^(S\.[0-9IlO]+)\.',},
            
            'solution': {'class': 'indent0',      
                          'ocr': r'^Solution\.',},
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk == 'problem': 
            d['q_or_a'] = 'q'
            d['k'] = k.replace('I', '1').replace('l', '1').replace('O', '0') 

        elif tk == 'solution':
            d['q_or_a'] = 'a'
        
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), sys.maxsize
