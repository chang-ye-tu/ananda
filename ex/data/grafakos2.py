# -*- coding: utf-8 -*-

from books import *
from grafakos1 import grafakos1

class grafakos2(grafakos1):
    
    def __init__(self):
        super(grafakos2, self).__init__()
        
        self.pgs = range(14, 493)
        self.src = "/home/cytu/usr/doc/math/anly/th/Grafakos L. Modern Fourier Analysis 3ed.pdf"
