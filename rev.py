from base import *
from ed import win_ed

class win_rev(QMainWindow):

    msg_win_rev = pyqtSignal(dict)

    lstw = ['stw', 'stw1'] 
    lstb = [('descr', 18, 'q-a info'),
            ('typ',    8, 'q-a type | part'), 
            ('stw',    6, 'active time of this fact'),
            ('n_span', 6, 'logged active time: today'),
            ('n_hist',12, 'history'),
            ('n_rev', 12, '#rev: due | done | done distinct | done today | done today distinct'),
            ('n_fact', 9, '#made: in this period | today | all'),
            ('aux',    9, 'session status'),]

    def __init__(self, par=None, mgr=None, names=None, db_file=None):

        QMainWindow.__init__(self, par)
        self.setWindowIcon(QIcon(':/res/img/x-office-presentation.png'))

        self.par = par
        self.td = getattr(par, 'td') if par else tempfile.mkdtemp(prefix=f"{self.n()}_{now().replace(':', '').replace(' ', '_')}_", dir=cat(os.getcwd(), tmp))
    
        self.b = b = browser(self)
        self.setCentralWidget(b)
        b.setFocusPolicy(Qt.NoFocus)
        
        for i, k in [('show_q',  ('Q',)), 
                     ('show_a',  ('A',)), 
                     ('edit',    ('E',)), 
                     ('ebk',     ('K',)),
                     ('forward', ('Right',)), 
                     ('backward',('Left',)),
                     ('delete',  ('Ctrl+Del',)), 
                     ('defer',   ('Ctrl+D',)),
                     ('defer_1d',('Ctrl+F',)),
                     ('full',    ('F11',)),
                     ('reset',   ('U',)),
                     ('grade_1', ('1', )),#'Return')), 
                     ('grade_2', ('2', )), 
                     ('grade_3', ('3', )),#'Space',)),  
                     ('grade_4', ('4', )),
                     ('grade_5', ('5', )),#'Shift+Space')),
                     ('vim',     ('V',)),
                    ]:

            s = f'act_{i}'
            setattr(self, s, QAction(self))
            a = getattr(self, s)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            a.triggered.connect(partial(self.handler, {'cnd': i}))
            self.addAction(a)
            
        self.setup_stb()

        self.tmr = t = QTimer(self)
        t.timeout.connect(self.handler_tmr)
        t.start(1000)
        
        for i in self.lstw:
            setattr(self, i, stopwatch(self))
        
        self.busy = False
        self.state, self.interval = st_rest, None
        self.reset()
        self.startTimer(1000)
    
        n = self.n()
        self.restoreState(sts.value(f'{n}/state', type=QByteArray))        
        self.resize(sts.value(f'{n}/size', type=QSize))
        self.move(sts.value(f'{n}/pos', type=QPoint))

        self.av = av = wdg_a(self)
        av.hide()
        
        self.names = names
        self.b_prefab = False
        if mgr is None:
            self.b_prefab = True
            mgr = mgr_due(self, db_file if db_file else cat('db', 'ananda_temp.db'), names=names)
        self.setup_mgr(mgr)

        # vim netbean interfaces
        self.nb = nb()
        self.nb_port = 24292 
        self.nb_name = 'rev'
        self.nb.listen(QHostAddress('127.0.0.1'), self.nb_port)
        self.nb.msg_vim.connect(self.handler_vim)
        
        # ananda signal handler
        self.signal_handler = DBusSignalHandler(self)
        self.signal_handler.alarmReceived.connect(self.alarm)
        
    def send(self, **d):
        self.msg_win_rev.emit(d)

    def n(self):
        return self.__class__.__name__

    def handler_vim(self, d):
        c = d['cnd'] 
        fact_id = self.d.get('fact_id', 0)
        cn = self.cn
        cr = cn.cursor()
        nn = self.nb_name
        if c == 'key':
            k = d['keycode']            
            if k == 'F2':
                dd = json.loads(fact(fact_id, cr)[0])
                if 'note' not in dd:
                    dd['note'] = {}
                dd['note'] = vim_get(nn)
                update_fact(json.dumps(dd), fact_id, cr)
                cn.commit()
                vim_kill(nn)

            elif k == 'F11':
                if getattr(self, 'w_prv', None) is None:
                    self.w_prv = win_b(self, nb_name=nn) 
                self.w_prv.set_htm(htm(vim_get(nn), css='/home/cytu/usr/src/py/ananda/res/ananda_prv.css', b_math=True))
                self.w_prv.show()
            
            elif k == 'F12':
                focus(all_w(self.nb_name.upper())['prv'])

        elif c == 'killed':
            self.pg_vim = -1
            # close orphaned previewer
            try:
                self.w_prv.close()
            except:
                pass
         
        #elif c == 'insert':
        #    pass

    def start_vim(self, content=''):
        sh = QTimer.singleShot
        nn = self.nb_name
        port = self.nb_port
        ff = partial
        sh(0, ff(vim_gui, nn))
        sh(100, ff(vim_mv, nn))
        sh(200, ff(vim_nb, nn, port))

        ks = ['F2', 'F11', 'F12']         
        t = ['set ft=tex bt=nofile bh=unload noswf']
        t.extend([r'imap <%s> <c-\><c-n><%s>a' % (k, k) for k in ks])
        
        sh(1500, ff(self.nb.send, '1:create!1\n' + ''.join([f'1:specialKeys!{i + 2} "{k}"\n' for i, k in enumerate(ks)])))        
        sh(2000, ff(vim_buf, nn, self.td, '\n'.join(t)))
        sh(2200, ff(vim_set, nn, content, True))

    def setup_stb(self):
        self.stb = stb = QStatusBar(self)
        self.setStatusBar(stb)
        
        for ii, (i, l, tlt) in enumerate(self.lstb):
            n = f'lbl_{i}'
            setattr(self, n, QLabel(self))
            w = getattr(self, n)
            w.setToolTip(tlt)
            w.setAlignment(Qt.AlignCenter)
            w.setScaledContents(True)
            w.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
            stb.insertPermanentWidget(ii, w, l)
        stb.setSizeGripEnabled(False)

    def setup_mgr(self, mgr):
        self.mgr = m = mgr
        m.msg_thread.connect(self.handler_mgr)
        self.cn = cn = sqlite3.connect(m.db)
        cn.create_function('meta_name', 1, meta_name)
        cn.create_function('meta_key', 1, meta_key)

    def handler(self, d):
        c = d['cnd'] 
        fact_id = self.d.get('fact_id', 0)
        
        if c == 'show_q':           
            self.show_qa('q')

        elif c == 'show_a':           
            self.show_qa('a')

        elif c.find('grade_') != -1:
            self.grade(c.split('_')[-1])

        elif c in ('forward', 'backward'):
            self.navigate(True if c == 'forward' else False)
        
        elif c == 'full':
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

        elif c == 'edit':
            self.ed = ed = win_ed(self, fact_id=fact_id, slide=self.slide)
            ed.setWindowModality(Qt.WindowModal)
            ed.show()
            ed.msg_win_ed.connect(self.edited)

            cn = self.cn
            cr = cn.cursor()
            name, k = get_name_key(fact_id, cr)
            if name == 'de_grundwortschatz':
                # XXX try to find longest q
                qas = json.loads(fact(fact_id, cr)[0])['qas']
                txt = ''
                for jj in qas:
                    for comp in jj['q']:
                        for d in comp:
                            t = test(d)
                            if t == TXT:
                                txt_ = comp['txt']
                                if len(txt_) >= len(txt):
                                    txt = txt_
                subprocess.Popen(['gvim', f'+/{txt}', '/home/cytu/usr/doc/lang/txt/Grundwortschatz.txt'])
        
        elif c == 'reset':
            self.stw.reset()
        
        elif c in ('delete', 'defer', 'defer_1d', 'ebk'):
            cn = self.cn
            cr = cn.cursor()
            name, k = get_name_key(fact_id, cr)
            if c == 'delete':
                d = get_ana(name)
                if 'del' not in d:
                    d['del'] = []
                d['del'].append(k)
                save_ana(d)
                delete_fact(fact_id, cn) 
                self.prepare(s=f'Fact [{name} {k}] deleted. Waiting for due fact...')

            elif c == 'ebk':
                if self.par is None and not is_lang(name):
                    from hrv import win_hrv
                    w = win_hrv(self, name=name, key=k, typ=hrv_edt)
                    w.msg_win_hrv.connect(self.handler_hrv)
                    w.showMaximized()
            
            elif (c == 'defer' or c == 'defer_1d'):
                defer_rev(self.d.get('rev_id', 0), 6 if c == 'defer' else 24, cn)
                self.prepare(s=f"Fact [{name} {k}] deferred for {'6' if c == 'defer' else '24'} hours. Waiting for due fact...")

        # XXX update fact
        #elif c in ('doubt', 'important'):
        #    cn = self.cn
        #    cr = cn.cursor()
        #    d = json.loads(fact(fact_id, cr)[0])
        #    d['meta']['value'] = (1 if c == 'doubt' else 2)
        #    update_fact(json.dumps(d), fact_id, cr)
        #    cn.commit()

        elif c == 'vim':
            if getattr(self, 'pg_vim', -1) >= 0:
                return
            self.pg_vim = 0
            try:
                content =  json.loads(fact(fact_id, self.cn.cursor())[0])['note']
            except:
                content = ''
            self.start_vim(content)

    def handler_tmr(self):
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
                tp = ('orange', f'[ {int(100. * t.seconds / T.seconds)}% ]', nr2t(t.seconds))

            elif st == st_rest:
                t = (t2 - t1) if t2 > t1 else (t1 - t2)
                tp = ('green', 'rest', nr2t(t.seconds))
            
            else:
                tp = ('red', '?', '')
        else:
            tp = ('red', '?', '')
       
        self.update_stb([
            ('stw', f"<font color='purple'>{nr2t(self.stw.cnt / 10) if st == st_learn else ''}</font>"),
            ('aux', '<font color="%s">%s&nbsp; %s</font>' % tp if tp != ('red', '?', '') else ''),])
        
    def handler_mgr(self, d):
        c = d['cnd'] 
        if c == 'rev':
            if self.state in (st_learn, st_rest):
            #    self.play_audio('/home/cytu/usr/src/py/ananda/res/av/due_rev.mp3')
                self.rev(d)

        elif c in ['none: no active category', 'none: all done']:
            s = 'No Active Category ...' if c == 'none: no active category' else 'All Done!'
            self.b.set_htm(s)
            #self.busy = False
            if self.par:
                self.close()
        
    def handler_hrv(self):
        fact_id = self.d.get('fact_id', 0)
        cn = self.cn
        cr = cn.cursor()
        name, k = get_name_key(fact_id, cr)
        fk = fact_key(k, get_ana(name))
        if fk:
            cr.execute('update fact set data = ? where id = ?', (fk, fact_id))
            cn.commit()
            self.prepare(s=f'Fact [ {name}  {k} ] updated!')

    def prepare(self, to=500, s=''): 
        self.reset(s)
        def f():
            self.busy = False
        QTimer.singleShot(to, f)
    
    def alarm(self, s):
        self.last_state = self.state

        d = json.loads(s)
        for k, v in d.items():
            setattr(self, k, v)

        self.busy = True
        
        st = self.state
        if st == st_learn:
            #if self.par is None:
            #    self.play_audio('/home/cytu/usr/src/py/ananda/res/av/learn.mp3')
            self.prepare(to=2000)

        elif st == st_rest:
            if self.par is None:
                self.close()
            #if self.par is None:
            #    self.play_audio('/home/cytu/usr/src/py/ananda/res/av/rest.mp3')
            #    self.reset('Take a Rest Now.')
            #    self.update_stb([('descr', ''), ('typ', ''), ('n_span', ''), ('n_rev', ''), ('n_fact', ''),])
        
        elif st == st_none:
            self.close()

    def rev(self, d):
        self.d = d
        self.qas = d['qas']
        self.gr = [-1] * len(self.qas)
        self.qa_span = [-1] * len(self.qas)
        cr = self.cn.cursor()
        fact_id = d.get('fact_id', 0)

        # this is the only safe way!
        self.slide = 0
        
        h = history(fact_id, cr)
        
        # check if this is the first time
        self.b_debut = False
        if h['s_last_at']:
            self.q_or_a = 'q'
            self.show_qa('q')
        else:
            self.q_or_a = 'a'
            self.show_qa('a')
            self.b_debut = True
        
        # XXX
        if self.last_state != self.state:
            self.last_state = self.state
        else:
            for i in self.lstw:
                getattr(self, i).reset()

        names = self.names 
        i = self.interval
        if i:
            i = map(utcstr, i)
        day = (today(), tomorrow())
        #n_span_period = nr2t(n_span(cr, i, names=names))
        n_span_today = nr2t(n_span(cr, day, names=names))
        n_span_today_all = nr2t(n_span(cr, day))

        n_rev_due_period = n_rev_due(cr, i, b_prefab=self.b_prefab, names=names)
        n_rev_done_period = n_rev(cr, i, names=names)
        n_rev_done_period_dst = n_rev(cr, i, True, names=names)
        n_rev_done_today = n_rev(cr, day, names=names)
        n_rev_done_today_dst = n_rev(cr, day, True, names=names)

        n_fact_period = n_fact(cr, i, names=names)
        n_fact_today_all = n_fact(cr, day, names=names)
        n_fact_all = n_fact(cr, names=names)
         
        tl = []
        tl.append(('n_fact', ('&nbsp;' * 3).join([
            f'<font color="blue">{n_fact_period}</font>',
            f'<font color="purple">{n_fact_today_all}</font>',
            f'<font color="goldenrod">{n_fact_all}</font>',
            ])))
        
        tl.append(('n_span', ('&nbsp;' * 3).join([
            #f'<font color="blue">{n_span_period}</font>',
            #f'<font color="purple">{n_span_today}</font>',
            f'<font color="purple">{n_span_today_all}</font>',
            ])))

        tl.append(('n_rev', ('&nbsp;' * 2).join([
            f'<font color="red">{n_rev_due_period}</font>',
            f'<font color="green">{n_rev_done_period}</font>',
            f'<font color="orange">{n_rev_done_period_dst}</font>',
            f'<font color="blue">{n_rev_done_today}</font>',
            f'<font color="purple">{n_rev_done_today_dst}</font>',
            ])))
        
        tl.append(('descr', f"<font color='blue'> {ellipsis(('&nbsp;' * 3).join(get_name_key(fact_id, cr)))} </font>"))
        
        last_grade = h['last_grade']
        s_last_at = h['s_last_at'] 
        n_at = h['n_at']
        tl.append(('n_hist', ('&nbsp;' * 3).join([f'<font color="red">#seen: {n_at}</font>', f'<font color="green">last: {s_last_at} [{last_grade}]</font>',]) if s_last_at else '<font color="red">debut</font>')) 
        self.update_stb(tl)

    def edited(self, d):
        c = d['cnd']
        log(c)
        if c != 'saved':
            return
        self.b.set_htm('Loading Edited Fact ...')
        QTimer.singleShot(1000, partial(setattr, self, 'busy', False))
    
    def update_stb(self, tl):
        for sct, s in tl:
            self.msg({'msg': s}, sct)
    
    def msg(self, d, sct='descr'):
        lbl = getattr(self, f'lbl_{sct}')
        msg = d.get('msg', '')
        to = d.get('to', 0)
        lbl.setText(msg)
        
        if to:
            QTimer.singleShot(to, partial(lbl.setText, ''))

    def reset(self, s=''):
        self.b.set_htm(s if s else htm('Query Due Review Items ...'))
        self.d, self.qas, self.gr, self.qa_span = {}, [], [], [] 
        self.slide = 0
        
        self.update_stb([('n_hist', ''), ('descr', ''), ('typ', ''),])

    def navigate(self, forward=True):
        i = self.slide
        if self.qas:
            self.slide += (1 if forward else -1)
            self.slide %= len(self.qas)
        else:
            self.slide = 0
        if self.slide != i:
            self.show_qa('a' if getattr(self, 'b_debut', False) else 'q')
                    
    def show_qa(self, st):
        qas = self.qas
        if qas:
            self.q_or_a = st
            self.b.set_htm(qas[self.slide][0 if st == 'q' else 1], b_raw=True)
            self.update_stb([('typ', f'<font color="red">[ {st.upper()} ] </font><font color="blue">&nbsp;#{self.slide + 1} of {len(qas)}</font>')])

    def grade(self, g, delay=3000):
        if getattr(self, 'b_busy_grade', False):
            print('busy_grading')
            return
        
        self.b_busy_grade = True
        def f():
            self.grade_(int(g))
            self.b_busy_grade = False

        if getattr(self, 'q_or_a', 'q') == 'a':
            f()
        else:
            self.show_qa('a')
            QTimer.singleShot(delay, f)

    def grade_(self, g):
        gr = self.gr
        qa_span = self.qa_span
        sl = self.slide
        stw1 = self.stw1
        if gr:
            gr[sl] = g
            qa_span[sl] = stw1.elapsed() / 10.

            if -1 in gr:
                self.navigate()
                stw1.reset()

            else:
                #self.play_audio('/home/cytu/usr/src/py/ananda/res/av/graded.mp3')
                self.sched(gr, qa_span)
                self.prepare()
    
    # XXX didn't use the full force of qa_span (detailed span info for each slide)
    def sched(self, gr, qa_span):
        cn = self.cn
        sched(self.d.get('rev_id', 0), gr, compute_sched(self.d.get('fact_id', 0), gr, cn.cursor()), int(self.stw.elapsed() / 10.), cn)

    def play_audio(self, src):
        a = self.av
        a.set_src(src)
        a.play()
    
    def cls(self):
        n = self.n()
        if not self.isFullScreen() and not self.isMaximized():
            sts.setValue(f'{n}/size', QVariant(self.size()))
        sts.setValue(f'{n}/state', QVariant(self.saveState()))     
        if self.par is None:
            shutil.rmtree(self.td)

    def timerEvent(self, e):
        if self.busy:
            return
        self.busy = True
        self.mgr.go()

    def closeEvent(self, e):
        self.cls()
        if self.par: 
            self.send(cnd='none')
        try:
            self.sc.shutdown(wait=False) 
        except:
            pass

        try:
            self.nb.close()
            vim_kill(self.nb_name)
        except:
            pass

    def event(self, e):
        try:
            typ = e.type()
            if typ == QEvent.WindowActivate:
                for i in self.lstw:
                    getattr(self, i).start() 
            
            elif typ == QEvent.WindowDeactivate:
                for i in self.lstw:
                    getattr(self, i).stop() 
        finally:
            return QMainWindow.event(self, e) 

if __name__ == '__main__':
    argv = sys.argv
    app = QApplication(argv)
    app.setApplicationName('rev')
    font = QFont('Microsoft JhengHei')
    font.setPointSize(12)
    app.setFont(font)

    argc = len(argv)
    ps = argparse.ArgumentParser(description='Ananda Reviewer')
    ps.add_argument('-n', '--names', nargs='+', dest='names')
    ps.add_argument('-d', '--database', dest='db_file')
 
    # XXX code for debugging
    if argc == 1:
        # use in test
        al = ['-n', 'evans', '-d', '/home/cytu/usr/src/py/ananda/db/ananda_temp.db'] 
    else:
        al = argv[1:] if argc else []
    w = win_rev(**ps.parse_args(al).__dict__)
    w.showMaximized()

    app.exec()
