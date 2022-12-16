# -*- coding: utf-8 -*-

from books import *

class ash_real(book):

    def __init__(self):
        super(ash_real, self).__init__()

        self.src = '/home/cytu/usr/doc/math/anly/th/Ash/Ash R. Real Variables with Basic Metric Space Topology.djvu' 
        self.range_indent1 = (7e-2, 1e-1)
        self.pgs = range(10, 210)
        self.tokens.update({
            'section': {'class': 'indent0', 
                        'ocr': r'^(\d+\.\d+ )',
                       },

            'subsection': {'class': 'indent0', 
                           'ocr': r'^(\d+\.\d+\.\d+) ',
                          },

            'proof': {'class': 'indent1',      
                      'ocr': r'^Proo', 
                     },

            'prob_start': {'class': 'allbx',      
                           'ocr': r'^(Problems for Section (\d+\.\d+)|REVIEW PROBLEMS FOR CHAPTER (\d+))', },

            'sol_start': {'class': 'indent0',      
                          'ocr': r'^SECTION (\d+\.\d+)', 
                         },

            'prob_sol': {'class': 'indent1',
                         'ocr': r'^(\d+)\. ',
                        },
        })
        
    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['prob_sol', 'subsection', 'proof']:
            if tk == 'prob_sol':
                d['k'] = 'e'.join([d['root'], k])
            elif tk == 'subsection':
                d['q_or_a'] = 'q'
                d['k'] = k
                d['prob'] = True
            elif tk == 'proof':
                d['q_or_a'] = 'a'

        else:
            if tk == 'sol_start':
                d['q_or_a'] = 'a'
                d['root'] = trim(k.replace('SECTION', ''))
                d['prob'] = False
            elif tk == 'prob_start':
                d['q_or_a'] = ('q' if d.get('prob', True) else 'a')
                d['root'] = trim(k.replace('Problems for Section ', '').replace('REVIEW PROBLEMS FOR CHAPTER ', ''))
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_line(bx), sys.maxsize
