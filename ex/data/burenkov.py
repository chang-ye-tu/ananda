# -*- coding: utf-8 -*-

from books import *
import re

p = re.compile('\d+')

class burenkov(book):

    def __init__(self):
        super(burenkov, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Burenkov V. Sobolev Spaces on Domains.pdf' 
        self.pgs = range(14, 289)
        self.range_lineh = (0, 3)
        self.range_indent0 = (0., 4e-2)        

        self.tokens.update({
            'chapter':  {'class': 'top', 
                         'ocr': r'^Chapter (\d+)$',
                        },

            'section':  {'class': 'indent0', 
                         'ocr': r'^(\d+[ ]?\.[ ]?\d+)',
                        },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Theorem|Lemma|Corollary)[ ]?(\d+))', 
                   },
            
            'example': {'class': 'indent0',      
                        'ocr': r'^(Example[ ]?(\d+))', 
                       },

            'defn': {'class': 'indent0',      
                     'ocr': r'^(Deﬁnition[ ]?(\d+))',
                    },

            'remark': {'class': 'indent0',
                       'ocr': r'^(Remark[ ]?(\d+))',
                      },
            
            'proof': {'class': 'indent0',      
                      'ocr': r'^(Proof|Idea of the)', 
                     },
        })
        
    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'example', 'proof']:
            if tk in ['thm', 'example']:
                d['q_or_a'] = 'q'
                nr = p.findall(k)
                d['k'] = ' '.join([d['root'], p.sub('', k).strip(), nr[0]])
            else:
                d['q_or_a'] = 'a' 
        else:
            if tk == 'chapter':
                d['root'] = trim(k)
            b_skip = True

        return b_skip, d
    
    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx, w=(0.1, 0.5))
    
    def post(self, d):
        self.post_func(d, l=('chapter',))
