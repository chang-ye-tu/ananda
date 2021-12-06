# -*- coding: utf-8 -*-

from books import *

from knapp_basic_real import *

class knapp_basic_alg(knapp_basic_real):
    
    def __init__(self):
        super(knapp_basic_alg, self).__init__()
        
        self.pgs = range(22, 741)
        self.src = "/home/cytu/usr/doc/math/anly/th/Knapp/Knapp A. Basic Algebra Digital Second Edition.pdf"
