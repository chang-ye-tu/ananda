import os, sys, sqlite3, time, codecs
from functools import partial
from subprocess import Popen, call 
from pathlib import Path

os.chdir(os.path.dirname(__file__))
cat = os.path.join

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import QWebChannel

def htm(s, b_centered=False):
    return r'''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 
    'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<meta http-equiv='X-UA-Compatible' content='IE=EmulateIE7' >
<head>
    <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <script>
        var doc_finder;
        if (typeof qt != 'undefined') {
            new QWebChannel(qt.webChannelTransport, function (channel) {
                if (typeof channel.objects != 'undefined') {
                    doc_finder = channel.objects.doc_finder;
                }
            });
        }
    </script>
<style>
p {
  font-family: "Helvetica", "Noto Sans", serif, Times;
  font-size: 20px;
}

img {
  float:left;  
  margin-right: 5px;
}

a {
  font-weight: bold;
  text-decoration: none;
  color: blue;
}

.fsize {
  font-weight: bold;
  color: red;
}

.ctime {
  font-weight: bold;
  color: green;
}

.fpath {
  font-weight: bold;
}
</style>
</head>
<body>
%s
</body>
</html>
''' %  ('''<div id='outer'><div id='middle'><div id='inner'>
%s
</div></div></div>''' % s if b_centered else s)

def make_db(cn):
    cr = cn.cursor()

    def create_ix(t, i):
        cr.execute('create index ix_%s_%s on %s(%s)' % (t, i, t, i))

    for t in ['doc']:
        cr.execute('''create table %s (id integer primary key, 
                                       filename text not null,
                                       path text not null,
                                       created text not null,
                                       size text not null,
                                       unique (path))''' % t)
        for i in ['filename',]:
            create_ix(t, i)

    for t in ['history']:
        cr.execute('''create table %s (id integer primary key, 
                                       search text not null,
                          created text not null default current_timestamp)''' % t)
        for i in ['search', 'created']:
            create_ix(t, i)
    
    cn.commit()

def recreate_db():
    folders = ['/home/cytu/usr/',]
    doc_types = ['.pdf', '.djvu', '.ps', '.chm', '.epub']
    r = None
    try:
        # copy old history items if any
        cr = sqlite3.connect(db_doc).cursor()
        r = cr.execute('select search, created from history').fetchall()
        os.remove(db_doc)
    except:
        pass
    cn = sqlite3.connect(db_doc)
    make_db(cn)
    cr = cn.cursor()
    
    if r:
        cr.executemany('insert into history(search, created) values(?, ?)', r)

    for fd in folders:
        for root, dirs, files in os.walk(fd):
            for f in files:
                fn, dt = os.path.splitext(f)
                if dt in doc_types:
                    path = cat(root, f)
                    cr.execute('insert into doc(filename, path, created, size) values(?, ?, ?, ?)', (fn, path, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(path))), human_readable(os.path.getsize(path)),))
    cn.commit()

def human_readable(size):
    suffixes=['B', 'KB', 'MB', 'GB', 'TB']
    ind = 0
    while size > 1024.:
        ind += 1       
        size /= 1024. 
    return '%.2f %s' % (size, suffixes[ind])

def get_doc(fid, cr):
    r = cr.execute('select path, filename from doc where id = ?', (fid,)).fetchone()
    return r if r else ('', '')

def get_doc_num(cr):
    r = cr.execute('select count(*) from doc').fetchone()
    return r if r else 0

class browser(QWebEngineView):

    def __init__(self, par=None):
        super(browser, self).__init__(par)
        self.setContextMenuPolicy(Qt.NoContextMenu)

    def set_htm(self, h):
        #self.setHtml(h, QUrl.fromLocalFile(str(Path(__file__).resolve().parent)))
        fn = cat(Path(__file__).resolve().parent, 'tmp', 'doc_finder.htm')
        codecs.open(fn, 'w', 'utf-8').write(h)   
        self.load(QUrl.fromLocalFile(fn))

class search_js(QObject):

    def __init__(self, par):
        super(QObject, self).__init__()
        self.par = par 
    
    @pyqtSlot(str)
    def open_file(self, fid):
        self.par.open_file(fid)

class wdg_search(QWidget):

    def __init__(self, par=None):
        QWidget.__init__(self, par)
        self.vlo = QVBoxLayout(self)
        self.led = QLineEdit(self)
        self.browser = browser(self)
        self.vlo.addWidget(self.led)
        self.vlo.addWidget(self.browser)

class win(QMainWindow):
    
    change_stb = pyqtSignal(dict)

    def __init__(self, par=None):
        QMainWindow.__init__(self, par)
        
        self.setWindowTitle('Document Finder')
        self.setWindowIcon(QIcon('./res/img/filefind.png'))

        stb = self.statusBar()
        for ii, it in enumerate([('lbl_status',  1),
                                 ('lbl_all',     1), ]):
            n, l = it
            setattr(self, n, QLabel(self))
            w = getattr(self, n)
            #if n in ['lbl_status',]:
            w.setAlignment(Qt.AlignCenter)
            w.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
            stb.insertPermanentWidget(ii, w, l)
        stb.setSizeGripEnabled(False)
        
        self.cn = sqlite3.connect(db_doc)
        self.cr = self.cn.cursor()
        self.otype = 'filename'

        self.wdg = wdg_search()
        self.setCentralWidget(self.wdg)
        led = self.wdg.led
        self.completer = QCompleter()
        led.setCompleter(self.completer)

        b = self.wdg.browser
        #b.set_htm(htm(''))
        self.js = search_js(self)
        ch = QWebChannel(self)
        ch.registerObject('doc_finder', self.js)
        b.page().setWebChannel(ch)

        #led.textChanged.connect(self.search)
        led.returnPressed.connect(self.show_result)
        self.change_stb.connect(self.update_stb)

        self.mnu = mnu = QMenu(self)
         
        for i in (('open_doc',    'Open File',           '', False),
                  ('open_doc_unique','Open File: Unique','', False),
                  None,
                  ('open_parent', 'Open Parent Folder',  '', False),
                  None,
                  ('sort_fname',  'Sort by File Name',   '', False),
                  ('sort_path',   'Sort by Path',        '', False),
                  ('sort_ctime',  'Sort by Created Time','', False),
                  None,
                  ('rename_file', 'Rename File',         '', False),
                  ('copy_name',   'Copy File Name',      '', False),
                  ('pdftk',       'PDFtk File',          '', False),
                  None,
                  ('delete_file', 'Delete File',         '', False),
                  None,
                  ('recreate_db', 'Recreate Database',   '', False),
                 ):

            if i is None:
                mnu.addSeparator()
            else:
                n, t, sc, ck = i
                setattr(self, 'act_%s' % n, QAction(t, self))
                a = getattr(self, 'act_%s' % n)
                a.setCheckable(ck)
                a.triggered.connect(partial(self.handler_act, n))
                mnu.addAction(a)

        for i, k in [('focus',     ('Ctrl+K',)),
                     ('find_text', ('Ctrl+F',)),  
                     ('find_previous', ('Alt+Left',)),  
                     ('find_next', ('Alt+Right',)),
                    ]:
            s = 'act_%s' % i
            try:
                a = getattr(self, s)
            except:
                setattr(self, s, QAction(self))
            finally:
                a = getattr(self, s)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            a.triggered.connect(partial(self.handler_act, i))
            self.addAction(a)
            
        self.update_all_num()
        self.update_history()
        QTimer.singleShot(2, self.recover_last)
    
    def recover_last(self):
        r = self.cr.execute('select distinct search from history order by created desc limit 1').fetchone()
        if r is not None:
            txt = r[0]
            self.wdg.led.setText(txt)
            self.update_result(txt)

    def update_history(self):
        r = self.cr.execute('select distinct search from history order by created desc limit 1000').fetchall()
        if r:
            model = QStringListModel()
            model.setStringList([rr[0] for rr in r])
            self.completer.setModel(model)
        self.row = 0

    def update_all_num(self):
        self.send(sect='lbl_all', msg='<font color="blue"> number of docs: &nbsp;&nbsp;&nbsp;</font><font color="red">%s</font>' % get_doc_num(self.cr))

    def send(self, **d):
        self.change_stb.emit(d)
    
    @pyqtSlot(dict)
    def update_stb(self, d):
        getattr(self, d['sect']).setText(d['msg'])

    def open_file(self, fid):
        self.fid = fid
        self.mnu.exec_(QCursor.pos())
            
    #def search(self, txt):
    #    self.update_result(txt) 
    
    @pyqtSlot()
    def show_result(self):
        self.send(sect='lbl_status', msg='<font color="blue"> searching ...</font>')
        txt = self.wdg.led.text()
        QTimer.singleShot(1, partial(self.update_result, txt))
        try:
            self.cr.execute('insert into history (search) values (?)', (str(txt),))
            self.cn.commit()
            self.update_history()
        except:
            pass
        self.wdg.browser.setFocus()

    def update_result(self, txt):
        r = self.cr.execute('select * from doc where filename like ? order by ' + self.otype, (str(txt),)).fetchall()
        def s_htm(l):
            ftype = os.path.splitext(l[2])[1][1:].lower()
            return """<p><img src='/home/cytu/usr/src/py/ananda/res/img/{}_icon.png' width='56' height='56' /><a href='' onClick="doc_finder.open_file('{}'); return false;">{}</a><br /><span class='ctime'>{}</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class='fsize'>{}</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class='fpath'>{}</span><br /></p>""".format(ftype, l[0], l[1], l[3], l[4], l[2])
        b = self.wdg.browser
        hhh = htm(''.join([s_htm(rr) for rr in r]))
        b.set_htm(hhh)

        self.send(sect='lbl_status', msg='<font color="blue"> result count: &nbsp;&nbsp;&nbsp;</font><font color="red">%s</font>' % len(r))
        
    def handler_act(self, i):
        led = self.wdg.led
        txt = led.text()
        slist = self.completer.model().stringList()

        if i == 'focus':
            led.setFocus()
            led.selectAll()
        
        elif i == 'find_text':
            page = self.wdg.browser.page()
            page.findText(str(txt).replace('%', ''), QWebEnginePage.FindWrapsAroundDocument)

        elif i in ['find_previous', 'find_next']:
            led.setFocus()
            if len(slist):
                self.row += (1 if i == 'find_previous' else -1)
                self.row %= len(slist)
                led.setText(slist[self.row]) 

        elif i == 'sort_fname':
            self.otype = 'filename'
            self.update_result(txt) 

        elif i == 'sort_ctime':
            self.otype = 'created desc'
            self.update_result(txt) 

        elif i == 'sort_path':
            self.otype = 'path'
            self.update_result(txt) 

        elif i == 'recreate_db':
            recreate_db()
            self.cn = sqlite3.connect(db_doc)
            self.cr = self.cn.cursor()
            self.update_result(txt)
            self.update_all_num()

        else:
            try:
                path, fname = get_doc(self.fid, self.cr)
            except:
                return

            if i == 'open_doc':
                Popen(['xdg-open', path]) 
            
            elif i == 'open_doc_unique':
                Popen(['qpdfview', '--unique', path])

            elif i == 'open_parent':
                Popen(['xdg-open', os.path.dirname(path)])
            
            elif i == 'rename_file':
                fn, ok = QInputDialog.getText(self, 'Rename File', 'Original Name:\n  ' + fname, QLineEdit.Normal, fname)
                if ok:
                    path_ = cat(os.path.dirname(path), str(fn) + os.path.splitext(path)[1])
                    os.rename(path, path_)
                    self.cr.execute('update doc set filename = ?, path = ?, created = ? where id = ?', (str(fn), path_, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(path_))), self.fid))
                    self.cn.commit()
                    self.update_result(txt) 

            elif i == 'delete_file':
                if QMessageBox.question(self, 'Delete File', 'Really want to delete file \n' + fname + ' ?', QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
                    os.remove(path)
                    self.cr.execute('delete from doc where id = ?', (self.fid,))
                    self.cn.commit()
                    self.update_result(txt) 
                    self.update_all_num()

            elif i == 'copy_name':
                cb = app.clipboard()
                cb.clear(mode=cb.Clipboard)
                cb.setText(fname, mode=cb.Clipboard)
            
            elif i == 'pdftk':
                path_ = path + '______'
                # XXX what if the file is not a pdf?
                call(['pdftk', path, 'cat', '1-end', 'output', path_]) 
                os.renames(path_, path)
                self.cr.execute('update doc set created = ?, size = ? where id = ?', (time.localtime(os.path.getctime(path)), human_readable(os.path.getsize(path)), self.pid))
                self.cn.commit()
                self.update_result(txt)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName('doc_finder')
    app.setFont(QFont('Microsoft JhengHei'))

    db_doc = cat('db', 'doc.db')
    if not os.path.isfile(db_doc):
        recreate_db()

    w = win()
    w.showMaximized()
    app.exec_()
