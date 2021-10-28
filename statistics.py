from base import * 

cn = sqlite3.connect(cat('db', 'ananda_temp.db'))
cr = cn.cursor()

def span():
    data = []
    tod = datetime.datetime.today()
    for i in range(10):
        tod1 = tod - datetime.timedelta(days=i)
        ts = tod1.strftime('%Y-%m-%d')
        r = cr.execute('select sum(span) from rev where at like ?', 
                       (ts + '%',)).fetchall()
        n = r[0][0] 
        if n is None:
            n = 0
            s = ' ' * 8
        else:
            s = nr2t(n)
        data.append((n, s, ts))
    return data

class win_stat(QMainWindow):

    def __init__(self, par=None):
        super(win_stat, self).__init__(par)
        self.setWindowTitle(u'Statistics')
        self.setWindowIcon(QIcon(':/res/img/view_list_details.png'))
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        wdg = QWidget(self)
        hlo = QHBoxLayout(wdg)
        #self.cbo = QComboBox(self)
        #hlo.addWidget(self.cbo)  
        self.setCentralWidget(wdg)
        
        for i, k in [('select', ('F2',)), 
                     ('close', ('Esc',)),]:
            n = 'act_%s' % i
            setattr(self, n, QAction(self))
            a = getattr(self, n)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            a.triggered.connect(getattr(self, i)) 
            self.addAction(a)

        self.dso = dso()
   
    def select(self):
        return
    
    def n(self):
        return self.__class__.__name__

s = span()
for i in s:
    print(i[1:])

#if __name__ == '__main__':
#    DBusQtMainLoop(set_as_default=True) 
#    argv = sys.argv
#    app = QApplication(argv)
#    app.setApplicationName('statistics')
#    app.setFont(QFont('Microsoft JhengHei'))
#    w = win_stat()
#    w.show()
#    app.exec_()
