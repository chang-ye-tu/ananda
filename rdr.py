from base import *
from ui.win_hrv import Ui_win_hrv

mode_read, mode_anno = range(2)

class cmd_view(QUndoCommand):
    
    def __init__(self, w, s_i, s_f, dsc):
        super(cmd_view, self).__init__(dsc)
        attrs_from_dict(locals())

    def redo(self):
        self.w.set_s(self.s_f) 

    def undo(self):
        self.w.set_s(self.s_i)

class view(QGraphicsView):
    
    def __init__(self, par=None, dd=None):
        super(view, self).__init__(par)
        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        attrs_from_dict(locals())
        self.td = tempfile.mkdtemp(prefix='%s_%s_' % (self.n(), now().replace(':', '')), dir=cat(os.getcwd(), tmp))

        self.scn = QGraphicsScene(self)
        self.setScene(self.scn)

        for i in [self.horizontalScrollBar(), self.verticalScrollBar()]:
            i.actionTriggered.connect(self.before)
            i.valueChanged.connect(self.after)
        
        self.hst = QUndoStack(self)
        
        self.book = bk(dd['name'])
        self.doc = dc = self.book.doc()
        if dd['sha'] != dc.sha:
            print("dd['sha'] != dc.sha !!!")
        dc.msg_doc.connect(self.handler_doc)
        
        self.set_mode(mode_anno)

    def hst_push(self, k):
        dd = self.dd
        qa = dd['qa']
        z = self.z()
        zo = dd['zo']
        zz = 2. * z / zo
        mm = QTransform(zz, 0, 0, zz, 0, 0)
        vs = self.verticalScrollBar()
        hs = self.horizontalScrollBar()
        dc = self.book.doc()
        dc.set_z(z)

        # reverse order
        s_i = {}
        for typ in ['a', 'q']:
            for pg, a in reversed(qa[typ][k]):
                # XXX compute exact z, v, h
                p = dc.render(pg)
                pw, ph = p.width(), p.height()
                r = mm.mapRect(QRectF(*a))
                rx, ry = r.x(), r.y()
                s_f = {'pg': pg, 'z': self.z(), 
        'v': int((vs.maximum() - vs.minimum() + vs.pageStep()) * (ry - 10) / ph), 
        'h': int((hs.maximum() - hs.minimum() + hs.pageStep()) * (rx - 10) / pw),}

                if s_f != s_i and s_i:
                    self.hst.push(cmd_view(self, s_i, s_f, 
                                           '%s --> %s' % (s_i, s_f)))
                s_i = dict(s_f) 

    def refresh(self, b_reset=False):
        scn = self.scn
        scn.clear()
        
        dd = self.dd
        pg = str(self.pg())
        
        if pg in dd['bxd']:
            z = get_z(dd['bxd'][pg]) * self.width() / (dd['w_desktop'] - 50.)
            # prevent z outlier
            self.set_z(z if z / dd['z'] < 2 else dd['z'])

        zo = dd['zo']
        zz = 2. * self.z() / zo
        self.mm = mm = QTransform(zz, 0, 0, zz, 0, 0)
        
        #self.render_pg_fact()
        try:
            pix = self.doc.pix
            pw, ph = pix.width(), pix.height()
            scn.setSceneRect(0, 0, pw, ph)
            
            #if int(pg) in self.pg_fact:
            #    render_i(pix, self.pg_fact[int(pg)], mm)

            scn.addItem(QGraphicsPixmapItem(pix))
            
            bx = dd['bxd'][pg]
            sp = span(bx)
            x, y, w, h = sp
            r = mm.mapRect(QRectF(*sp))
            rx, ry, rw, rh = r.x(), r.y(), r.width(), r.height()
            
            def set_hv():
                vs = self.verticalScrollBar()
                hs = self.horizontalScrollBar()
                self.set_v(int((vs.maximum() - vs.minimum() + vs.pageStep()) * (ry - 10) / ph))
                self.set_h(int((hs.maximum() - hs.minimum() + hs.pageStep()) * (rx - 10) / pw))
            if b_reset:
                QTimer.singleShot(0, set_hv)

            if self.mode == mode_anno:
                for b in bx:
                    try:
                        tks = dd['tkd'][pg]
                        i = [bb for bb, typ, s, ke in tks].index(b)
                        tk = tks[i]
                    except:
                        tk = [b, '', '', ''] 
                    
                    scn.addItem(box(
                        mm.map(QPointF(*b[:2])), 
                        mm.mapRect(QRectF(QPointF(0, 0), QPointF(*b[2:]))), tk))
            
                yd1, yd2 = dd['yd'][pg]
                for n, y in enumerate([max(yd1, y), min(yd2, y + h)]):
                    scn.addItem(line(mm.map(QPointF(x + w / 2, y)), n))
                
                for b, typ, s, ke in dd['tkd_man'][pg]:            
                    scn.addItem(sep(mm.map(QPointF(*b[:2])), [list(b), typ, s, ke]))
        except:
            pass
            
        self.send(cnd='update')
    
    def set_mode(self, m):
        self.mode = m
        if m == mode_read:
            if self.cursor().shape() == Qt.CrossCursor:
                self.setCursor(Qt.ArrowCursor)
        self.send(cnd='set_mode', mode=m)
    
    def switch_mode(self):
        m = self.mode 
        m += 1
        m %= 2
        self.set_mode(m)
        
    def find(self):
        pass
        
    def restart(self):
        self.send(cnd='restart')
    
    def mousePressEvent(self, e):
        if self.cursor().shape() == Qt.CrossCursor and e.button() == Qt.LeftButton: 
            p = self.mm.inverted()[0].map(self.mapToScene(e.pos()))
            pg = str(self.pg())
            if pg not in self.dd['tkd_man']:
                self.dd['tkd_man'][pg] = []
            self.dd['tkd_man'][pg].append([[p.x(), p.y(), 1000, 0], 'sep', '', ''])
            self.refresh()
        
        else:
            ww, hh = 400, 200
            sz = self.size()
            #po = self.mm.inverted()[0].map(self.mapToScene(QPoint((sz.width()-ww)/2, (sz.height()-hh)/2)))
            #b = [po.x(), po.y(), 400, 200]
            #self.scn.addItem(rubber(self.mm.mapRect(QRectF(*b))))
            #po = self.mapToScene(QPoint((sz.width()-ww)/2, (sz.height()-hh)/2))
            #self.scn.addItem(rubber(QRectF(po.x(), po.y(), 400, 200)))
        QGraphicsView.mousePressEvent(self, e)
    
    #def wheelEvent(self, e):
    #    n = 1.41 ** (-e.delta() / 240.0)
    #    self.scale(n, n)

    # ===================================================
    #  neutral code
    # ===================================================
    def handler_doc(self, d):
        c = d['cnd']

        #if c == 'scroll':
        #    bar = d['bar']
        #    tick = d['tick']
        #    
        #    def scr(b, t):
        #        b.setValue(b.value() + 10 * (1 if tick >= 0 else -1))
        #        
        #    scr(self.horizontalScrollBar() if bar == 'h' else self.verticalScrollBar(), tick)    
        if c == 'before_page_changed':            
            self.before()

        elif c == 'page_changed':
            self.after()
            self.refresh(b_reset=True)

        elif c == 'before_zoom_changed':
            self.before()

        elif c == 'zoom_changed':
            self.after()
            self.refresh(b_reset=True)

    def before(self, n=0):
        self.s_i = self.s()

    def after(self, n=0):
        self.s_f = self.s()

    def remember(self):
        if self.s_i == self.s_f:
            return
        
        self.hst.push(cmd_view(self, self.s_i, self.s_f, 
                               '%s --> %s' % (self.s_i, self.s_f)))
    
    def z_in(self):
        self.zoom(1.25)
        self.remember()

    def z_out(self):
        self.zoom(0.8)
        self.remember()

    def fst(self):
        self.doc.fst()
        self.remember()

    def last(self):
        self.doc.last()
        self.remember()

    def next(self):
        self.doc.next()
        self.remember()

    def prev(self):
        self.doc.prev()
        self.remember()

    def fwd(self):
        self.hst.redo()

    def bwd(self):
        self.hst.undo()

    def set_pg(self, n):
        self.doc.set_pg(n)

    def set_z(self, n):
        self.doc.set_z(n)

    def set_v(self, v):
        self.verticalScrollBar().setValue(v)

    def set_h(self, h):
        self.horizontalScrollBar().setValue(h)

    def set_s(self, s):
        if s:
            self.set_pg(s['pg'])
            self.set_z(s['z'])
            self.set_v(s['v'])
            self.set_h(s['h'])

    def zoom(self, n):
        self.doc.zoom(n)
   
    def pgs(self):
        return self.doc.pgs

    def pg(self):
        return self.doc.pg 

    def z(self):
        return self.doc.z
    
    def s(self):
        return {'pg': self.pg(), 
                'z': self.z(), 
                'v': self.verticalScrollBar().value(), 
                'h': self.horizontalScrollBar().value()}

    def send(self, **d):
        getattr(self, 'msg_%s' % self.n()).emit(d)
    
    def cls(self):
        try:
            shutil.rmtree(self.td)
        except:
            pass

    def n(self):
        return self.__class__.__name__

class win_hrv(QMainWindow, Ui_win_hrv):

    def __init__(self, par=None, name=None, key=None, state=None, typ=hrv_read_rev):
        QMainWindow.__init__(self, par)
        self.setupUi(self)
        attrs_from_dict(locals())
        self.setStyleSheet('*{font: 11pt "Microsoft JhengHei";}')       

        for i, k in [('ed',         ('Ctrl+E',)),
                     ('switch_mode',('F12',))]:

            s = 'act_%s' % i
            setattr(self, s, QAction(self))
            a = getattr(self, s)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            a.triggered.connect(partial(self.handler, i))
            self.addAction(a)

        for i in ['open', 'open_new', 'tab_close', 'tab_close_all', 'save', 
                  'tab_next', 'tab_prev', 
                  'z_in', 'z_out', 'fst', 'last', 'prev', 'next', 
                  'fwd', 'bwd']:
            a = getattr(self, 'act_%s' % i)
            a.triggered.connect(partial(self.handler, i))
            self.addAction(a)

        for i in ['spb_z_', 'spb_pg_', 'spb_z', 'spb_pg']:
            setattr(self, i, QSpinBox(self))
            w = getattr(self, i)
            w.setMinimum(1)
            w.setMaximum(5000)
            w.editingFinished.connect(self.spb_changed)
        
        for i in ['lbl_z_', 'lbl_z']:
            setattr(self, i, QLabel('%'))

        for i in ['lbl_pg_', 'lbl_pg']:
            setattr(self, i, QLabel(' of '))
        
        tb = self.tb
        for k, i in enumerate(['spb_z_', 'lbl_z_', '', 'spb_pg_', 'lbl_pg_', '']):
            setattr(self, 'lbl_%s' % k, QLabel(self))
            w = getattr(self, 'lbl_%s' % k)
            w.setText(u'  ')        
            tb.addWidget(w)
            if i:
                tb.addWidget(getattr(self, i))
            else:
                tb.addSeparator()
            
        # create labels and widgets in stb
        stb = self.stb
        self.stw = stopwatch(self)

        for ii, it in enumerate([('mode',   2),
                                 ('task',  30),
                                 ('spb_z',  1),
                                 ('lbl_z',  1),
                                 ('spb_pg', 3),
                                 ('lbl_pg', 3),
                                 ('stw',    4),
                                 ('count', 10),
                                 ('aux',    6),
                                 ]):

            i, l = it
            if i in ['spb_z', 'spb_pg', 'lbl_z', 'lbl_pg']:
                stb.insertPermanentWidget(ii, getattr(self, i), l)

            else:
                n = 'lbl_%s' % i
                setattr(self, n, QLabel(self))
                w = getattr(self, n)
                if i in ['mode', 'count', 'aux', 'stw']:
                    w.setAlignment(Qt.AlignCenter)
                w.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
                stb.insertPermanentWidget(ii, w, l)
        stb.setSizeGripEnabled(False)
        
        self.tw = t = QTabWidget()
        t.setTabPosition(QTabWidget.West)
        t.setTabsClosable(True)
        t.setDocumentMode(True)
        self.setCentralWidget(t)
        t.currentChanged.connect(self.update_tb)
        t.tabCloseRequested.connect(t.removeTab)
        self.root = cwd 
        
        # manually setup sdb
        self.sdb = sdb = QDockWidget('tokens', self)
        sdb.setObjectName('sdb') 
        sdb.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        
        self.lw = lw = lwd(self)
        self.vw = vw = pix_view(self)
        
        self.spl = spl = QSplitter(Qt.Vertical, self)
        spl.addWidget(lw)
        spl.addWidget(vw)

        w = QWidget(self)
        lo = QVBoxLayout()
        lo.addWidget(spl)
        w.setLayout(lo)
        sdb.setWidget(w)

        self.addDockWidget(Qt.RightDockWidgetArea, sdb)
        
        lw.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        fi = self.focus_item
        lw.itemClicked.connect(fi)
        lw.itemActivated.connect(fi)  
   
        for i in ['full', 'quit',]:
            try:
                a = getattr(self, 'act_%s' % i)
                a.triggered.connect(getattr(self, i)) 
                self.addAction(a)
            except:
                pass 

        n = self.n()
        l = ['mnb', 'tb', 'stb',]

        for i in l:
            a = getattr(self, 'act_show_%s' % i)
            b = sts.value('%s/%s/visible' % (n, i), type=QBool)
            getattr(self, i).setVisible(b)
            a.setChecked(b)
            a.toggled.connect(getattr(self, i).setVisible)
            self.addAction(a) 
        
        self.spl.restoreState(sts.value('%s/spl/state' % n, type=QByteArray))

        self.restoreState(sts.value('%s/state' % n, type=QByteArray))        
        self.resize(sts.value('%s/size' % n, type=QSize))
        self.move(sts.value('%s/pos' % n, type=QPoint))
        
        self.typ = typ 
        self.busy = False 

        if name:
            self.create(name)
            w = self.tw.currentWidget()
            if key:
                QTimer.singleShot(0, partial(w.hst_push, key))    
            else:
                if state:
                    s = json.loads(state)
                    if s:
                        w.set_s(s)
                w.set_mode(mode_read)
            
            if self.typ == hrv_read_rev:
                # introduce learn/rest session management
                self.state, self.interval = st_rest, None
                self.overlay = overlay(self.centralWidget(), False)

                names = [w.dd['name']]
                self.mgr = m = mgr(self, cat('db', 'ananda.db'), names=names) 
                getattr(m, 'msg_%s' % m.n()).connect(self.handler_mgr)
                
        self.startTimer(1000)

    def focus_item(self, i):
        w = self.tw.currentWidget()
        if not w:
            return
        b = item_data(i, 0)
        r = QRectF(w.mm.mapRect(QRect(*b)))
        w.ensureVisible(r)
        p = QPainterPath()
        p.addRect(r)
        w.scn.setSelectionArea(p, QTransform())

    def handler_mgr(self, d):
        c = d['cnd']
        if c == 'rev':
            try:
                w = self.rev
                # XXX w.alarm(bus.get_object(ifc, '/').state())
                w.showMaximized()
                self.msg({'msg': 'reviewing ...'})

            except:
                pass 

        elif c == 'none':
            self.busy = False
    
    def handler_rev(self, d):
        self.busy = False
        self.msg({'msg': ''})

    def handler(self, c):
        if c in ('open', 'open_new'):
            self.open(new_tab=(c=='open_new'))    

        else:
            t = self.tw
            ix = t.currentIndex()
            w = t.currentWidget()

            if w is None or ix == -1:
                return

            if c == 'tab_close':
                t.removeTab(ix)

            elif c == 'tab_close_all':
                t.clear()
            
            elif c == 'tab_next':
                t.setCurrentIndex(ix + 1 if ix < t.count() - 1 else 0)

            elif c == 'tab_prev':
                t.setCurrentIndex(ix - 1 if ix else t.count() - 1)
            
            elif c == 'z_in':
                w.zoom(1.25)
                
            elif c == 'z_out':
                w.zoom(0.8)

            elif c == 'fst': 
                w.fst()        
                
            elif c == 'last': 
                w.last()
                
            elif c == 'prev': 
                w.prev()
                
            elif c == 'next':
                w.next()
                
            elif c == 'fwd':
                w.fwd()
                
            elif c == 'bwd': 
                w.bwd()        
            
            elif c == 'switch_mode':
                w.switch_mode()
            
            elif c == 'ed':
                popen(['python', '/home/cytu/usr/src/py/ananda/ed.py', 
                       '-c', json.dumps({'meta': {'name': w.dd['name'], 
                                         'key': 'page %s' % (w.pg() + 1)}})])  
    def handler_view(self, d): 
        c = d['cnd']

        def update_vw():
            self.vw.load_pix([d.get('f', '')])

        if c == 'update':
            self.update_all()
        
        elif c == 'op_starts':
            self.msg({'msg': 'parsing ...'})

        elif c == 'op_ends':
            self.msg({'msg': 'parsing completed !', 'to': 10000}) 
        
        elif c == 'msg':
            self.msg({'msg': d['msg']}) 
        
        elif c == 'pg_fact:error':
            self.msg({'msg': 'error rendering fact ...', 'to': 10000})
            update_vw()

        elif c == 'pg_fact:done':
            self.msg({'msg': 'fact rendered !', 'to': 10000})
            update_vw()

        elif c == 'pg_fact:none':
            self.msg({'msg': 'no fact on this page ...', 'to': 10000})
            update_vw()

        elif c == 'saved':
            self.msg({'msg': 'saved!', 'to': 10000})
            self.msg({'msg': d['count']}, 'count')
            if self.typ == hrv_edt:
                getattr(self, 'msg_%s' % self.n()).emit()
                self.close()

        elif c == 'set_mode':
            self.sdb.setVisible(d['mode'] == mode_anno)
        
        elif c == 'restart':
            w = self.tw.currentWidget()
            if not w:
                return

            @atexit.register   
            def restart():
                popen(['python', '/home/cytu/usr/src/py/ananda/hrv.py', '-n', w.dd['name']])
            
            self.close()

    def update_stb(self, tl):
        for sct, s in tl:
            self.msg({'msg': s}, sct)

    def msg(self, d, sct='task'):
        lbl = getattr(self, 'lbl_%s' % sct)
        msg = '<font color="%s">%s</font>' % ('blue', d.get('msg', ''))
        to = d.get('to', 0)
        lbl.setText(msg)
        
        if to:
            QTimer.singleShot(to, partial(lbl.setText, ''))
    
    def spb_changed(self):
        w = self.tw.currentWidget()
        if w is None:
            return

        spb = self.sender()
        if spb is self.spb_pg_ or spb is self.spb_pg:
            w.set_pg(spb.value() - 1)
            w.remember()

        elif spb is self.spb_z_ or spb is self.spb_z:
            w.set_z(spb.value() / 100.)

    def update_tb(self, i=0):
        tw = self.tw
        w = tw.widget(i) if i else tw.currentWidget()
        try: 
            self.setWindowTitle('%s -- [Ebook Harvester]'  % tw.tabText(i))
        except:
            pass

        if w is not None:
            for i in ['lbl_pg_', 'lbl_pg']:
                getattr(self, i).setText('  of   %s' % w.pgs())

            for i in ['spb_pg_', 'spb_pg']:
                spb = getattr(self, i)
                spb.setValue(w.pg() + 1)
                spb.setMaximum(w.pgs())
            
            for i in ['spb_z', 'spb_z_']:
                getattr(self, i).setValue(int(100 * w.z()))
            
    def update_all(self):
        self.update_tb()
        self.lw.clear()
        
        w = self.tw.currentWidget()
        if w is None:
            return
        
        m = w.mode
        if m == mode_anno:
            pg = str(w.pg())
            dd = w.dd
            tkd = []
            for i in ['tkd', 'tkd_man']:
                try:
                    tkd.extend(dd[i][pg])
                except:
                    pass

            for b, tk, s, ke in sorted(tkd, key=lambda b:b[0][1]):
                it = QListWidgetItem('[ %s ] %s' % (tk, s) + (' [k: %s]' % ke if ke else ''))
                it.setData(Qt.UserRole, QVariant(json.dumps([b, tk, s, ke])))
                self.lw.addItem(it)
        
        if m == mode_anno: 
            s = 'frame_edit' 

        elif m == mode_read:
            s = 'viewer'
        
        self.lbl_mode.setPixmap(QPixmap(':/res/img/%s.png' % s))
        
    def create(self, name, new_tab=False):
        try:
            dd = get_ana(name) 
            t = self.tw
            i = t.currentIndex()
            fn, typ = os.path.splitext(os.path.basename(dd['src']))
            f = ellipsis(fn)
            icon = QIcon(':/res/img/%s.png' % typ.lower()[1:])
            
            vw = view(dd=dd)
            if i != -1:
                if new_tab:
                    i = t.addTab(vw, icon, f)
                    t.setCurrentIndex(t.count() - 1)                 
                else:
                    t.removeTab(i)
                    t.insertTab(i, vw, icon, f)
                    t.setCurrentIndex(i)
            
            else:
                i = t.addTab(vw, icon, f)
            
            w = t.widget(i)
            getattr(w, SIGNAL('msg_%s' % vw.n())).connect(self.handler_view)
            w.setFocus()
            
            w.set_s(dd.get('last_state', {}))

            return True
        
        except:
            return False
    
    def open(self, new_tab=True):
        dlg = QFileDialog(self)
        dlg.setDirectory(self.root)
        dlg.setFileMode(QFileDialog.ExistingFiles)
        dlg.setNameFilter('Ananda Ebook Data File (*.ana)')
        if dlg.exec_():
            fl = dlg.selectedFiles()
            fl_failed = []
            for f in fl:
                try:
                    f = unicode(f)
                    self.root = os.path.dirname(f)
                    name = os.path.splitext(os.path.split(f)[1])[0]
                    if not self.create(name, new_tab=new_tab):
                        fl_failed.append(f) 
                except:
                    fl_failed.append(f) 
            
            if fl_failed:
                QMessageBox.warning(self, 'Ebook Harvester: Failed to Open File(s)',
            'The following files could not be opened:\n%s' % '\n'.join(fl_failed))
         
    def find(self):
        #self.tw.currentWidget().ensureVisible(hit.x(), hit.y())
        pass
       
    def quit(self):
        for i in range(self.tw.count()):
            w = self.tw.widget(i)
            if self.typ != hrv_edt: # not to save again
                w.save()
            w.cls()
        self.cls()

    def full(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def cls(self):
        n = self.n()
        if not self.isFullScreen() and not self.isMaximized():
            sts.setValue(f'{n}/size', QVariant(self.size()))
        
        #sts.setValue(f'{n}/state', QVariant(self.saveState()))        
        sts.setValue(f'{n}/spl/state', QVariant(self.spl.saveState()))

        l = ['mnb', 'stb', 'tb',]
        for i in l:
            sts.setValue(f'{n}/{i}/visible', QVariant(getattr(self, i).isVisible()))

    def n(self):
        return self.__class__.__name__
        
    def alarm(self, s):
        d = json.loads(s)
        for k, v in d.iteritems():
            setattr(self, k, v)
        
        if self.typ != hrv_read_rev:
            return

        o = self.overlay
        st = self.state
        if st == st_learn:
            o.hide()
            self.busy = False
            
        elif st == st_rest:
            self.close()
            #self.rev.close() 
            #o.show()
            #self.busy = True
        
        elif st == st_none:
            self.close()

    def closeEvent(self, e):
        self.quit()
    
    def timerEvent(self, e):
        if self.typ != hrv_read_rev:
            return
        
        st = self.state
        i = self.interval
        if i: 
            a, b = self.interval
            t0 = str2dt(a)
            t1 = str2dt(now(utc=False))
            t2 = str2dt(b)
            T = t2 - t0

            if st == st_learn:
                t = (t1 - t0) if t1 > t0 else (t0 - t1)
                tp = ('orange', '[ %d%% ]' % int(100. * t.seconds / T.seconds), 
                        nr2t(t.seconds))

            elif st == st_rest:
                t = (t2 - t1) if t2 > t1 else (t1 - t2)
                tp = ('green', 'rest', nr2t(t.seconds))
            
            else:
                tp = ('red', '?', '')
        else:
            tp = ('red', '?', '')
       
        self.update_stb([
            #('stw', '<font color="purple">%s</font>' % (nr2t(self.stw.cnt / 10) if st == st_learn else '')),
            ('aux', '<font color="%s">%s&nbsp; %s</font>' % tp if tp != ('red', '?', '') else ''),])

        if self.busy:
            return
        self.mgr.go()
        self.busy = True

    def event(self, e):
        try:
            typ = e.type()
            if typ == QEvent.WindowActivate:
                self.stw.start() 
            
            elif typ == QEvent.WindowDeactivate:
                self.stw.stop()
        finally:
            return QMainWindow.event(self, e) 

if __name__ == '__main__':
    argv = sys.argv
    app = QApplication(argv)
    app.setApplicationName('rdr')
    app.setFont(QFont('Microsoft JhengHei'))

    argc = len(argv)
    ps = argparse.ArgumentParser(description='Ananda Ebook Reader')
    ps.add_argument('-f', '--files', nargs='+', dest='files')
    ps.add_argument('-s', '--state', dest='state')
    ps.add_argument('-t', '--type', type=int, dest='typ')
    
    if argc == 1:
        # use in test
        al = ['-n', 'dacorogna0', '-t', str(hrv_read_rev)]    

    elif argc == 2:
        # use in *.ana file browsing 
        al = ['-n', f_no_ext(argv[1]), '-t', str(hrv_read)] 
        
    else:
        al = argv[1:] if argc else []

    w = win_rdr(**ps.parse_args(al).__dict__)
    w.showMaximized()

    app.exec()
