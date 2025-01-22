from books import *

class abadir_stat(book):

    def __init__(self):
        super().__init__()

        self.src = "/home/cytu/usr/doc/math/anly/appl/Abadir K. M., Heijmans R. D. H., Magnus J. R. Statistics.pdf"
        self.pgs = range(32, 728)
        self.tokens.update({
            'notes':  {'class': 'indent0', 
                       'ocr': r'^Notes$',
                       },

            'section':  {'class': 'centerh', 
                         'ocr': r'^\d+\.\d+',
                         },

            'exercise': {'class': 'indent0',      
                        'ocr': r'\**[EKH]?[EKH]xercise (\d+\.\d+)', 
                        },
            
            'solution': {'class': 'indent0',      
                         'ocr': r'^Solution$', 
                         },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['section', 'notes', 'sep']:
            b_skip = True

        else:
            if tk == 'solution':
                d['q_or_a'] = 'a'
            else:
                d['k'] = trim(k)
                d['q_or_a'] = 'q' 
        
        return b_skip, d
