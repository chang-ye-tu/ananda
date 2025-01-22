from base import * 

tasks = {
#    'default drills + German words + Knapp basic real': [
#        ['drill', [], 60, 10],
#        ['word', 'de_grundwortschatz_pre', 60, 10],
#        ['hrv', 'knapp_basic_real', 60 , 10],
#    ],
#
    '2 digits-action drill': [
        ['drill', 
         ['nr_action_1', '0', '1', '2', '5', 
          'nr_action',   '0', '1', '3', '3',], 
         3, 1],
    ], 
#
#    'German words': [['word', 'de_grundwortschatz_pre', 60, 10],],
#    'Generic': [['rev', ['gen',], 60, 10],],
#    'Ambrosio et al: Analysis': [['hrv_temp', 'ambrosio', 120, 10],],
#    'Ash R.: Real Variables': [['rev', ['ash_real',], 120, 10],],
    'Aliprantis-Burkinshaw: Real Analysis': [['hrv_temp', 'aliprantis', 120, 10],],
#    'Aliprantis: Problems in Real Analysis': [['rev_temp', ['aliprantis_sol',], 120, 10],],
    'Baldi: Probability': [['hrv_temp', 'baldi2', 120, 10],],
#    'Baldi: Stochastic Analysis': [['hrv_temp', 'baldi1', 120, 10],],
    'Dreyfus-Law: The Art and Theory of Dynamic Programming': [['rev_temp', ['dreyfus',], 120, 10],],
    'Evans: Partial Differential Equations': [['rev_temp', ['evans',], 120, 10],],
#    'Medvegyev: Stochastic Analysis': [['hrv_temp', 'medvegyev', 120, 10],],
#    'Kirsch-Grinberg: Factorization Method':[['hrv_temp', 'kirsch_grinberg', 120, 10],],
#    'Colton-Kress: Inverse Scattering':[['hrv_temp', 'colton_kress', 120, 10],],
#    'Knapp: Basic Real Analysis': [['hrv', 'knapp_basic_real', 60 , 10],],
#    'Zastawniak: Stochastic Process': [['hrv', 'zastawniak', 60, 10],],
#    'Rudin: Functional Analysis': [['hrv', 'rudin_fa', 60, 10],],
#    'Boyd: Convex Optimization': [['hrv', 'boyd', 60, 10],],
#    'Ash: Complex Analysis': [['hrv', 'ash_complex', 60, 10],],
#    'Hörmander I': [['hrv', 'hoermander1', 60, 10],],
#    'Milman: Functional Analysis': [['hrv', 'milman', 60, 10],],
#    'Brezis: Functional Analysis': [['hrv', 'brezis', 120, 10],],     
#    'Fabian: Banach Space': [['hrv_temp', 'fabian', 120, 10],],
#    'Casella: Mathematical Statistics': [['hrv_temp', 'casella', 120, 10],],
#    'Rosenthal: Probability': [['hrv_temp', 'rosenthal', 120, 10],],
#    'Rosenthal: Probability Solutions': [['rev', ['rosenthal_sol',], 120, 10],],
#    'Zizler: Modern Analysis': [['hrv_temp', 'zizler', 120, 10],],
#    'Knapp: Basic Real Analysis': [['hrv_temp', 'knapp_basic_real', 120, 10],],
#    'Knapp: Advanced Real Analysis': [['hrv_temp', 'knapp_adv_real', 120, 10],],
#    'Girault & Raviart: FEM for Navier-Stokes': [['hrv_temp', 'girault', 120, 10],],
#    'Evans-Gariepy: Geometric Measure Theory': [['hrv_temp', 'evans_gariepy', 120, 10],],     
#    'McLean: Strongly Elliptic Systems and BIE': [['hrv_temp', 'mclean', 120, 10],],
#    'Nečas J. Theory of Elliptic Equations': [['hrv_temp', 'necas', 120, 10],],
#    'Abadir: Matrix Analysis': [['rev_temp', ['abadir',], 120, 10],],
#    'Abadir: Statistics': [['rev_temp', ['abadir_stat',], 120, 10],],
#    'Boyd: Convex Optimization Problems': [['rev_temp', ['boyd_sol',], 120, 10],],
#    'Costara': [['rev_temp', ['costara',], 120, 10],], 
#    'Zuily': [['rev_temp', ['zuily',], 120, 10],], 
#    'Kaczor vol.1': [['rev', ['kaczor1',], 60, 10],], 
#    'Kaczor vol.2': [['rev', ['kaczor2',], 60, 10],], 
#    'Kaczor vol.3': [['rev', ['kaczor3',], 60, 10],], 
#    'review due memorized facts': [
#        ['rev', [], 60, 10],
#    ],
    'null': [['null', '', 10000, 1],],
#   '1.5 hr work': [
#        ['null', '', 90, 1],
#   ],
}

class win_task(QMainWindow):

    def __init__(self, par=None):
        super(win_task, self).__init__(par)
        self.setWindowTitle(u'Select Task')
        self.setWindowIcon(QIcon(':/res/img/view_list_details.png'))
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.Dialog)
        
        wdg = QWidget(self)
        hlo = QHBoxLayout(wdg)
        self.cbo = QComboBox(self)
        hlo.addWidget(self.cbo)  
        self.setCentralWidget(wdg)
        
        for i, k in [('select', ('F2',)), 
                     ('close', ('Esc',)),]:
            n = f'act_{i}'
            setattr(self, n, QAction(self))
            a = getattr(self, n)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            a.triggered.connect(getattr(self, i)) 
            self.addAction(a)

        self.service = ScheduleService(self)

        for k in tasks:
            self.cbo.addItem(k, QVariant(json.dumps(tasks[k])))
        
        n = self.n()
        i = sts.value(f'{n}/index', type=int)
        self.cbo.setCurrentIndex(i)
        
    def select(self):
        i = self.cbo.currentIndex()
        self.service.schedule(self.cbo.itemData(i))
        sts.setValue(f'{self.n()}/index', QVariant(i))
        self.close()

    def n(self):
        return self.__class__.__name__

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('task')
    app.setFont(QFont('Microsoft JhengHei'))
    w = win_task()
    w.show()
    app.exec()
