from books import *

class gadea(book):

    def __init__(self):
        super(gadea, self).__init__()

        self.src = u'/home/cytu/usr/doc/math/geo/Gadea P., Munoz Masqué J., Mykytyuk I. Analysis and Algebra on Differentiable Manifolds A Workbook for Students and Teachers 2ed.pdf'
        self.pgs = range(19, 563)

        self.tokens.update({
            'chapter':  {'class': 'first', 
                         'ocr': r'^Chapter (\d+)',
                        },

            'section':  {'class': 'indent0', 
                         'ocr': r'(\d+\.\d+) ',
                        },

            'problem': {'class': 'indent0',      
                        'ocr': r'^Problem (\d+\.\d+)', 
                       },
            
            #'thm': {'class': 'indent0', 
            #        'ocr': r'^((Theorem|Proposition|Lemma) (\d+\.\d+))',
            #       },

            #'def': {'class': 'indent0', 
            #        'ocr': r'^(Deﬁnition[s]? (\d+\.\d+))',
            #       },

            'ref':  {'class': 'indent0', 
                     'ocr': r'^(References|Further Reading)',
                    },
            
            'remark':  {'class': 'indent0', 
                        'ocr': r'^Remark',
                       },

            'hint':  {'class': 'indent0', 
                      'ocr': r'^H[ ]?int',
                     },

            'solution': {'class': 'indent0',      
                         'ocr': r'^Solution', 
                        },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['remark', 'chapter', 'section', 'sep', 'hint', 'ref']:
            b_skip = True

        else:
            if tk == 'solution':
                d['q_or_a'] = 'a'
            else:
                d['k'] = trim(k)
                d['q_or_a'] = 'q' 
        
        return b_skip, d

    def ym(self, bx):
        return self.ymin_skip1(bx), self.ymax_line(bx) 
