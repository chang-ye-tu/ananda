# -*- coding: utf-8 -*-

from books import *
from tkachuk_1 import tkachuk_1

class tkachuk_3(tkachuk_1):

    def __init__(self):
        super(tkachuk_3, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/gt/Tkachuk V. A C_p-Theory Problem Book Compactness in Function Spaces.pdf'

        self.pgs = range(64, 473)
        
        self.tokens.update({
            'problem': {'class': 'indent0',      
                         'ocr': r'^(U\.[0-9IlO]+)\.',},
        })
