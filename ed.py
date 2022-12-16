from base import *

def item(txt, icon):
    i = QTreeWidgetItem()
    i.setText(0, txt)
    i.setIcon(0, QIcon(icon))
    return i
    
def qas2db(qas, cr, fact_id=0, name=''):
    try:
        orig = json.loads(fact(fact_id, cr)[0])
    except:
        orig = {'meta': {'name': name if name else 'gen' , 
                         'key': str(datetime.datetime.utcnow())},}
    def distill(d):
        for i in ['q', 'a']:
            d[i] = [dd for dd in d[i] if test(dd) not in (AV, TXT, PIX)]
        return d 

    tt = []
    for j, qa in enumerate(qas):
        # XXX tmp measure to add audio/text/pix without touching others (eg. ebk)
        try:
            d = distill(orig['qas'][j])
        except:
            d = {'q': [], 'a': []}

        for i in ['q', 'a']:
            try:            
                a = qa['%s_audio' % i]
                if a:
                    d[i].append({'sha': os.path.split(a)[-1], 'f': a, 
                                 'start': '', 'stop': ''})
            except:
                pass
            
            try:
                t = qa['%s_text' % i].strip()
                if t:
                    d[i].append({'txt': t})
            except:
                pass

            try:
                p = qa['%s_pix' % i]
                if p:
                    d[i].append({'sha': os.path.split(a)[-1], 'f': a, 'qry': ''})
            except:
                pass

        # not be strict? XXX
        #if d['q'] and d['a']:
        if d['q'] or d['a']:
            tt.append(d)
    
    orig['qas'] = tt
    return orig 

def db2qas(fact_id, td, cr):
    l = []
    r = fact(fact_id, cr)
    if r:
        qas = json.loads(r[0])
        for qa in qas['qas']:
            d = {}.fromkeys(['q_audio', 'a_audio', 'q_text', 'a_text', 
                             'q_pix', 'a_pix'], '')
            for s in ['q', 'a']:
                for dd in qa[s]:
                    t = test(dd)
                    if t in (AV, PIX):
                        f, meta = load_f(dd['sha'], td, cr)
                        d['%s_%s' % (s, 'audio' if t == AV else 'pix')] = f
                    elif t == TXT:
                        d['%s_text' % s] = dd['txt']
            l.append(d)
    return l

class cmd_ed(QUndoCommand):
    
    def __init__(self, dsc):
        super(cmd_ed, self).__init__(dsc)
        attrs_from_dict(locals())
    
    def redo(self):
        pass

    def undo(self):
        pass

class twg(QTreeWidget):
    
    twg_delete = pyqtSignal(str)
    twg_update = pyqtSignal(str)

    def __init__(self, par):
        super(twg, self).__init__(par)

    def keyPressEvent(self, e):
        i = self.currentItem()
        if i is None:
            QTreeWidget.keyPressEvent(self, e)
        else:
            k = e.key()
            if k == Qt.Key_Delete:
                self.twg_delete.emit(item_data(i, 'key'))
            else:
                QTreeWidget.keyPressEvent(self, e)

    def keyReleaseEvent(self, e):
        i = self.currentItem()
        if i is None:
            QTreeWidget.keyReleaseEvent(self, e)
        else:
            k = e.key()    
            if k in (Qt.Key_Up, Qt.Key_Down):
                self.twg_update.emit(item_data(i, 'key'))
            else:
                QTreeWidget.keyReleaseEvent(self, e)

class edt(QTextEdit):
    
    msg_edt = pyqtSignal()

    def __init__(self, par):
        super(edt, self).__init__(par)
        self.setAcceptRichText(False)

    # note that we can't use the keyPressEvent!
    def keyReleaseEvent(self, e):
        self.msg_edt.emit()
        QTextEdit.keyReleaseEvent(self, e)

class win_ed(QMainWindow):
    
    msg_win_ed = pyqtSignal(dict)

    def __init__(self, par=None, fact_id=0, slide=0, name=None):
        QMainWindow.__init__(self, par)
        
        attrs_from_dict(locals())
        
        self.setWindowTitle(u'Q/A Editor')
        self.setWindowIcon(QIcon(':/res/img/view_list_details.png'))
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.Dialog)
        
        td = getattr(par, 'td', '')
        self.has_par = td 
        self.td = td if td else tempfile.mkdtemp(prefix='%s_%s_' % (self.n(), now().replace(':', '')), dir=cat(os.getcwd(), tmp)) 
        
        wdg = QWidget(self)
        hlo = QHBoxLayout(wdg)
        self.spl = QSplitter(wdg)
        self.spl.setOrientation(Qt.Horizontal)
        
        self.tw = tw = twg(self.spl)
        tw.setHeaderLabel(u'Q/A Pairs')
        tw.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tw.setSelectionMode(QAbstractItemView.SingleSelection)
        p = self.preview
        tw.itemClicked.connect(p)
        tw.itemActivated.connect(p)  
        tw.twg_update.connect(self.update_item)
        tw.twg_delete.connect(self.delete_item)

        w = QWidget(self.spl)
        vlo = QVBoxLayout(w)
        vlo.setContentsMargins(0, 0, 0, 0)

        for i in ['q', 'a']:
            s = 'ed_%s' % i
            setattr(self, s, edt(w))
            ed = getattr(self, s) 
            ed.setFont(QFont('Microsoft JhengHei', 20, QFont.Black))
            ed.setTabChangesFocus(True)
            ed.msg_edt.connect(self.update_text)
            vlo.addWidget(ed)
        
        hlo.addWidget(self.spl)
        self.setCentralWidget(wdg)
        
        self.av = av = wdg_a(self)
        av.hide()
        av.msg_av.connect(self.handler_av)
        
        for i, k in [('save',        ('F2', 'Ctrl+S',)), 
                     ('add_qa',      ('F3', 'Ctrl+T',)),
                     ('rec',         ('F4',)),
                     ('preview_htm', ('F5',)),
                     ('flip',        ('Ctrl+M',)),
                     ('quit',        ('Esc',)),]:
            n = 'act_%s' % i
            setattr(self, n, QAction(self))
            a = getattr(self, n)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            a.triggered.connect(getattr(self, i)) 
            self.addAction(a)

        # setup stb
        stb = QStatusBar(self)
        self.setStatusBar(stb)
        for ii, (i, l) in enumerate([('rec',  1),
                                     ('side', 1),
                                     ('gen',  23)]):
            n = 'lbl_%s' % i
            setattr(self, n, QLabel(self))
            w = getattr(self, n)
            w.setAlignment(Qt.AlignCenter)
            w.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
            stb.insertPermanentWidget(ii, w, l)
        stb.setSizeGripEnabled(False)
        
        n = self.n()
        self.restoreState(sts.value('%s/state' % n, type=QByteArray))
        self.resize(sts.value('%s/size' % n, type=QSize))
        self.move(sts.value('%s/pos' % n, type=QPoint))
        self.spl.restoreState(sts.value('%s/spl' % n, type=QByteArray))        
         
        self.hst = QUndoStack(self)
        
        try:
            self.cn = cn = getattr(par, 'cn') 
            self.reset(db2qas(self.fact_id, self.td, cn.cursor()), self.slide)
            self.mgr = getattr(par, 'mgr')

        except:
            #from db.make_db import make_db
            #db = cat('db', 'adhoc.db')
            #if not os.path.isfile(db):
            #    make_db(sqlite3.connect(db))
            #self.cn = cn = sqlite3.connect(db)
            #cr = cn.cursor()
            #cr.execute('drop table if exists prefab')
            #cn.commit()
            #self.mgr = mgr_due(self, db)
            self.cn = sqlite3.connect(cat('db', 'ananda.db'))
            self.reset()
        
    def send(self, **d):
        self.msg_win_ed.emit(d)

    def n(self):
        return self.__class__.__name__

    def alarm(self, d):
        for k, v in d.items():
            setattr(self, k, v)
        
    def reset(self, qas=None, slide=0):
        self.qas = qas
        self.slide = slide 
        self.build_tw()

    def add_qa(self):
        self.slide += 1
        self.qas.insert(self.slide, 
            {}.fromkeys(['q_audio', 'a_audio', 'q_text', 'a_text'], ''))
        
        # Item data might have been changed, so rebuild tw.
        self.build_tw()
    
    def save(self):
        fact_id = self.fact_id
        cn = self.cn
        save_fact(qas2db(self.qas, cn.cursor(), fact_id, self.name), cn, fact_id=fact_id)
        # XXX 08/30/14
        # QTextEdit in this version may have strange problems rendering CJK symbols which will result data loss !!! One can only use copy-and-paste to insert CJK symbols, other ways are not possible.
        if fact_id: 
            # edit existing fact
            QTimer.singleShot(1000, self.close)
        else:
            self.reset()
        self.send(cnd='saved')
        self.play_audio('/home/cytu/usr/src/py/ananda/res/av/saved.mp3')

    def update_slide(self, b=True):
        slide = self.slide
        
        # update ed
        if self.qas:
            qa = self.qas[slide]
            for s in ['q', 'a']:
                s_t = '%s_text' % s
                ed = getattr(self, 'ed_%s' % s)
                ed.clear()
                ed.setPlainText(qa[s_t])
        if b:
            self.update_elem(self.tw.topLevelItem(slide), slide)
        
    def update_text(self, b=True):
        slide = self.slide
        
        if self.qas:
            for s in ['q', 'a']:
                self.qas[slide]['%s_text' % s] = getattr(self, 'ed_%s' % s).toPlainText()
        
        # update tw 
        if b:
            self.update_elem(self.tw.topLevelItem(slide), slide)

    def update_item(self, k):
        # update text only.
        self.update_text(False)
        
        slide, typ = k  
        if slide != self.slide:
            self.slide = slide
            self.update_slide(False)

    def delete_item(self, k):
        slide, typ = k
        if typ == 'qa':
            self.qas.pop(slide)
            if self.qas:
                if self.slide:
                    self.slide -= 1
            
            self.build_tw()

        else:
            self.qas[slide][typ] = ''
            self.update_slide()

    def build_tw(self):
        tw = self.tw
        tw.clear()
        
        if not self.qas:
            self.qas = [{}.fromkeys(['q_audio', 'a_audio', 'q_text', 'a_text'], '')]
            self.slide = 0

        for ii, qa in enumerate(self.qas): 
            i = item('Q/A %s' % str(ii + 1), ':/res/img/package_education.png')
            i.setData(Qt.UserRole, 0, QVariant(json.dumps({'key': (ii, 'qa')})))
            self.update_elem(i, ii)
            tw.addTopLevelItem(i)
        tw.setCurrentItem(tw.topLevelItem(self.slide))

        # set to side q
        self.flip(0)
        
        self.update_slide()

    def handler_av(self, d):
        c = d['cnd']
        if c == 'rec_start':
            self.lbl_rec.setPixmap(QPixmap(':/res/img/audio_headset.png'))

        elif c == 'rec_stop':
            self.lbl_rec.setPixmap(QPixmap())
            
            self.qas[self.slide]['%s_audio' % ('a' if self.side == 1 else 'q')] = d['f']
            # automatically switch side.
            self.flip()
            self.update_slide()

    def update_elem(self, i, ii):
        if not self.qas or i is None:
            return
        
        i.takeChildren()
        tw = self.tw

        b = True
        for s in ['q', 'a']:
            s_a, s_t = '%s_audio' % s, '%s_text' % s
            a = self.qas[ii][s_a]

            if a:
                ia = item(s_a, ':/res/img/kmix.png')
                ia.setData(Qt.UserRole, 0, 
                           QVariant(json.dumps({'key': (ii, s_a), 'a': a})))
                i.addChild(ia)
                tw.setCurrentItem(ia)
                if b:
                    b = False

            t = self.qas[ii][s_t]
            if t.strip():
                it = item(s_t, ':/res/img/tex.png')
                it.setData(Qt.UserRole, 0, QVariant(json.dumps({'key': (ii, s_t)})))
                i.addChild(it)
                tw.setCurrentItem(it) 
                if b:
                    b = False
        if b:
            tw.setCurrentItem(i)

        tw.expandAll()

    def flip(self, side=None):
        self.side = side if side is not None else (0 if self.side == 1 else 1)
        self.update_stb()

    def navigate(self, forward=True):
        if self.qas:
            self.slide = self.slide + (1 if forward else -1)
            self.slide %= len(self.qas)
        else:
            self.slide = 0

    def rec(self):
        self.av.rec()
    
    def preview(self, i, col):
        slide, typ = item_data(i, 'key')
        if typ.find('audio') != -1:
            self.play_audio(item_data(i, 'a'))
        
        self.slide = slide
        self.update_slide(False)
    
    def preview_htm(self):
        tl = []
        for qa in self.qas:
            tq, ta = qa['q_text'].strip(), qa['a_text'].strip()
            if tq or ta:
                tl.append('<div class="question_pre">%s</div><div class="answer_pre">%s</div>' % (tq, ta))
                 
        self.win_b = win_b(self, htm('\n'.join(tl), 
            css='usr/src/py/ananda/res/ananda_prv.css', b_math=True))
        self.win_b.showMaximized()

    def play_audio(self, src):
        a = self.av
        a.set_src(src)
        a.play()

    def quit(self):
        self.close()
         
    def update_stb(self):
        s = 'a' if self.side else 'q'
        
        self.cn.create_function('meta_name', 1, meta_name)
        self.cn.create_function('meta_key', 1, meta_key)
        
        cr = self.cn.cursor()
        n_fact_today_all = n_fact(cr, (today(), tomorrow()))
        n_fact_all = n_fact(cr, names=['gen',])
        
        for i, t in [('side', '<font color="blue">%s</font>' % s.upper()), 
                     ('gen', ('&nbsp;' * 2).join([
                '<font color="purple">today: %s</font>' % n_fact_today_all,
                '<font color="goldenrod">all: %s</font>' % n_fact_all,
                ]))]:
            getattr(self, 'lbl_%s' % i).setText(t)

        getattr(self, 'ed_%s' % s).setFocus()

    def closeEvent(self, e):
        n = self.n()
        sts.setValue('%s/state' % n, self.saveState())
        sts.setValue('%s/spl' % n, self.spl.saveState())
        sts.setValue('%s/size' % n, QVariant(self.size()))
        sts.setValue('%s/pos' % n, QVariant(self.pos()))
        
        if not self.has_par:
            shutil.rmtree(self.td)

if __name__ == '__main__':
    DBusQtMainLoop(set_as_default=True) 
    argv = sys.argv 
    
    app = QApplication(argv)
    app.setApplicationName('ed')
    app.setFont(QFont('Microsoft JhengHei'))
    
    argc = len(argv)

    ps = argparse.ArgumentParser(description='Ad Hoc Editor')
    ps.add_argument('-n', '--name', dest='name')
    
    w = win_ed(**ps.parse_args(argv[1:] if argc else []).__dict__)
    w.show()

    bus = dbus.SessionBus()
    ifc = 'ananda.ctrl'
    bus.add_signal_receiver(w.alarm, dbus_interface=ifc, signal_name='alarm')
    try:
        w.alarm(bus.get_object(ifc, '/').state())
    except:
        pass 

    app.exec_()
