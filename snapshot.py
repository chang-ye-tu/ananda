from base import *

def limit_point_to_rect(p, r):
    q = QPoint()
    q.setX(r.x() if p.x() < r.x() else p.x() if p.x() < r.right() else r.right()) 
    q.setY(r.y() if p.y() < r.y() else p.y() if p.y() < r.bottom() else r.bottom())
    return q

class camera(QWidget):

    def __init__(self):
        super(camera, self).__init__(None)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setMouseTracking(True)
        self.sel = QRect()
        self.mouse_down = False
        
        self.service = SnapshotService(self)

        self.screen = QApplication.primaryScreen()
        self.winid = QApplication.desktop().winId()
        self.pix = self.screen.grabWindow(self.winid)
        self.showFullScreen()
        self.resize(self.pix.size())
        self.setCursor(Qt.CrossCursor)
        
    def grab(self, p, rct=None):
        fp = os.path.join('/home/cytu/usr/src/py/test/pix', f"{datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d-%H-%M-%S')}.png")
        p.save(fp) 
        d = {'f': fp}
        if rct:
            d['rct'] = rct
        self.service.select(json.dumps(d))
        self.close()

    def exit(self):
        self.close()

    def paintEvent(self, e):
        p = QPainter(self)
        p.drawPixmap(0, 0, self.pix)
        r = self.sel.normalized()#.adjusted(0, 0, -1, -1)
        if not self.sel.isNull():
            p.drawRect(r)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if not self.mouse_down:
                self.mouse_down = True
                self.start_point = e.pos()
        self.update()

    def mouseMoveEvent(self, e):
        if self.mouse_down:
            p = e.pos()
            r = self.rect()
            self.sel = QRect(self.start_point, limit_point_to_rect(p, r)).normalized()
            self.update()

    def mouseReleaseEvent(self, e):
        r = self.sel.normalized()
        p = None
        if not r.isNull() and r.isValid():
            r = r.adjusted(1, 1, -1, -1) 
            x, y, w, h = r.x(), r.y(), r.width(), r.height()
            try:
                p = self.screen.grabWindow(self.winid, x, y, w, h) 
                if p is not None:
                    self.grab(p, [x, y, w, h])
            except:
                print('An error occurred in snapshot.py.')
                self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = camera()
    app.exec()
