from base import *
from db.make_db import make_db

def data(name):
    if is_lang(name):
        d = {'name': name, 'qa': {}, 'del': []} 
        if name == 'en_boatland':
            from ex.en_boatland import groups
            for g in groups():
                ex = g['ex']
                df = g['def']
                l = []
                a, b = [s.strip() for s in df.split(u'–')]
                #l.append({'q': ('-- ' + b.capitalize()), 'a': a})
                tt = [a]
                tt.extend(ex)
                l = [{'q': ('-- ' + b.capitalize()), 'a': '<br /><br />'.join(tt),}]
                d['qa'][a] = l
            keys = sorted(d['qa'].keys())
            return d, keys 
        
        elif name in ('de_grundwortschatz', 'de_grundwortschatz_pre'):
            from ex.de_grundwortschatz import groups
            i = 0
            for g in groups():
                ex = g['ex']
                df = g['def']
                # some words don't have examples.
                if not df:
                    continue
                i += 1
                l = []
                dfs = [s.strip() for s in df.split('\n')]
                w = dfs.pop()
                l.append({'q': w, 'a': '<br /><br />'.join(dfs)})
                if name == 'de_grundwortschatz':
                    for e in ex:
                        de, en = [s.strip() for s in e.split('\n')]
                        l.append({'q': en, 'a': de})
                d['qa'][str(i)] = l
            keys = sorted(d['qa'].keys(), key=lambda i:int(i))
            return d, keys 
    
    else:
        d = get_ana(name)
        src = d['src']
        qa = d['qa']
        z = d['z']
        zo = d['zo']
        sha = d['sha'] 
        r = cr.execute('select data from res where sha = ?', (sha,)).fetchone()
        if not r:
            cr.execute('insert into res (data, sha, meta) values (?, ?, ?)', 
                (sqlite3.Binary(open(src, 'rb').read()), sha, 
                json.dumps({'fn': os.path.basename(src), 'z': z, 'zo': zo})))
            #cn.commit()
        
        def mycmp(s):
            # sort by page and y
            q1 = qa['q'][s][0]
            return (q1[0], q1[1][1])
        
        keys = sorted(list((set(qa['q'].keys()) & set(qa['a'].keys())) - set(d.get('del', []))), key=mycmp)
        return d, keys 

def insert_prefab(name):
    d = data(name)
    if is_lang(name):
        save_ana(d[0])
    keys = list(map(json.dumps, d))[1]
    cr.execute('insert into prefab (name, keys) values (?, ?)', (name, keys))
    cn.commit()

def insert_prefab_read(name):
    d = data(name)
    cr.execute('insert into prefab (name, keys) values (?, ?)', (name, '[]'))
    cn.commit()

def merge():
    dd = {}
    for i in ['aliprantis', 'aliprantis_sol']:
        ks = data(i)[1]
        chapter0 = 0
        t = []
        b = False
        dd[i] = {}
        for k in ks:
            m = re.search(r'\d+\.\d+', k)
            if m is None:
                print('error in {k}: wrong key')
                b = True
                break

            else:
                chapter, nr = [int(s) for s in m.group().split('.')]
                if chapter0 > chapter: # error!
                    print(f'error in {k}: wrong chapter')
                    b = True
                    break

                elif chapter0 < chapter:
                    if t:
                        dd[i][str(chapter0)] = t
                        t = []
                    t.append(k)
                    nr0 = nr

                elif chapter0 == chapter:
                    t.append(k)
                
                chapter0 = chapter
                # check nr
                
                if nr0 > nr:
                    print(f'error in {k}: wrong nr')
                    break

                nr0 = nr
        if b:
            break
        
        # don't forget this!
        if t:
            dd[i][str(chapter0)] = t

        #cr.execute('insert into prefab (name, keys) values (?, ?)', (i, json.dumps(ks)))

    keys = []
    for i in range(1, 41):
        try:
            t = [(s, 'aliprantis') for s in dd['aliprantis'][str(i)]]
        except:
            continue
        try:
            t.extend([(s, 'aliprantis_sol') for s in dd['aliprantis_sol'][str(i)]])
        finally:
            keys.extend(t)
     
    cr.execute('insert into prefab (name, keys) values (?, ?)', ('aliprantis_real', json.dumps(keys)))
    cn.commit()

def fn(s):
    try:
        return json.loads(s)['fn']
    except:
        return ''

def update_res(name):
    d = get_ana(name)
    src = d['src']
    qa = d['qa']
    z = d['z']
    zo = d['zo']
    dd = open(src, 'rb').read()
    f = os.path.basename(src)
    cr.execute('update res set data = ?, sha = ?, meta = ? where id = (select id from res where fn(meta) = ?)', (sqlite3.Binary(dd), hashlib.sha224(dd).hexdigest(), json.dumps({'fn': f, 'z': z, 'zo': zo}), f))
    cn.commit()

def move_db():
    def mysorted(it):
        def mycmp(s):
            # sort by page and y
            q1 = d['qa']['q'][s][0]
            return (q1[0], q1[1][1])
        return sorted(list(it), key=mycmp)
    
    cn1 = sqlite3.connect(cat('db', 'ananda_abadir.db'))
    cr1 = cn1.cursor()
    cn1.create_function('meta_name', 1, meta_name)
    cn1.create_function('meta_key', 1, meta_key)

    name = 'abadir'
    d = get_ana(name)
    qa = d['qa']
    keys_in_db = set([r[0] for r in cr1.execute('select meta_key(data) from fact where meta_name(data) = ?', (name,)).fetchall()])
    keys = mysorted((set(qa['q'].keys()) & set(qa['a'].keys())) - set(d.get('del', [])) - keys_in_db)

    #cr.execute('insert into prefab (keys, name) values (?, ?)', (json.dumps(keys), name))
    #cn.commit()

def reconsolidate(name):
    cn1 = sqlite3.connect(cat('db', 'ananda.db'))
    cr1 = cn1.cursor()
    cn1.create_function('meta_name', 1, meta_name)
    cn1.create_function('meta_key', 1, meta_key)
    data = [r for r in cr1.execute('select id, data, meta_key(data) from fact where meta_name(data) = ?', (name,)).fetchall()]
    
    def mycmp(r):
        t = []
        dd = json.loads(r[1])
        try:
            qas = dd['qas']
            for qa in qas:
                for i in qa['q']:
                    if 'pg' in i and 'path' in i:
                        t.append((i['pg'], i['path'][1]))
            return sorted(t)[0]
        except:
            return dd['meta']['key']

    keys = sorted(data, key=mycmp)
     
    cr1.execute('delete from rev where at = "" and fact_id in (select id from fact where meta_name(data) = ?)', (name,))
    for ii, i in enumerate([k[0] for k in keys]):
        cr1.execute('insert into rev (fact_id, sched) values (?, ?)', (i, t_add(t_delta(seconds=ii), now())))
    cn1.commit()

if __name__ == '__main__':

    #reconsolidate('ash_real') 
    #sys.exit()

    new = True 
    #db = cat('db', 'ananda.db')
    db = cat('db', 'ananda_temp.db')
    if new:
        try:
            os.remove(db)
        except:
            pass

    cn = sqlite3.connect(db)
    if new:
        make_db(cn)
    cn.create_function('fn', 1, fn)
    cn.create_function('meta_name', 1, meta_name)
    cn.create_function('meta_key', 1, meta_key)
    cr = cn.cursor()

    for i in ('baldi2','aliprantis'):#, 'baldi1', 'medvegyev', 'fabian', 'knapp_basic_real', 'knapp_adv_real', 'milman', 'ambrosio', 'ash_complex', 'boyd', 'zastawniak', 'grimmett', 'brezis', 'evans_gariepy', 'bauschke', 'hoermander1', 'rudin_fa',):
        try:
            insert_prefab_read(i)
        except:
            print(f'{i} has been saved.')

    for i in ('evans', 'dreyfus'): #, 'abadir_stat', 'aliprantis_sol', 'dreyfus', 'kaczor1', 'kaczor2', 'kaczor3', 'boyd_sol', 'abramovich_sol', 'grimmett_sol'):
        try:
            insert_prefab(i)
        except:
            print(f'{i} has been saved.')
    cn.commit()

    #save_ana(data('de_grundwortschatz_pre')[0])
    #save_ana(data('de_grundwortschatz')[0])
