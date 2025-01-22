from base import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

mode_insert, mode_update = range(2)

def make_db(cn):
    cr = cn.cursor()

    def create_ix(t, i):
        cr.execute(f'create index ix_{t}_{i} on {t}({i})')

    for t in ['loci']:
        cr.execute(f'''create table {t} (id integer primary key, 
                                         link text not null,
                                         pix blob not null,
                                         rct text not null,
                          created text not null default current_timestamp,
                                         unique (link))''')
        for i in ['link', 'created']:
            create_ix(t, i)

    for t in ['route']:
        cr.execute(f'''create table {t} (id integer primary key, data text not null, unique (data))''')
        for i in ['data',]:
            create_ix(t, i)

    cn.commit()

db_loci = '/home/cytu/usr/src/py/ananda/db/loci.db'
if not os.path.isfile(db_loci):
    make_db(sqlite3.connect(db_loci))

cn = sqlite3.connect(db_loci)
cr = cn.cursor()

def n_fact(interval=None):
    try:
        count = 'select count(*) from loci'
        sql = (count,) if interval is None else (' '.join([count, 'where created between ? and ?']), interval)
        return cr.execute(*sql).fetchone()[0]
    except:
        return 0

class win_loci(QMainWindow):
    
    resized = pyqtSignal()    

    def __init__(self, par=None):
        QMainWindow.__init__(self, par)
        self.setWindowTitle('Loci Selector')
        self.setWindowIcon(QIcon(':/res/img/google-streets-icon.png'))
        self.td = tempfile.mkdtemp(prefix=f"{self.n()}_{now().replace(':', '')}_", dir=cat(os.getcwd(), tmp))
        
        self.lw = lw = QListWidget(self)
        f = self.load_lw
        lw.itemClicked.connect(f)
        lw.itemActivated.connect(f)

        self.gv = gv = QGraphicsView(self)
        self.scn = scn = QGraphicsScene(self)
        gv.setScene(scn)

        self.spl = spl = QSplitter(Qt.Horizontal, self)
        spl.addWidget(lw)
        spl.addWidget(gv)

        ww = QWidget(self)
        lo = QHBoxLayout()
        lo.addWidget(spl)
        ww.setLayout(lo)
        
        self.setCentralWidget(ww)

        for i, k in [('load', ('F3',)),
                     ('mode', ('F4',)), 
                     ('del',  ('Ctrl+D',)), 
                     ('new',  ('Ctrl+T',)),
                     ('next', ('Alt+Right', 'PgDown')),
                     ('prev', ('Alt+Left',  'PgUp')),
                    ]:
            s = f'act_{i}'
            setattr(self, s, QAction(self))
            a = getattr(self, s)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            a.triggered.connect(partial(self.handler, i))
            self.addAction(a)
        
        stb = QStatusBar(self)
        self.setStatusBar(stb)
        for ii, (i, l) in enumerate([('mode', 1),
                                     ('gen',  8),
                                     ('num',  8),
                                     ('route',13),
                                    ]):
            n = f'lbl_{i}'
            setattr(self, n, QLabel(self))
            lbl = getattr(self, n)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
            stb.insertPermanentWidget(ii, lbl, l)
        stb.setSizeGripEnabled(False)

        n = self.n()
        spl.restoreState(sts.value(f'{n}/spl/state', type=QByteArray))
        self.restoreState(sts.value(f'{n}/state', type=QByteArray))        
        
        self.signal_handler = DBusSignalHandler(self)
        self.signal_handler.selectReceived.connect(self.select)

        # XXX
        #n, ok = sts.value(f'{self.n()}/id').toInt()
        #self.setup(n if ok else 1) 
        n = sts.value(f'{self.n()}/id', type=int)
        self.setup(n) 
    
        # To handle the resizeEvent better
        self.resized.connect(self.display)

    def setup(self, i=1):
        self.mode = mode_insert
        r = cr.execute('select * from route where id = ?', (i,)).fetchone()
        if r:
            self.d = json.loads(r[1])
            self.d['id'] = i
        else:    
            self.d = {'name': '', 'loci': []}

        self.ix = self.d.get('last_ix', 0)
        self.display()
        
        self.lw.clear()
        r = cr.execute('select id, data from route').fetchall()
        for dd in r:
            ii, data = dd
            d = json.loads(data)
            name = d['name']
            it = QListWidgetItem(QIcon(':/res/img/Google_Maps_Marker.png'), name)
            it.setData(Qt.UserRole, QVariant(json.dumps({'name': name, 'id': ii})))
            self.lw.addItem(it)

        self.update_stb()
        self.show_link()

    def load_lw(self, i):
        self.save()
        self.setup(item_data(i)['id'])

    def show_link(self):
        d = self.d
        loci = d.get('loci', [])
        if not loci:
            return
        
        link = getattr(self, 'link', 'http://maps.google.com')
        r = cr.execute('select link from loci where id = ?', (loci[self.ix],)).fetchone()
        if not r:
            return
        link = r[0]
        self.link = link
       
        driver.get(link)
        #try:
        #    # hide imagery: '<div class="widget-expand-button-icon"></div>'
        #    time.sleep(5)
        #    btn_expand = driver.find_element_by_class_name('widget-expand-button-icon')
        #    btn_expand.click()
        #except:
        #    print('click widget-expand-button-icon error')
    
    @pyqtSlot()
    def display(self):
        try:
            i = self.d['loci'][self.ix]
        except:
            return
        r = cr.execute('select pix from loci where id = ?', (i,)).fetchone() 
        if r:
            f = cat(self.td, 'display.png')
            open(f, 'wb').write(r[0])
            p = QPixmap(f)
            gv = self.gv
            if p.width():
                h = gv.height()
                w = gv.width()
                if p.height() >= 0.95 * h:
                    p = p.scaledToHeight(int(0.95 * h), Qt.SmoothTransformation)
                if p.width() >= 0.95 * w:
                    p = p.scaledToWidth(int(0.95 * w), Qt.SmoothTransformation)
                scn = self.scn
                scn.clear()
                scn.setSceneRect(0, 0, p.width(), p.height())
                scn.addItem(QGraphicsPixmapItem(p))

    def update_stb(self):
        self.lbl_mode.setPixmap(QPixmap(f":/res/img/{'list_add' if self.mode == mode_insert else 'frame_edit'}.png"))
        
        d = self.d
        n = len(d['loci'])
        
        self.msg({'msg': f'<font color="green">route &nbsp; [{d["name"]}] : &nbsp;#{self.ix + 1 if n else 0} of {n}</font>', 'sct': 'route'})
        self.msg({'msg': f'<font color="blue"># today: {n_fact((today(), tomorrow()))}&nbsp; all: {n_fact()}</font>', 'sct': 'num'})

    def handler(self, i):
        if i == 'load':
            self.show_link()            

        elif i == 'mode':
            self.mode += 1
            self.mode %= 2

        elif i == 'del':
            if self.d['loci']:
                cr.execute('delete from loci where id = ?', (self.d['loci'][self.ix],))
                cn.commit()
                self.d['loci'].pop(self.ix)
                self.navigate(False)
                # XXX
                self.save()

        elif i in ['next', 'prev']:
            self.navigate(True if i == 'next' else False)
        
        elif i == 'new':
            name, ok = QInputDialog.getText(self, 'Create New Route', 'Enter New Route Name:', text='Route')
            if ok:
                # save unfinished work before starting new route
                self.save()
                cr.execute('insert into route (data) values (?)', (json.dumps({'name': name, 'loci': []}),))
                cn.commit()
                i = cr.execute('select last_insert_rowid()').fetchone()[0]
                self.setup(i)

        self.update_stb()

    def navigate(self, forward=True):
        if getattr(self, 'busy', False):
            print('navigate: busy')
            return

        self.busy = True
        i = self.ix
        loci = self.d['loci']
        if loci:
            self.ix += (1 if forward else -1)
            self.ix %= len(loci)
        else:
            self.ix = 0
        
        if self.ix != i:
            self.display()
        self.busy = False
    
    def save(self):
        d = self.d
        i = d.get('id', 0)
        d['last_ix'] = self.ix 
        dd = json.dumps(d)
        if i:
            cr.execute('update route set data = ? where id = ?', (dd, i))
        else:
            if d['loci']:
                cr.execute('insert into route (data) values (?)', (dd,))
                i = cr.execute('select last_insert_rowid()').fetchone()[0]
                d['id'] = i

        sts.setValue(f'{self.n()}/id', QVariant(i))        
        cn.commit()

    def select(self, s):
        link = driver.current_url 
        d = json.loads(s)
        f = d['f']
        pix = sqlite3.Binary(open(f, 'rb').read())
        rct = json.dumps(d.get('rct', []))
        
        def insert():
            cr.execute('insert into loci (link, pix, rct) values (?, ?, ?)', (link, pix, rct))
            cn.commit()
            self.d['loci'].insert(self.ix + 1, 
                cr.execute('select last_insert_rowid()').fetchone()[0])
            self.navigate()
            self.save()

        if self.mode == mode_insert:
            insert() 

        else:
            try:
                cr.execute('update loci set link = ?, pix = ?, rct = ? where id = ?', (link, pix, rct, self.d['loci'][self.ix]))
                cn.commit()
                self.display()

            except:
                insert()
        
        os.remove(f)
        self.update_stb()

    def msg(self, d):
        lbl = getattr(self, f"lbl_{d.get('sct', 'gen')}")
        msg = d.get('msg', '')
        to = d.get('to', 0)
        lbl.setText(msg)
        
        if to:
            QTimer.singleShot(to, partial(lbl.setText, ''))
        
    def cls(self):
        n = self.n()
        #if not self.isFullScreen() and not self.isMaximized():
        #    sts.setValue(f'{n}/size', QVariant(self.size()))
        
        sts.setValue(f'{n}/state', QVariant(self.saveState()))        
        sts.setValue(f'{n}/spl/state', QVariant(self.spl.saveState()))

        #l = ['mnb', 'stb', 'tb',]
        #for i in l:
        #    sts.setValue(f'{n}/{i}/visible', QVariant(getattr(self, i).isVisible()))
        
        shutil.rmtree(self.td)

    def n(self):
        return self.__class__.__name__
   
    def closeEvent(self, e):
        driver.close()
        self.save()
        self.cls()

    def resizeEvent(self, e):
        self.resized.emit() 

def save_all_path():
    # routine that save the whole path into a folder
    data = cr.execute('select data from route').fetchall()
    for d in data:
        dd = json.loads(d[0])
        ids = dd['loci']
        name = dd['name']
        fd = '/home/cytu/Downloads/loci/' + name
        if not os.path.isdir(fd):
            os.makedirs(fd) 
        for index, ii in enumerate(ids): 
            r = cr.execute('select pix from loci where id = ?', (ii,)).fetchone() 
            if r:
                f = cat(fd, str(index+1).zfill(3) + '.png')
                open(f, 'wb').write(r[0])

if __name__ == '__main__':
    #save_all_path(); sys.exit()

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Since we are using maximize_window()

    # Create service object
    service = Service(executable_path='/home/cytu/usr/src/py/ananda/chromedriver')

    # Create driver with service and options
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    app = QApplication(sys.argv)
    app.setFont(QFont('Microsoft JhengHei'))

    QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
     
    w = win_loci()
    w.showMaximized()
    
    app.exec() 
