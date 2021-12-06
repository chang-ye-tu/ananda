# -*- coding: utf-8 -*-

from books import *

class grimmett(book):

    def __init__(self):
        super(grimmett, self).__init__()

        self.src = '/home/cytu/usr/doc/math/prob/th/Grimmett/Grimmett G., Stirzaker D. Probability and Random Processes 3ed.djvu'

        self.pgs = range(11, 575)
        self.tokens.update({
            'section':  {'class': 'centerh', 
                         'ocr': r'^(\d+\.\d+) ',
                         },
            'point': {'class': 'indent0',
                      'ocr': r'^\((\d+)\)',
                     },

            'proof': {'class': 'indent0',
                      'ocr': r'^Proof',
                      },

            'sol': {'class': 'indent0',
                      'ocr': r'^Solution',
                      },

            'bar': {'class': 'line',},
        })
    
    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['point', 'proof', 'sol']:
            if tk == 'point':
                d['q_or_a'] = 'q' 
                d['k'] = '.'.join([d['root'], k])
            else:
                d['q_or_a'] = 'a'

        else:
            if tk == 'section':
                d['root'] = k

            b_skip = True

        return b_skip, d
    
    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx, w=(0.15, 0.3))
    
    def tkd_filter(self, d):
        tkd = d['tkd']
        bxd = d['bxd']
        for pg in tkd:
            bx = bxd[pg]
            w = span(bx)[2]
            l = []
            for tk in tkd[pg]:
                tw = self.range_tinyw
                b, typ, s, ke = tk
                if not (typ == 'point' and (tw[0] <= b[2] * 1. / w <= tw[1])):
                    l.append(tk)
            tkd[pg] = l
