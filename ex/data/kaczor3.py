# -*- coding: utf-8 -*-

from books import *
from kaczor1 import kaczor1

class kaczor3(kaczor1):

    def __init__(self):
        super(kaczor3, self).__init__()
        
        self.src = u"/home/cytu/usr/doc/math/ex/Kaczor W., Nowak M. Problems in Mathematical Analysis III Integration.djvu"
        self.pgs = range(11, 361)
