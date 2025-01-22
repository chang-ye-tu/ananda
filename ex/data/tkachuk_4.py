from books import *
from tkachuk_1 import tkachuk_1

class tkachuk_4(tkachuk_1):

    def __init__(self):
        super(tkachuk_4, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/gt/Tkachuk V. A C_p-Theory Problem Book Functional Equivalencies.pdf'

        self.pgs = range(78, 651)
        
        self.tokens.update({
            'problem': {'class': 'indent0',      
                         'ocr': r'^(V\.[0-9IlO]+)\.',},
        })
