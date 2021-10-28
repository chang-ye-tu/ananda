from base import *
from rev import win_rev
from db.make_db import make_db

from ex.mem import *
from ex.jp_kana import * 
from ex.ru_alphabets import alphabets as ru_abc 

drill_suite = { 
  'hiragana_kana_read': [(a, c + '<br />' + b) for a, b, c in hiragana],
  'katakana_kana_read': [(a, c + '<br />' + b) for a, b, c in katakana],
  'hiragana_read_kana': [(c, a + '<br />' + b) for a, b, c in hiragana],
  'katakana_read_kana': [(c, a + '<br />' + b) for a, b, c in katakana],
  'nr_action': nr_action,
  'nr_action_1': nr_action_1,
  '4_digits': d4,
  '4_digits_rvs': d4_,
  '4_digits_1': d41,
  '4_digits_rvs_1': d41_,
  'ru_alphabets': [(a, d + '<br />' + e) for a, b, c, d, e in ru_abc],
}

for i in range(100):
    nn = str(i).zfill(2)
    drill_suite['4_digits[%s]' % nn] = d4[100 * i : 100 * (i+1)]
    drill_suite['4_digits_rvs[%s]' % nn] = d4_[100 * i : 100 * (i+1)]

def update_loci(b_write=True): # XXX behave badly 08/27/14
    cn = sqlite3.connect(cat('db', 'loci.db'))
    cr = cn.cursor()
    r = cr.execute('select data from route').fetchall()
    dr = cat('ex', 'loci')
    if b_write:
        try:
            shutil.rmtree(dr)
        except:
            pass
        try:
            os.mkdir(dr)
        except:
            pass

    for rr in r:
        d = json.loads(rr[0])
        if b_write:
            for i in d['loci']:
                open(cat(dr, str(i) + '.png'), 'wb').write(cr.execute('select pix from loci where id = ?', (i,)).fetchone()[0])
        drill_suite['loci_' + d['name']] = [(str(ii + 1).zfill(3), img_s % cat(os.getcwd(), dr, str(i) + '.png')) for ii, i in enumerate(d['loci'])]

#update_loci(True)

def make_db_drill(cn):
    cr = cn.cursor()

    def create_ix(t, i):
        cr.execute('create index ix_%s_%s on %s(%s)' % (t, i, t, i))
    
    for t in ['result']:
        cr.execute('''create table %s (id integer primary key, 
                                       data text not null,
                          created text not null default current_timestamp
                                       )''' % t)
        for i in ['created']:
            create_ix(t, i)

    cn.commit()

db_drill = cat('db', 'drill.db') 
if not os.path.isfile(db_drill):
    make_db_drill(sqlite3.connect(db_drill))

def get_4digits_test():
    cn = sqlite3.connect(db_drill)
    cn.create_function('meta_name', 1, meta_name)
    
    tests = []
    for ss in ['4_digits', '4_digits_rvs']:
        r = [s[0] for s in cn.cursor().execute('select meta_name(data) from result where meta_name(data) like ?', (ss + '[%',)).fetchall()]
        p = re.compile(ss + r'\[(\d+)\]')
        ns = []
        for s in r:
            g = p.search(s)
            if g is not None:
                ns.append(g.groups()[0])
        n0 = set([str(i).zfill(2) for i in range(100)])
        df = n0 - set(ns)
        tests.append(ss + '[%s]' % (sorted(list(df))[0] if len(df) else '00'))
    return tests

def n_tested(cr, interval=None):
    try:
        count = 'select count(*) from result'
        sql = (count,) if interval is None else \
              (' '.join([count, 'where created between ? and ?']), interval)
        
        return cr.execute(*sql).fetchone()[0]
    except:
        return 0

def drill_set(n, qas, b_random=False):
    l = []
    qq = [(ii, i) for ii, i in enumerate(qas)]
    
    if b_random:
        shuffle(qq)
    
    for ii, (q, a) in qq:
        dd = {} 
        dd['q'] = [{'txt': q}]
        dd['a'] = [{'txt': a}]
        l.append(dd)
    
    return [q[0] for q in qq], json.dumps({'qas': l, 
                                           'meta': {'name': n, 'key': ''}})

class mgr(mgr_due):

    def __init__(self, par, db):
        super(mgr, self).__init__(par, db)

    def run(self):
        cn = sqlite3.connect(self.db)
        cn.create_function('meta_name', 1, meta_name)
        cn.create_function('meta_key', 1, meta_key)
        cr = cn.cursor()
        
        # check due rev
        r = due_rev(cr, b_prefab=False)
        if r:
            rev_id, fact_id = r[:2]
            self.send(cnd='rev', rev_id=rev_id, fact_id=fact_id, 
                      qas=self.fact_to_htm(fact_id, cr, b_math=False, b_hr=True, 
                                css='usr/src/py/ananda/res/ananda_noframe.css'))
        else:
            self.send(cnd='none')
            
class win_drill(win_rev):
     
    lstb = [('auto',   1, u''),
            ('descr',  8, u'q-a info'),
            ('typ',    6, u'q-a type | part'), 
            ('stw',    3, u'active time of this fact'),
            ('n_span', 3, u'logged active time: today'),
            ('n_hist', 6, u'history'),
            ('aux',    3, u'session status'),
            ]

    def __init__(self, names=None):
        super(win_drill, self).__init__()
        f = cat(self.td, 'drill.db')
        make_db(sqlite3.connect(f))
        self.setup_mgr(mgr(self, f))
        self.add_test(names)
        
        self.sc = sc = Scheduler()
        sc.add_listener(self.listen, EVENT_JOB_EXECUTED) 
        sc.start()
        
        self.dso = dso()

        for i, k in [('auto',  ('F3',)),
                     ('mark',  ('m',)),]:
            s = 'act_%s' % i
            setattr(self, s, QAction(self))
            a = getattr(self, s)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            
            f = partial(self.handler, {'cnd': i})
            a.triggered.connect(f)
            self.addAction(a)

        for f, s in [(self.callback, 'auto'),
                     (self.alarm, 'alarm'), 
                    ]:
            dbus.SessionBus().add_signal_receiver(f, dbus_interface=ifc,
                                                  signal_name=s)

    def update_auto(self):
        self.lbl_auto.setPixmap(QPixmap(':/res/img/1rightarrow.png' if self.b_auto else ''))

    def auto(self, b=True):
        sc = self.sc
        for j in sc.get_jobs():
            sc.unschedule_job(j)
        
        if b:
            self.add_callback()
        self.update_auto()

    def add_callback(self):
        sc = self.sc
        if self.q_or_a == 'q':
            n = 'show_answer'
            t = self.t_a
        else: 
            n = 'check'
            t = self.t_q 
        sc.add_date_job(self.dso.auto, 
                        str(t_add(t_delta(seconds=t), now(utc=False))), name=n)
    
    def callback(self):
        if self.q_or_a == 'q':
            self.show_qa('a')
        else:
            self.grade(3)

    def listen(self, e):
        if e.job.name in ('show_answer', 'check'):
            self.add_callback()

    def handler(self, d):
        c = d['cnd'] 
        if c == 'show_q':           
            self.show_qa('q')

        elif c == 'show_a':           
            self.show_qa('a')

        elif c == 'full':
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

        elif c.find('grade_') != -1:
            self.grade(c.split('_')[-1], delay=1000)
        
        elif c == 'auto':
            self.b_auto = not self.b_auto
            self.auto(self.b_auto)
        
        elif c == 'mark':
             n = getattr(self, 'test_id', -1)
             if n != -1:
                if n not in self.d_mark:
                    self.d_mark[n] = []
                self.d_mark[n].append(self.slide)

    def handler_mgr(self, d):
        c = d['cnd'] 
        if c == 'rev':
            if self.state == st_learn:
                self.rev(d)
                meta = self.d_meta[self.test_id]
                self.b_auto, self.t_q, self.t_a = meta['b_auto'], meta['t_q'], meta['t_a']
                self.auto(self.b_auto)

        elif c == 'none':
            self.test_id = -1
            cn = sqlite3.connect(db_drill)

            # display statistics and then extra turn(s) of failed/marked drills
            # save score, speed data for comparison
            marks = []

            for n in self.d_result:
                order = self.d_order[n]
                mark = self.d_mark.get(n, [])
                meta = self.d_meta[n]
                name = meta['name']
                if name == 'failed':
                    continue
                # use set(mark) to remove duplicates
                marks.extend([drill_suite[name][:][order[i]] for i in set(mark)])
                score, speed = self.d_result[n]
                nl = range(len(self.d_result[n]))
                score_orig = [score[order[i]] for i in nl]
                speed_orig = [speed[order[i]] for i in nl]
                
                dd = {'meta': meta, 
                      'speed': speed,
                      'score': score,
                      'order': order,
                      'mark': mark}
                
                cn.cursor().execute('insert into result (data) values (?)', 
                                    (json.dumps(dd),)) 
            cn.commit()

            if marks:
                drill_suite['failed'] = marks
                # Go over those marked again?
                self.add_test(['failed', '0', '1', '2', '2'])
                self.busy = False

            else:
                self.b.set_htm('All Done!')
            
    def rev(self, d):
        self.d = d
        self.qas = d['qas']
        self.gr = [-1] * len(self.qas)
        self.qa_span = [-1] * len(self.qas)
        self.slide = 0
        
        self.q_or_a = 'q'
        self.show_qa('q')
        for i in self.l_stw:
            getattr(self, i).reset()
         
        tl = [('descr', '<font color="blue"> %s </font>' % ellipsis(self.d_meta[self.test_id]['name']))]
        self.update_stb(tl)
    
    def sched(self, gr, qa_span):
        delete_fact(self.d['fact_id'], self.cn)
        self.d_result[self.test_id] = (gr, qa_span) 
        self.test_id += 1

    def add_test(self, names=None):
        if names is None:
            return
        tps = [names[5 * i : 5 * (i + 1)] for i in range(len(names) / 5)] 
        cn = self.cn
        self.b_auto, self.t_q, self.t_a = 0, 0, 0 
        self.d_result, self.d_order, self.d_mark, self.d_meta = {}, {}, {}, {}
        self.test_id = 0
        for i, (n, b_random, b_auto, t_q, t_a) in enumerate(tps):
            order, d = drill_set(n, drill_suite[n], b_random=int(b_random))
            self.d_order[i] = order
            self.d_meta[i] = {
                'name': n, 'b_random': int(b_random), 'b_auto': int(b_auto),
                't_q': int(t_q) , 't_a': int(t_a),}
            insert_new_fact(d, cn.cursor())
        cn.commit()

if __name__ == '__main__':
    DBusQtMainLoop(set_as_default=True) 
    argv = sys.argv
    app = QApplication(argv)
    app.setApplicationName('drill')
    app.setFont(QFont('Microsoft JhengHei'))

    argc = len(argv)
    ps = argparse.ArgumentParser(description='Ananda Driller')
    ps.add_argument('-n', '--names', nargs='+', dest='names')
    
    if argc in (0, 1): # use in test
        
        # XXX 5-tuple: n (test name), b_random (randomize?), b_auto (autoplay?), 
        #              t_q (question shown /secs), t_a (answer shown /secs)
        #al = ['-n', 
        #      'hiragana_read_kana', '0', '1', '1', '1', 
        #      'ru_alphabets',       '1', '1', '2', '2', 
        #      'katakana_read_kana', '0', '1', '3', '3',]
        
        t1, t2 = get_4digits_test()
        al = ['-n', 
              'nr_action_1', '0', '1', '3', '3', 
              'nr_action',   '1', '1', '3', '3',
              t1,            '0', '1', '6', '3', 
              t2,            '0', '1', '6', '3',]
              #t1,            '1', '1', '6', '3',
              #t2,            '1', '1', '6', '3',]
    else:
        al = argv[1:]
   
    w = win_drill(**ps.parse_args(al).__dict__)
    w.show()
    
    try:
        w.alarm(dbus.SessionBus().get_object(ifc, '/').state())
    except:
        pass 
    app.exec_()
