# -*- coding: utf-8 -*-

from books import *
from kaczor1_fr import kaczor1_fr

class kaczor2_fr(kaczor1_fr):

    def __init__(self):
        super(kaczor2_fr, self).__init__()
        
        self.src = "/home/cytu/usr/doc/math/ex/Kaczor W., Nowak M. Problemes d'analyse II.pdf"
        self.pgs = range(13, 382)
