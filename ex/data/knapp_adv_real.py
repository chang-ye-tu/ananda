# -*- coding: utf-8 -*-

from books import *
from knapp_basic_real import *

class knapp_adv_real(knapp_basic_real):
    
    def __init__(self):
        super(knapp_adv_real, self).__init__()
        
        self.pgs = range(30, 631)
        self.morph0 = 'c150.4'
        self.src = "/home/cytu/usr/doc/math/anly/th/Knapp/Knapp A. Advanced Real Analysis Digital Second Edition.pdf"
