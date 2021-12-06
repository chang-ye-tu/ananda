# -*- coding: utf-8 -*-

from books import *
from tkachuk_1 import tkachuk_1

class tkachuk_2(tkachuk_1):

    def __init__(self):
        super(tkachuk_2, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/gt/Tkachuk V. A C_p-Theory Problem Book Special Features of Function Spaces.pdf'

        self.pgs = range(59, 540)
        
        self.tokens.update({
            'problem': {'class': 'indent0',      
                         'ocr': r'^(T\.[0-9IlO]+)\.',},
        })
