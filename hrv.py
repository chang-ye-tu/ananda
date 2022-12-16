from base import *
from op import *

from ui.win_hrv import Ui_win_hrv
from ui.dlg_tk import Ui_dlg_tk
from ui.dlg_op import Ui_dlg_op

mode_read, mode_anno = range(2)

from rev import win_rev

def promote(self, typ='tkd'):
    par = self.par()
    pg = str(par.pg())
    dlg = dlg_tk(par, self.tk)         
    if dlg.exec_():
        b = self.tk[0]
        cbo = dlg.cbo_tk
        k = str(cbo.itemData(cbo.currentIndex()).value())
        s = dlg.led_tk.text().strip()
        ke = dlg.led_key.text().strip()
        setattr(par, 'last_tk', k)
        tkd = par.dd[typ]
        if pg not in tkd:
            tkd[pg] = []
        tkd[pg].append([b, k, s, ke]) 
        self.tk = [b, k, s, ke]
        par.refresh()

def eligible_fact(d, pg, tp):
    qa = d['qa']
    q = qa['q']
    a = qa['a']
    # XXX convenient setting to specify randering range
    pg_range = d.get('pg_range', '-')
    ans, pg_range_all = parse_range(pg_range, tp)
    ks = []
    for k in q:
        # both q and a can span several pages;
        # last of q and first of a can be seperated several pages long.
        try:
            qq, aa = q[k], a[k]
        except:
            continue
        all_q_pgs = set([qi[0] for qi in qq])
        all_a_pgs = set([ai[0] for ai in aa])
        all_pgs = all_q_pgs | all_a_pgs
        if all_pgs <= set(pg_range_all) and sorted(list(all_pgs))[-1] <= int(pg):
            ks.append(k)
    
    # sort by pg and y
    def mycmp(k):
        q1 = q[k][0]
        return (q1[0], q1[1][1])
    return sorted(list((set(ks) & set(q.keys()) & set(a.keys())) - set(d.get('del', []))), key=mycmp)

def render_fact(self, itk):
    b, tk, s, ke = itk
    par = self.par()
    try:
        w = par.tw.currentWidget()
        if w is None:
            return
    except:
        w = par

    dd = w.dd
    d = w.d_fact
    
    if (w.pg(), b[1], tk, s, ke) in d:
        k = d[(w.pg(), b[1], tk, s, ke)]
        qa = dd['qa']
        if k in qa['q'] and k in qa['a']:
            ww = win_fact(par, dd['name'], k, w.td)
            ww.showMaximized()
        else:
            print('not complete')
    else:
        print('not found')

class rubber(QGraphicsObject):

    def __init__(self, rct):
        super(rubber, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable)
        self.setAcceptHoverEvents(True)
        self.rct = rct
        self.setFocus()
        self.reset()    
    
    def boundingRect(self):
        return self.rct.normalized().adjusted(-1, -1, 1, 1)

    def par(self):
        return self.scene().views()[0]

    def paint(self, p, opt, w):
        pen = QPen(Qt.DashLine)
        pen.setColor(QColor('blue'))
        p.setPen(pen)
        p.drawRect(self.boundingRect())

        c_hd = QColor(0, 0, 0, 40)
        c_hd.setAlpha(40)
        p.setBrush(c_hd)
        for hd in self.hds():
            p.drawRect(hd)

    def reset(self):
        self.sz_hd = 10
        
        self.hd_tl = QRectF(0, 0, self.sz_hd, self.sz_hd)
        self.hd_tr = QRectF(0, 0, self.sz_hd, self.sz_hd)
        self.hd_bl = QRectF(0, 0, self.sz_hd, self.sz_hd)
        self.hd_br = QRectF(0, 0, self.sz_hd, self.sz_hd)
        self.hd_l =  QRectF(0, 0, self.sz_hd, self.sz_hd)
        self.hd_t =  QRectF(0, 0, self.sz_hd, self.sz_hd)
        self.hd_r =  QRectF(0, 0, self.sz_hd, self.sz_hd)
        self.hd_b =  QRectF(0, 0, self.sz_hd, self.sz_hd)
        
        self.on = False
        self.update_hds()
        self.update()

    def hds(self): 
        return [self.hd_tl, self.hd_tr, self.hd_bl, self.hd_br, self.hd_l,  self.hd_t,  self.hd_r,  self.hd_b]

    def update_hds(self):
        r = self.boundingRect()

        self.hd_tl.moveTopLeft(r.topLeft())
        self.hd_tr.moveTopRight(r.topRight())
        self.hd_bl.moveBottomLeft(r.bottomLeft())
        self.hd_br.moveBottomRight(r.bottomRight())

        s2 = self.sz_hd / 2
        self.hd_l.moveTopLeft(QPointF(r.x(), r.y() + r.height() / 2 - s2))
        self.hd_t.moveTopLeft(QPointF(r.x() + r.width() / 2 - s2, r.y()))
        self.hd_r.moveTopRight(QPointF(r.right(), r.y() + r.height() / 2 - s2))
        self.hd_b.moveBottomLeft(QPointF(r.x() + r.width() / 2 - s2, r.bottom()))

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:    
            if self.contains(e.pos()):
                self.setSelected(True)
            self.setCursor(Qt.ClosedHandCursor)
            self.p_drag_i = e.pos()
            self.rct_i = copy.copy(self.rct)
            self.update()

    def mouseReleaseEvent(self, e):
        #if self.hd_over is None and self.contains(e.pos()):
        #    self.setCursor(Qt.OpenHandCursor)
        #else:
        self.setCursor(Qt.ArrowCursor)
        self.update()
        self.on = False

    def mouseMoveEvent(self, e):
        if not self.on:
            self.on = True
            self.state = []

            found = False
            for hd in self.hds():            
                if hd.contains(e.pos()):
                    self.hd_over = hd
                    found = True
                    break              

            if found: 
                hd = self.hd_over
                if hd in [self.hd_tl, self.hd_br]:
                    self.setCursor(Qt.SizeFDiagCursor)

                if hd in [self.hd_tr, self.hd_bl]:
                    self.setCursor(Qt.SizeBDiagCursor)

                if hd in [self.hd_l, self.hd_r]:
                    self.setCursor(Qt.SizeHorCursor)
                    
                if hd in [self.hd_t, self.hd_b]:
                    self.setCursor(Qt.SizeVerCursor)            
                
                r = copy.copy(self.rct_i) 
                offset = e.pos() - self.p_drag_i
                
                if hd in [self.hd_t, self.hd_tl, self.hd_tr]:
                    self.state.append('top')
                    r.setTop(r.top() + offset.y())

                if hd in [self.hd_l, self.hd_tl, self.hd_bl]:
                    self.state.append('left')
                    r.setLeft(r.left() + offset.x())

                if hd in [self.hd_b, self.hd_bl, self.hd_br]:
                    self.state.append('bottom')
                    r.setBottom(r.bottom() + offset.y())                

                if hd in [self.hd_r, self.hd_tr, self.hd_br]:
                    self.state.append('right')
                    r.setRight(r.right() + offset.x())

                r = r.normalized()
                if r.width() > 2 * self.sz_hd and r.height() > 2 * self.sz_hd: 
                    self.prepareGeometryChange()
                    self.rct = r
            
            else:
                self.state.append('move')
                s = self.rct_i.normalized()
                p = s.topLeft() + e.pos() - self.p_drag_i
                self.prepareGeometryChange()
                self.rct.moveTo(p)
        
        else:

            st = self.state
            if 'move' in st:
                s = self.rct_i.normalized()
                p = s.topLeft() + e.pos() - self.p_drag_i
                self.prepareGeometryChange()
                self.rct.moveTo(p)

            else:
                r = copy.copy(self.rct_i) 
                offset = e.pos() - self.p_drag_i
                if 'top' in st:
                    r.setTop(r.top() + offset.y())

                if 'left' in st:
                    r.setLeft(r.left() + offset.x())

                if 'bottom' in st:
                    r.setBottom(r.bottom() + offset.y())                

                if 'right' in st:
                    r.setRight(r.right() + offset.x())

                r = r.normalized()
                if r.width() > 2 * self.sz_hd and r.height() > 2 * self.sz_hd: 
                    self.prepareGeometryChange()
                    self.rct = r

        self.update()
        self.update_hds()

    def keyPressEvent(self, e):
        k = e.key()
        if k == Qt.Key_Escape or k == Qt.Key_Delete:
            self.par().refresh()

        elif k == Qt.Key_Enter or k == Qt.Key_Return:
            # self.grab_rect()
            print('grab') 

        else:
            QGraphicsObject.keyPressEvent(self, e)

    def itemChange(self, change, v):
        if change != QGraphicsObject.ItemSelectedChange:
            return QGraphicsObject.itemChange(self, change, v)

class line(QGraphicsItem):
    
    def __init__(self, o, n=0):
        super(line, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable)

        attrs_from_dict(locals())
        self.setFocus()
        self.setPos(o)
        self.w = 800

    def par(self):
        return self.scene().views()[0]

    def paint(self, pt, opt, w):
        p = QPen(Qt.DotLine)
        p.setWidth(4)
        p.setColor(QColor('red' if opt.state & QStyle.State_Selected else 'purple'))
        pt.setPen(p)
        w = self.w
        pt.drawLine(QLineF(QPointF(-w, 0), QPointF(w, 0)))
    
    def boundingRect(self):
        h, w = 25, self.w
        return QRectF(QPointF(-w, 0), QPointF(w, 0)).adjusted(-h, -h, h, h)
    
    def mouseReleaseEvent(self, e):
        par = self.par()
        pg = str(par.pg())
        y = par.mm.inverted()[0].map(self.pos()).y()
        yd = par.dd['yd']
        y1, y2 = yd[pg]
        yd[pg] = ((y1, y) if y >= y1 else (y, y1)) if self.n else ((y, y2) if y2 >= y else (y2, y))   
        QGraphicsItem.mouseReleaseEvent(self, e) 
        #p_cur = self.mapToParent(e.pos())

    #def mouseMoveEvent(self, e):
    #    #self.pos()
    #    if p_cur.y() >= self.parent().height():
    #        self.send(cnd='scroll', bar='v', tick=1)
    #        
    #    elif p_cur.y() <= 0:
    #        self.send(cnd='scroll', bar='v', tick=-1)
    #    
    #    if p_cur.x() >= self.parent().width():
    #        self.send(cnd='scroll', bar='h', tick=1)
    # 
    #    elif p_cur.x() <= 0:
    #        self.send(cnd='scroll', bar='h', tick=-1)
    #
    #    QGraphicsItem.mouseMoveEvent(self, e)

class sep(QGraphicsItem):

    def __init__(self, o, tk):
        super(sep, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable)

        attrs_from_dict(locals())
        self.setFocus()
        self.setPos(o)
        self.w = 1000

    def par(self):
        return self.scene().views()[0]

    def paint(self, pt, opt, w):
        p = QPen(Qt.DotLine)
        p.setWidth(2)
        p.setColor(QColor('red' if opt.state & QStyle.State_Selected else 'green'))
        pt.setPen(p)
        w = self.w
        pt.drawLine(QLineF(QPointF(-w, 0), QPointF(w, 0)))
        pt.drawLine(QLineF(QPointF(0, 10), QPointF(0, -10)))
                
    def boundingRect(self):
        h, w = 25, self.w
        return QRectF(QPointF(-w, 0), QPointF(w, 0)).adjusted(-h, -h, h, h)
    
    def mouseReleaseEvent(self, e):
        par = self.par()
        pg = str(par.pg())
        p = par.mm.inverted()[0].map(self.pos())
        tkd = par.dd['tkd_man']
        tkd[pg].remove(self.tk)
        
        ymin, ymax = 0, sys.maxsize
        try:
            bx = sorted(par.dd['bxd'][pg], key=lambda b: b[1])
            ymin, ymax = bx[0][1], bx[-1][1] + bx[-1][-1]
        except:
            pass
        y = p.y()
        if y < ymin:
            y = ymin
        elif y > ymax:
            y = ymax
            
        self.tk = [[p.x(), y, 1000, 0], 'sep', '', '']
        tkd[pg].append(self.tk)

        QGraphicsItem.mouseReleaseEvent(self, e) 
        par.refresh()

    def contextMenuEvent(self, e):
        m = QMenu(self.par())
        l = [('&Remove', 'remove'), ('&Promote', 'promote')]  
        for ll in l:
            if ll is None:
                m.addSeparator()
            else:
                s, f = ll
                m.addAction(s, getattr(self, f))
        m.exec_(e.screenPos())
    
    def remove(self, b_refresh=True):
        par = self.par()
        pg = str(par.pg())
        par.dd['tkd_man'][pg].remove(self.tk)
        if b_refresh:
            par.refresh()
    
    def promote(self):
        self.remove(b_refresh=False)
        promote(self, 'tkd_man')
            
class box_sym(QGraphicsItem):

    def __init__(self, o, rct, b):
        super(box_sym, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        attrs_from_dict(locals())
        self.setFocus()
        self.setPos(o)

    def boundingRect(self):
        return self.rct.adjusted(-1, -1, 1, 1)

    def paint(self, pt, opt, w):
        p = QPen(Qt.DashLine)
        p.setWidth(1)
        p.setColor(QColor('red' if opt.state & QStyle.State_Selected else 'purple'))
        pt.setPen(p)
        pt.drawRect(self.boundingRect())

    def par(self):
        return self.scene().views()[0]

    def contextMenuEvent(self, e):
        m = QMenu(self.par())
        l = [('&Select this', 'select'), 
             None, ('&Erase', 'erase'),] 

        for ll in l:
            if ll is None:
                m.addSeparator()
            else:
                s, f = ll
                m.addAction(s, getattr(self, f))

        m.exec_(e.screenPos())
    
    def select(self):
        self.par().save_sym(self.b)
           
    def erase(self):
        self.par().erase(self.b)
    
class box(QGraphicsItem):

    def __init__(self, o, rct, tk):
        super(box, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        attrs_from_dict(locals())
        self.setFocus()
        self.setPos(o)

    def boundingRect(self):
        return self.rct.adjusted(-1, -1, 1, 1)

    def paint(self, pt, opt, w):
        r = self.boundingRect()
        p = QPen(Qt.DashLine)
        p.setWidth(2)
        c = 'blue' if self.tk[1] else 'gold'
        p.setColor(QColor('red' if opt.state & QStyle.State_Selected else c))
        pt.setPen(p)
        pt.drawRect(r)

    def par(self):
        return self.scene().views()[0]

    def contextMenuEvent(self, e):
        m = QMenu(self.par())
        
        if self.tk[1]:
            l = [('&Demote', 'demote',), ('&Edit', 'edit'),]  
        else:
            l = [('&Promote', 'promote'), ]
        l.extend([None, ('&Re-ocr', 'reocr'), 
                  None, ('&Erase',  'erase'),
                  None, ('&Try to Render', 'render'),
                  None, ('&Measurements', 'measure'),])
        for ll in l:
            if ll is None:
                m.addSeparator()
            else:
                s, f = ll
                m.addAction(s, getattr(self, f))

        m.exec_(e.screenPos())
    
    def demote(self):
        par = self.par()
        pg = str(par.pg())
        try:
            b = self.tk[0]
            par.dd['tkd'][pg].remove(self.tk)
            self.tk = [b, '', '', '']
            par.refresh()

        except:
            print('error demoting')

    def promote(self):
        promote(self)

    def edit(self):
        par = self.par()
        pg = str(par.pg())
        dlg = dlg_tk(par, self.tk)
        if dlg.exec_():
            b = self.tk[0]
            cbo = dlg.cbo_tk
            tkd = par.dd['tkd']
            try:
                tkd[pg].remove(self.tk)

            except:
                print('error editing')
                return

            tk = str(cbo.itemData(cbo.currentIndex()).value())
            s = dlg.led_tk.text().strip()
            ke = dlg.led_key.text().strip()
            self.tk = [b, tk, s, ke]
            tkd[pg].append(self.tk) 
            par.refresh()
            setattr(par, 'last_tk', tk)
    
    def render(self):
        render_fact(self, self.tk)

    def erase(self):
        self.par().erase(md.mapRect(QRect(*self.tk[0]))) 
    
    def measure(self):
        par = self.par()
        pg = str(par.pg())
        bx = par.dd['bxd'][pg]
        gaps = get_gap(bx)
        l = [b - a for a, b in gaps]
        thr = 1.8 * (sum(l) / len(l) if l else 0)
        x, y, w, h = span(bx)
        xx, yy, ww, hh = self.tk[0]
        QMessageBox.information(par, 'Measurements', '\n'.join([
            '[item] x: %s  y: %s  w: %s  h: %s' % (xx, yy, ww, hh), 
            '[span] x: %s  y: %s  w: %s  h: %s' % (x, y, w, h), 
            '[ratio] indent: (%.4f, %.4f)' % (1.*(xx-x)/w, 1.*(x+w-xx-ww)/w),
            '            top: (%.4f, %.4f)' % (1.*(yy-y)/h, 1.*(h+y-hh-yy)/h),     
            '            width: %.4f' % (1.*ww/w),
            '            height: %.4f' % (1.*hh/h),
            '            thr: %.4f' % thr,
            ]))
        
    def reocr(self):
        par = self.par()
        td = par.td
        dd = par.dd
        book = bk(dd['name'])
        dc = book.doc()
        dc.set_z(dd['zo'])
        i = dc.render(par.pg())
        f_i = cat(td, 'reocr.tif')
        corr = get_corr(i, td, book, book.nn_corr)
        r = md.mapRect(QRect(*self.tk[0]))
        rc = md.mapRect(QRect(*corr))
        rw, rh = rc.width(), rc.height()
        r.adjust(-rw, -rh, rw, rh)
        i.copy(r).convertToFormat(QImage.Format_Indexed8).save(f_i)
        f_w = cat(td, 'reocr')
        f_w_t = f_w + '.txt'
        # tesseract may fail
        if ocr(f_i, f_w):
            QMessageBox.information(par, 'Ocr Reads ...', get_s(f_w_t))
            print(get_s(f_w_t)) 
        else:
            print('reocr error')

class dlg_tk(QDialog, Ui_dlg_tk):

    def __init__(self, par=None, tk=None):
        QDialog.__init__(self, par)
        self.setupUi(self)        
        attrs_from_dict(locals())
        self.cbo_tk.currentIndexChanged.connect(self.reset) 
        self.book = book = par.book
        for bt in self.btb.buttons():
            if bt.text() == '&Ok':
                bt.setDefault(True)

        cbo = self.cbo_tk
        for k in sorted(book.tokens.keys()):
            cbo.addItem(k, QVariant(k))
        
        b, k, s, ke = tk
        self.led_tk.setText(s)
        self.led_key.setText(ke)
        
        last_tk = getattr(par, 'last_tk', '')
        if k or last_tk:
            k = k if k else last_tk
            cbo.setCurrentIndex(cbo.findData(QVariant(k))) 
        else:
            cbo.setCurrentIndex(0)
            k = str(cbo.itemData(0).value())
        
        self.set_ocr(k)

    def set_ocr(self, k):
        tk = self.book.tokens[k]
        s = tk['ocr'] if 'ocr' in tk else 'none'
        self.lbl_ocr.setText('<font color="blue">ocr regex pattern: </font><font color="red"> %s</font>' % (s if s else 'none'))
    
    def reset(self, i):
        self.set_ocr(str(self.cbo_tk.itemData(i).value()))

class dlg_op(QDialog, Ui_dlg_op):
    
    l = ['tkd', 'yd', 'bxd', 'sep', 'man']

    def __init__(self, par=None):
        QDialog.__init__(self, par)
        self.setupUi(self)        
        pg = str(par.pg() + 1)
        book = par.book
            
        tp = (1, par.pgs())
        def f(n):
            return confine(n, tp)

        pgs = getattr(book, 'pgs')
        try:
            self.tp = tuple(map(f, (min(pgs) + 1, max(pgs) + 1)))
        except:
            self.tp = tp 

        for i in self.l:
            w = getattr(self, 'chk_%s' % i)
            n = sts.value('%s/chk_%s/check_state' % (self.n(), i), type=int)
            w.setCheckState(n)
            w.stateChanged.connect(self.blank)
            
            w = getattr(self, 'led_%s' % i)
            w.setText(pg)
            w.setEnabled(n == Qt.Checked)
        
        lm = self.led_bxd_morph
        lm.setEnabled(self.chk_bxd.checkState() == Qt.Checked)
        lm.setText(book.morph0)
        
        self.led_sep.textChanged.connect(self.sync_text)

    def sync_text(self, s):
        self.led_man.setText(s)

    def blank(self, i):
        for s in dir(self):
            if s.find('led_%s' % self.sender().objectName().split('_')[-1]) != -1:
                getattr(self, s).setEnabled(i == Qt.Checked)

    def accept(self):
        for i in self.l:
            if getattr(self, 'chk_%s' % i).checkState() == Qt.Checked:
                led = getattr(self, 'led_%s' % i)
                b, r = parse_range(led.text(), self.tp)
                setattr(self, 'pgl_%s' % i, r)
                if i == 'bxd':
                    setattr(self, 'morph', getattr(self, 'led_bxd_morph').text())
                if not b:
                    QMessageBox.warning(self, 'Error', 'Range specification in %s is wrong. Please correct it.' % i)
                    led.selectAll()
                    led.setFocus()
                    return  

        n = self.n()
        for i in self.l:
            sts.setValue('%s/chk_%s/check_state' % (n, i), QVariant(getattr(self, 'chk_%s' % i).checkState()))
        QDialog.accept(self)
    
    def n(self):
        return self.__class__.__name__

class cmd_view(QUndoCommand):
    
    def __init__(self, w, s_i, s_f, dsc):
        super(cmd_view, self).__init__(dsc)
        attrs_from_dict(locals())

    def redo(self):
        self.w.set_s(self.s_f) 

    def undo(self):
        self.w.set_s(self.s_i)

class opr(thread):
    
    def __init__(self, par):
        super(opr, self).__init__(par)

    def run(self):
        self.send(cnd='op_starts')
        par = self.parent()

        d = self.d
        dd = par.dd
        td = par.td
        
        book = bk(dd['name'])    
        dc = book.doc()
        dc.set_z(zo)

        pgl_tkd, pgl_bxd, pgl_yd, pgl_sep, pgl_man = [], [], [], [], []
        morph = ''
        
        # note that all pgl's are off-by-one.
        if d['bxd']:
            pgl_bxd = [i - 1 for i in d['bxd']['pgl']]
            morph = d['bxd']['morph'] 

        if d['yd']:
            pgl_yd = [i - 1 for i in d['yd']['pgl']] 
                
        if d['tkd']:
            pgl_tkd = [i - 1 for i in d['tkd']['pgl']]

        if d['sep']:
            pgl_sep = [i - 1 for i in d['sep']['pgl']]
        
        if d['man']:
            pgl_man = [i - 1 for i in d['man']['pgl']]

        tic = dt_now()
        
        def log(msg):
            self.send(cnd='msg', msg=msg)

        def msg_dsp(ii, n_pg, n, task=''):
            log(u'[ %s ]  processing page %-4d (%-4d of %4d: %3d %%) ... time elapsed:  %s' % (task, n_pg, ii + 1, n, int((ii + 1) * 100. / n), lapse(dt_now() - tic)))

        pgl_all = pgl_bxd + pgl_yd + pgl_tkd + pgl_sep
        n_bxd = len(pgl_bxd)
        n_yd = len(pgl_yd)
        n_tkd = len(pgl_tkd)
        n_sep = len(pgl_sep)
        n_all = len(pgl_all)

        # the order is important
        if d['man']:
            for n_pg in pgl_man:
                try:
                    dd['tkd_man'].update({str(n_pg): []})
                except:
                    log('man error: n_pg %s' % n_pg)

        if d['bxd']:
            for ii, n_pg in enumerate(pgl_bxd):
                msg_dsp(ii, n_pg, n_all, 'generate bxd')
                try:
                    bx = get_bx(dc.render(n_pg), td, book, morph)
                    if bx: 
                        dd['bxd'].update({str(n_pg): bx})
                        # delete yd and tkd
                        dd['yd'].update({str(n_pg): [0, sys.maxsize]})            
                        dd['tkd'].update({str(n_pg): []})  
                except:
                    log('bxd error: n_pg %s' % n_pg)
        
        if d['yd']:
            for ii, n_pg in enumerate(pgl_yd):
                msg_dsp(ii + n_bxd, n_pg, n_all, 'generate yd')
                try:
                    y = get_y(book, dd['bxd'][str(n_pg)])
                    if y:
                        dd['yd'].update({str(n_pg): y})
                except:
                    log('yd error: n_pg %s' % n_pg)
        
        corr = [] 
        if d['tkd']:
            for ii, n_pg in enumerate(pgl_tkd):
                msg_dsp(ii + n_bxd + n_yd, n_pg, n_all, 'generate tkd')
                try:
                    i = dc.render(n_pg)
                    if not corr:
                        corr = get_corr(i, td, book, book.nn_corr)
                    tk = get_tk(i, td, book, dd['bxd'][str(n_pg)], n_pg, corr)
                    if tk:
                        dd['tkd'].update({str(n_pg): tk})
                except:
                    log('tkd error: n_pg %s' % n_pg)

        tkd = dd['tkd_man']

        fs = []
        try:
            for ii, sym in enumerate(dd['sym']['tome']):
                f = cat(td, 'sym_%s.tif' % ii)
                open(f, 'wb').write(bin_loads(sym))
                fs.append(f)
        except:
            pass
        
        for ii, n_pg in enumerate(pgl_sep):
            msg_dsp(ii + n_bxd + n_yd + n_tkd, n_pg, n_all, 'generate tkd_man')
            
            try:
                bx = dd['bxd'][str(n_pg)]
                fi = cat(td, 'orig.tif')
                dc.render(n_pg).save(fi)
                gaps = get_gap(bx)
                x, y, w, h = span(bx)
                
                def search_before(y_):
                    l = sorted([yy for xx, yy, ww, hh in bx if (yy + hh <= y_)])
                    return l[-1] if l else y_

                yys = []
                for f in fs:    
                    sep_sym = get_sep_sym(bx, fi, f, 75)
                    for yyy in sep_sym:
                        yys.append(yyy)
                    
                    if getattr(book, 'b_sep_sym_before', False):
                        hhh = span(boxes(f, 'c150.150'))[-1]
                        for yyy in sep_sym:
                            yys.append(search_before(yyy-hhh))
                
                if getattr(book, 'b_sep_heu', False):
                    yys.extend(get_sep_heu(book, bx, gaps, y))

                # regularize seps: delete duplicates
                ys = []
                dys = {}
                for yy in yys:
                    i = bisect.bisect([g[0] for g in gaps], yy)
                    # test duplicity
                    if i in dys:
                        dys[i].append(yy)
                        continue
                    else:
                        dys[i] = [yy]
                    
                    ys.append(y + h if i == len(gaps) else sum(gaps[i]) / 2)
                
                if ys:
                    if str(n_pg) not in tkd:
                        tkd[str(n_pg)] = []
                    tkd[str(n_pg)].extend([[[x + w / 2, yy, 1000, 0], 'sep', '', ''] for yy in ys])

            except:
                log('sep error: n_pg %s' % n_pg)
        
        book.post(dd)
        dd = json.loads(json.dumps(dd))
        self.send(cnd='op_ends')

class mgr(thread):
    
    def __init__(self, par, db, names=None):
        super(mgr, self).__init__(par)
        self.db = db
        self.names = names

    def run(self):
        cn = sqlite3.connect(self.db)
        cr = cn.cursor()
        cn.create_function('meta_name', 1, meta_name)
        cn.create_function('meta_key', 1, meta_key)
        
        # check due rev
        r = due_rev(cr, names=self.names)
        if r:
            self.send(cnd='rev')

        else:
            # check if name in self.names is in prefab
            l = []
            for n in self.names:
                r = cr.execute('select * from prefab where name = ?', (n,)).fetchone()
                if r:
                    l.append(n)
            if not l:
                self.send(cnd='none')
                return
            
            name = choice(l)
            b, fa = prefab_fact(name, cn)
            if not b:
                self.send(cnd='none')
                return
            insert_new_fact(fa, cr)
            cn.commit()
            self.send(cnd='rev')

class view(QGraphicsView):
    
    msg_view = pyqtSignal(dict)

    def __init__(self, par=None, dd=None, db_file=None):
        super(view, self).__init__(par)
        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        attrs_from_dict(locals())
        self.td = tempfile.mkdtemp(prefix='%s_%s_' % (self.n(), now().replace(':', '').replace(' ', '_')), dir=cat(os.getcwd(), tmp))

        self.scn = QGraphicsScene(self)
        self.setScene(self.scn)

        for i in [self.horizontalScrollBar(), self.verticalScrollBar()]:
            i.actionTriggered.connect(self.before)
            i.valueChanged.connect(self.after)
       
        self.verticalScrollBar().valueChanged.connect(self.turn)

        self.hst = QUndoStack(self)
        
        self.book = bk(dd['name'])
        self.doc = dc = self.book.doc()
        if dd['sha'] != dc.sha:
            print("dd['sha'] != dc.sha !!!")
        dc.msg_doc.connect(self.handler_doc)
        
        self.opr = o = opr(self)
        o.msg_thread.connect(self.handler_opr)
        
        self.set_mode(mode_anno)
        self.update_pg_fact(b_update_qa=False)

        # vim netbean interfaces
        self.nb = nb()
        self.nb_port = 32190
        self.nb_name = 'hrv'
        self.nb.listen(QHostAddress('127.0.0.1'), self.nb_port)
        self.nb.msg_vim.connect(self.handler_vim)
        
    def send(self, **d):
        self.msg_view.emit(d)
    
    def n(self):
        return self.__class__.__name__
    
    def handler_vim(self, d):
        c = d['cnd'] 
        nn = self.nb_name
        if c == 'key':
            k = d['keycode']            
            if k == 'F2':
                if 'note' not in self.dd:
                    self.dd['note'] = {}
                self.dd['note'][str(self.pg_vim)] = vim_get(nn)
                # XXX 09/02/15 drastic measure
                self.save(b_display=False)
                vim_kill(nn)

            elif k == 'F11':
                if getattr(self, 'w_prv', None) is None:
                    self.w_prv = win_b(self, nb_name=nn) 
                self.w_prv.set_htm(htm(vim_get(nn), css='usr/src/py/ananda/res/ananda_prv.css', b_math=True))
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
        sh(200, ff(vim_mv, nn))
        sh(700, ff(vim_nb, nn, port))

        ks = ['F2', 'F11', 'F12']         
        t = ['set ft=tex bt=nofile bh=unload noswf']
        t.extend([r'imap <%s> <c-\><c-n><%s>a' % (k, k) for k in ks])
        
        sh(2000, ff(self.nb.send, '1:create!1\n' + ''.join(['1:specialKeys!%s "%s"\n' % (i + 2, k) for i, k in enumerate(ks)])))        
        sh(3000, ff(vim_buf, nn, self.td, '\n'.join(t)))
        sh(4000, ff(vim_set, nn, content, True))

    def turn(self, v):
        if self.mode == mode_anno:
            return

        def getm():
            try:
                sp = span(self.dd['bxd'][str(self.pg())])
                x, y, w, h = sp
                r = self.mm.mapRect(QRectF(*sp))
                rx, ry, rw, rh = r.x(), r.y(), r.width(), r.height()
                vs = self.verticalScrollBar()
                return True, (rh, ry, vs.pageStep())
            
            except:
                return False, (0, 0, 0)
        
        b, (rh, ry, step) = getm()
        if b:
            if v >= (rh + ry - step + 40): 
                self.doc.next()

            elif v < (ry - 40):
                self.doc.prev()
                b, (rh, ry, step) = getm()
                if b:
                    QTimer.singleShot(0, partial(self.set_v, rh + ry - step + 20))
                
    def prefab(self):
        pg_ = self.pg() - 1 if self.pg() else 0
        
        cn = sqlite3.connect(self.db_file)
        cn.create_function('meta_name', 1, meta_name)
        cn.create_function('meta_key', 1, meta_key)
        cr = cn.cursor() 
        # XXX 02/21/14 10:39:22 update dd because of possible deletion in win_rev 
        name = self.dd['name']
        self.dd = get_ana(name)
        dd = self.dd
        keys_in_db = set([r[0] for r in cr.execute('select meta_key(data) from fact where meta_name(data) = ?', (name,)).fetchall()])

        def mycmp(s):
            # sort by page and y
            q1 = dd['qa']['q'][s][0]
            return (q1[0], q1[1][1])
        
        pgs = self.book.pgs
        tp = (min(pgs) + 1, max(pgs) + 1)
        keys = sorted(list(set(eligible_fact(dd, pg_, tp)) - keys_in_db), key=mycmp)
        
        r = cr.execute('select keys from prefab where name = ?', (name,)).fetchone()
        if not r:
            return 
        kl = json.loads(r[0])
        if len(kl) < len(keys):
            cr.execute('update prefab set keys = ? where name = ?', (json.dumps(keys), name))
            cn.commit()

    def hst_push(self, k):
        dd = self.dd
        qa = dd['qa']
        zo = dd['zo']
        z = self.z()
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
                    self.hst.push(cmd_view(self, s_i, s_f, '%s --> %s' % (s_i, s_f)))
                s_i = dict(s_f) 

    def save(self, b_display=True):
        dd = self.dd
        update_qa(dd)
        dd['last_state'] = self.s()
        dd['sha'] = sha(self.book.src)
        save_ana(dd)
        if not b_display:
            return
        qa = dd['qa']
        s_q = set(qa['q'].keys())
        s_a = set(qa['a'].keys())
        self.send(cnd='saved', count='#qa: %s  #q\\a: %s  #a\\q: %s' % (len(s_q & s_a), len(s_q - s_a), len(s_a - s_q)))
        
    def refresh(self, b_reset=False):
        scn = self.scn
        scn.clear()
        
        dd = self.dd
        pg = str(self.pg())
        
        if pg in dd['bxd']:
            #z = get_z(dd['bxd'][pg]) #* self.width() / (dd['w_desktop'] - 50.)
            z = dd['z'] * 0.96 * self.width() / (dd['w_desktop'])
            # prevent z outlier
            self.set_z(z if z / dd['z'] < 2 else dd['z'])
        
        zo = dd['zo']
        base_dpix = dd.get('dpix', 96)
        zz = 2. * self.z() / zo * self.physicalDpiX() / base_dpix
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
                    
                    scn.addItem(box(mm.map(QPointF(*b[:2])), mm.mapRect(QRectF(QPointF(0, 0), QPointF(*b[2:]))), tk))
            
                yd1, yd2 = dd['yd'][pg]
                for n, y in enumerate([max(yd1, y), min(yd2, y + h)]):
                    scn.addItem(line(mm.map(QPointF(x + w / 2, y)), n))
                
                for b, typ, s, ke in dd['tkd_man'][pg]:            
                    scn.addItem(sep(mm.map(QPointF(*b[:2])), [list(b), typ, s, ke]))
        except:
            pass
            
        self.send(cnd='update')
    
    def get_orig(self):
        pg = str(self.pg() + 1)
        f = cat(self.td, 'orig.tif')
        call(['ddjvu', '-format=tiff', '-page=%s' % pg, self.dd['src'], f]) 
        return f

    def replace(self, f):
        src = self.dd['src']
        pg = str(self.pg() + 1)
        f1 = cat(self.td, '1.djvu')
        call(['cjb2', '-dpi', str(self.book.doc().dpi(self.pg())), f, f1])
        call(['djvm', '-d', src, pg])
        call(['djvm', '-i', src, f1, pg]) 
        self.restart()

    def deskew(self):
        f = self.get_orig() 
        call(['/home/cytu/usr/src/cpp/deskew', f])
        self.replace(f)
    
    def restore(self):
        src = self.dd['src']
        pg = str(self.pg() + 1)
        f1 = cat(self.td, '1.djvu')
        # XXX hack!
        if src.find('/home/cytu') != 0:
            return
        call(['djvused', src.replace('/home/cytu', '/media/Elements'), '-e', 'select %s; save-page-with %s' % (pg, f1)])
        call(['djvm', '-d', src, pg])
        call(['djvm', '-i', src, f1, pg]) 
        self.restart()

    def erase(self, b):
        f = self.get_orig() 
        im = QImage(f)
        dc = self.book.doc()
        dc.set_z(self.dd['zo'])
        pix = dc.render(self.pg())
        m = QTransform(1. * im.width() / pix.width(),   0, 0, 
                       1. * im.height() / pix.height(), 0, 0)
        b = m.mapRect(b)
        p = QPainter(im)
        #for ii, i in enumerate(li):
        i = QImage(QSize(b.size()), QImage.Format_RGB32)
        i.fill(QColor('white').rgb())
        p.drawImage(QPoint(b.topLeft()), i)
        im.convertToFormat(QImage.Format_Mono).save(f)
        p.end()
        self.replace(f)

    def save_sym(self, b):
        td = self.td
        f = cat(td, 'sym.tif')
        QImage(cat(td, 'page.tif')).copy(b).convertToFormat(QImage.Format_Indexed8).save(f)
        self.refresh()

        if 'sym' not in self.dd:
            self.dd['sym'] = {}
        if 'tome' not in self.dd['sym']:
            self.dd['sym']['tome'] = []
        self.dd['sym']['tome'].append(bin_dumps(open(f, 'rb').read()))

    def select_sym(self):
        dc = self.book.doc()
        dc.set_z(self.dd['zo'])
        f = cat(self.td, 'page.tif') 
        dc.render(self.pg()).convertToFormat(QImage.Format_Indexed8).save(f)
        bx = boxes(f, self.book.morph_sym)
        mm = self.mm

        try:
            scn = self.scn
            scn.clear()

            pix = self.doc.pix
            scn.setSceneRect(0, 0, pix.width(), pix.height())
            scn.addItem(QGraphicsPixmapItem(pix))
            
            for b in bx:
                scn.addItem(box_sym(mm.map(QPointF(*b[:2])), mm.mapRect(QRectF(QPointF(0, 0), QPointF(*b[2:]))),md.mapRect(QRect(*b))))
        except:
            pass
    
    def update_pg_fact(self, b_update_qa=True):
        try:
            if b_update_qa:
                b = update_qa(self.dd)
            self.pg_fact = pg_fact(self.dd['qa'])

        except:
            self.pg_fact = {}
        
        try:
            dd = self.dd
            self.d_fact = tk_k_real(self.book, dd['tkd'], dd['yd'], dd['tkd_man'])
        except:
            self.d_fact = {}

    def handler_opr(self, d):
        c = d['cnd']
        if c == 'op_ends':
            self.update_pg_fact()
            self.refresh()
        self.send(**d)
            
    def edit_py(self):
        call(['gvim', cat(cwd, '%s.py' % self.dd['name'])])

    def add_man(self):
        if self.mode == mode_anno:
            self.setCursor(Qt.CrossCursor if self.cursor().shape() == Qt.ArrowCursor else Qt.ArrowCursor)

    def op(self):
        dlg = dlg_op(self)

        if dlg.exec_():
            d = dict.fromkeys(dlg.l)
            for i in dlg.l:
                if getattr(dlg, 'chk_%s' % i).checkState() == Qt.Checked:
                    d[i] = {}
                    d[i]['pgl']= getattr(dlg, 'pgl_%s' % i)
                    if i == 'bxd':
                        d[i]['morph'] = getattr(dlg, 'morph')
            self.opr.go(d=d)
    
    def show_pg_fact(self):
        self.update_pg_fact()

        pg = self.pg()
        if pg in self.pg_fact: 
            b, f = render_pg_fact(self.pg_fact[pg], pg, self.doc, self.mm, self.td)
            self.send(cnd='pg_fact:%s' % ('done' if b else 'error'), f=f)

        else:
            self.send(cnd='pg_fact:none')
    
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
       
    def vim(self):
        if getattr(self, 'pg_vim', -1) >= 0:
            return
        self.pg_vim = self.pg()
        try:
            content = self.dd['note'][str(self.pg_vim)] 
        except:
            content = ''
        self.start_vim(content)

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
    
    def resizeEvent(self, e):
        try:
            dd = self.dd
            self.set_z(dd['z'] * 0.96 * self.width() / (dd['w_desktop']))
            
        finally:
            QGraphicsView.resizeEvent(self, e)
    
    #def wheelEvent(self, e):
    #    n = 1.41 ** (-e.delta() / 240.0)
    #    self.scale(n, n)
    #
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

        elif c == 'before_zoom_changed':
            self.before()

        elif c == 'page_changed':
            self.after()
            self.refresh(b_reset=True)
            self.send(cnd='prefab', w=self) 

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
        
        self.hst.push(cmd_view(self, self.s_i, self.s_f, '%s --> %s' % (self.s_i, self.s_f)))

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
        self.verticalScrollBar().setValue(int(v))

    def set_h(self, h):
        self.horizontalScrollBar().setValue(int(h))

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
                'z':  self.z(), 
                'v':  self.verticalScrollBar().value(), 
                'h':  self.horizontalScrollBar().value()}

    def cls(self):
        try:
            shutil.rmtree(self.td)
            self.nb.close()
            vim_kill(self.nb_name)
        except:
            pass

class lwd(QListWidget):
        
    msg_lwd = pyqtSignal(dict)

    def __init__(self, par):
        QListWidget.__init__(self, par)
        self._par = par
        self.p = None
    
    def send(self, **d):
        self.msg_lwd.emit(d)
    
    def n(self):
        return self.__class__.__name__
    
    def par(self):
        return self._par

    def contextMenuEvent(self, e):
        m = QMenu(self)
        l = [('&try to render', 'render'), None, 
             ('&deskew', 'deskew'), None, 
             ('&restore', 'restore'),
            ]  
        for ll in l:
            if ll is None:
                m.addSeparator()
            else:
                s, f = ll
                m.addAction(s, getattr(self, f))
        
        self.p = e.pos() 
        m.exec_(e.globalPos())
    
    def deskew(self):
        self.par().deskew() 

    def restore(self):
        self.par().restore()

    def render(self):
        i = self.itemAt(self.p)
        if i is None:
            return
        render_fact(self, item_data(i))

class win_hrv(QMainWindow, Ui_win_hrv):

    msg_win_hrv = pyqtSignal()

    def __init__(self, par=None, name=None, key=None, state=None, typ=hrv_read_rev, db_file=None):
        QMainWindow.__init__(self, par)
        self.setupUi(self)
        attrs_from_dict(locals())
        
        # XXX  07/29/13
        self.setStyleSheet('*{font: 11pt "Microsoft JhengHei";} QTextEdit{font: bold; font-size: 20pt;}')       
        # XXX 09/22/15
        self.db_file = db_file if db_file else cat('db', 'ananda.db') 

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
            
        self.tw = t = QTabWidget()
        t.setTabPosition(QTabWidget.West)
        t.setTabsClosable(True)
        t.setDocumentMode(True)
        self.setCentralWidget(t)
        t.currentChanged.connect(self.update_tb)
        t.tabCloseRequested.connect(t.removeTab)

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
            b = sts.value('%s/%s/visible' % (n, i), type=bool)
            getattr(self, i).setVisible(b)
            a.setChecked(b)
            a.toggled.connect(getattr(self, i).setVisible)
            self.addAction(a) 
        
        self.restoreState(sts.value('%s/state' % n, type=QByteArray))        
        self.resize(sts.value('%s/size' % n, type=QSize))
        self.move(sts.value('%s/pos' % n, type=QPoint))
        
        self.stw = stopwatch(self)
        self.root = cwd 

        # create labels and widgets in stb
        stb = self.stb
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
        
        # keyboard shortcut
        for i, k in [('save',       ('F2',)),
                     ('edit_py',    ('F3',)), 
                     ('add_man',    ('F4',)), 
                     ('op',         ('F5',)),
                     ('ed',         ('Ctrl+E',)),
                     ('vim',        ('Ctrl+M',)),
                     ('select_sym', ('F6',)), 
                     ('restart',    ('F7',)), 
                     ('switch_mode',('F12',))]:

            s = 'act_%s' % i
            setattr(self, s, QAction(self))
            a = getattr(self, s)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            a.triggered.connect(partial(self.handler, i))
            self.addAction(a)

        for i in [#'open', 'open_new', 'tab_close', 'tab_close_all', 'save', 'tab_next', 'tab_prev', 
                  'z_in', 'z_out', 'fst', 'last', 'prev', 'next', 'fwd', 'bwd']:
            a = getattr(self, 'act_%s' % i)
            a.triggered.connect(partial(self.handler, i))
            self.addAction(a)

        # ===========================================
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
                db_file = self.db_file
                self.mgr = m = mgr(self, db_file, names=names) 
                m.msg_thread.connect(self.handler_mgr)
                self.rev = r = win_rev(w, names=names, db_file=db_file)
                r.msg_win_rev.connect(self.handler_rev)
                
        self.spl.restoreState(sts.value('%s/spl/state' % self.n(), type=QByteArray))

        self.startTimer(1000)
        
    def n(self):
        return self.__class__.__name__
        
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
                w.alarm(bus.get_object(ifc, '/').state())
                w.showMaximized()
                self.msg({'msg': 'reviewing ...'})

            except:
                pass 

        elif c == 'none':
            self.msg({'msg': ''})
            self.busy = False
    
    def handler_rev(self, d):
        self.busy = False

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
            
            elif c == 'save':
                w.save()
                
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
            
            elif c == 'edit_py':
                w.edit_py()
            
            elif c == 'add_man':
                w.add_man()
            
            elif c == 'op':
                w.op()
            
            elif c == 'select_sym':
                w.select_sym()
            
            elif c == 'restart':
                w.restart()

            elif c == 'switch_mode':
                w.switch_mode()
            
            elif c == 'ed':
                popen(['python', '/home/cytu/usr/src/py/ananda/ed.py', '-c', 
                       json.dumps({'meta': {'name': w.dd['name'], 'key': 'page %s' % (w.pg() + 1)}})])
            elif c == 'vim':
                w.vim() 

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
                self.msg_win_hrv.emit()
                self.close()

        elif c == 'set_mode':
            self.sdb.setVisible(d['mode'] == mode_anno)
            w = self.tw.currentWidget()
            if not w:
                return
            w.refresh()

        elif c == 'prefab':
            if self.typ == hrv_read_rev:
                if not self.busy:
                    d['w'].prefab()

        elif c == 'restart':
            w = self.tw.currentWidget()
            if not w:
                return

            @atexit.register   
            def restart():
                popen(['python', '/home/cytu/usr/src/py/ananda/hrv.py', '-n', w.dd['name']])
            
            self.close()

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
        #try:
        dd = get_ana(name) 
        t = self.tw
        i = t.currentIndex()
        fn, typ = os.path.splitext(os.path.basename(dd['src']))
        f = ellipsis(fn)
        icon = QIcon(':/res/img/%s.png' % typ.lower()[1:])
        
        vw = view(dd=dd, db_file=self.db_file)
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
        w.msg_view.connect(self.handler_view)
        w.setFocus()
        
        w.set_s(dd.get('last_state', {}))

        return True
        
        #except:
        #    return False
    
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
                    self.root = os.path.dirname(f)
                    name = os.path.splitext(os.path.split(f)[1])[0]
                    if not self.create(name, new_tab=new_tab):
                        fl_failed.append(f) 
                except:
                    fl_failed.append(f) 
            
            if fl_failed:
                QMessageBox.warning(self, 'Ebook Harvester: Failed to Open File(s)', 'The following files could not be opened:\n%s' % '\n'.join(fl_failed))
         
    # =======================================
    #  neutral code  
    # =======================================
    
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
            
    def quit(self):
        for i in range(self.tw.count()):
            w = self.tw.widget(i)
            if self.typ != hrv_edt: # not to save again
                w.save()
            w.cls()
        self.cls()

    def find(self):
        #self.tw.currentWidget().ensureVisible(hit.x(), hit.y())
        pass
       
    def full(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def cls(self):
        n = self.n()
        if not self.isFullScreen() and not self.isMaximized():
            sts.setValue('%s/size' % n, QVariant(self.size()))
        
        #sts.setValue('%s/state' % n, QVariant(self.saveState()))        
        sts.setValue('%s/spl/state' % n, QVariant(self.spl.saveState()))

        l = ['mnb', 'stb', 'tb',]
        for i in l:
            sts.setValue('%s/%s/visible' % (n, i), QVariant(getattr(self, i).isVisible()))

    def alarm(self, s):
        d = json.loads(s)
        for k, v in d.items():
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
                tp = ('orange', '[ %d%% ]' % int(100. * t.seconds / T.seconds), nr2t(t.seconds))

            elif st == st_rest:
                t = (t2 - t1) if t2 > t1 else (t1 - t2)
                tp = ('green', 'rest', nr2t(t.seconds))
            
            else:
                tp = ('red', '?', '')
        else:
            tp = ('red', '?', '')
       
        self.update_stb([('stw', '<font color="purple">%s</font>' % (nr2t(self.stw.cnt / 10) if st == st_learn else '')),
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
    DBusQtMainLoop(set_as_default=True) 
    argv = sys.argv
    app = QApplication(argv)
    app.setApplicationName('hrv')
    font = QFont('Microsoft JhengHei')
    #font.setPointSize(16)
    app.setFont(font)
    
    # never put the following before the creation of qt loop 
    bus = dbus.SessionBus()

    argc = len(argv)
    ps = argparse.ArgumentParser(description='Ananda Ebook Harvester')
    ps.add_argument('-n', '--name', dest='name')
    ps.add_argument('-s', '--state', dest='state')
    ps.add_argument('-k', '--key', dest='key')
    ps.add_argument('-t', '--type', type=int, dest='typ', default=hrv_read)
    ps.add_argument('-d', '--database', dest='db_file')
    
    if argc == 1:
        # use in test
        #al = ['-n', 'baldi1']
        #al = ['-n', 'knapp_adv_real']
        al = ['-n', 'schilling'] 
        #al = ['-n', 'jungnickel'] 
        #al = ['-n', 'kirsch_grinberg', '-t', str(hrv_read_rev), '-d', '/home/cytu/usr/src/py/ananda/db/ananda_temp.db']    

    elif argc == 2:
        # use in *.ana file browsing 
        al = ['-n', f_no_ext(argv[1])] 
        
    else:
        al = argv[1:] if argc else []

    w = win_hrv(**ps.parse_args(al).__dict__)
    bus.add_signal_receiver(w.alarm, dbus_interface=ifc, signal_name='alarm')
    try:
        w.alarm(bus.get_object(ifc, '/').state())
    except:
        pass 
    w.showMaximized()

    app.exec_()
