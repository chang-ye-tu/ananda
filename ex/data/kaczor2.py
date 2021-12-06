# -*- coding: utf-8 -*-

from books import *
from kaczor1 import kaczor1

class kaczor2(kaczor1):

    def __init__(self):
        super(kaczor2, self).__init__()
        
        self.src = u"/home/cytu/usr/doc/math/ex/Kaczor W., Nowak M. Problems in Mathematical Analysis II Continuity and Differentiation.pdf"
        self.pgs = range(15, 406)
