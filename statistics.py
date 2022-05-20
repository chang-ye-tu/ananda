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

"""
A clone of 'sensors' utility on Linux printing hardware temperatures.

$ python3 scripts/sensors.py
asus
    asus                 47.0 °C (high = None °C, critical = None °C)

acpitz
    acpitz               47.0 °C (high = 103.0 °C, critical = 103.0 °C)

coretemp
    Physical id 0        54.0 °C (high = 100.0 °C, critical = 100.0 °C)
    Core 0               47.0 °C (high = 100.0 °C, critical = 100.0 °C)
    Core 1               48.0 °C (high = 100.0 °C, critical = 100.0 °C)
    Core 2               47.0 °C (high = 100.0 °C, critical = 100.0 °C)
    Core 3               54.0 °C (high = 100.0 °C, critical = 100.0 °C)
"""

#import psutil
#
#def main():
#    if not hasattr(psutil, "sensors_temperatures"):
#        sys.exit("platform not supported")
#    temps = psutil.sensors_temperatures()
#    if not temps:
#        sys.exit("can't read any temperature")
#    for name, entries in temps.items():
#        print(name)
#        for entry in entries:
#            print("    %-20s %s °C (high = %s °C, critical = %s °C)" % (
#                entry.label or name, entry.current, entry.high,
#                entry.critical))
#        print()

"""
A clone of 'sensors' utility on Linux printing hardware temperatures,
fans speed and battery info.

$ python3 scripts/sensors.py
asus
    Temperatures:
        asus                 57.0°C (high=None°C, critical=None°C)
    Fans:
        cpu_fan              3500 RPM
acpitz
    Temperatures:
        acpitz               57.0°C (high=108.0°C, critical=108.0°C)
coretemp
    Temperatures:
        Physical id 0        61.0°C (high=87.0°C, critical=105.0°C)
        Core 0               61.0°C (high=87.0°C, critical=105.0°C)
        Core 1               59.0°C (high=87.0°C, critical=105.0°C)
Battery:
    charge:     84.95%
    status:     charging
    plugged in: yes
"""

#def secs2hours(secs):
#    mm, ss = divmod(secs, 60)
#    hh, mm = divmod(mm, 60)
#    return "%d:%02d:%02d" % (hh, mm, ss)
#
#def main():
#    if hasattr(psutil, "sensors_temperatures"):
#        temps = psutil.sensors_temperatures()
#    else:
#        temps = {}
#    if hasattr(psutil, "sensors_fans"):
#        fans = psutil.sensors_fans()
#    else:
#        fans = {}
#    if hasattr(psutil, "sensors_battery"):
#        battery = psutil.sensors_battery()
#    else:
#        battery = None
#
#    if not any((temps, fans, battery)):
#        print("can't read any temperature, fans or battery info")
#        return
#
#    names = set(list(temps.keys()) + list(fans.keys()))
#    for name in names:
#        print(name)
#        # Temperatures.
#        if name in temps:
#            print("    Temperatures:")
#            for entry in temps[name]:
#                print("        %-20s %s°C (high=%s°C, critical=%s°C)" % (
#                    entry.label or name, entry.current, entry.high,
#                    entry.critical))
#        # Fans.
#        if name in fans:
#            print("    Fans:")
#            for entry in fans[name]:
#                print("        %-20s %s RPM" % (
#                    entry.label or name, entry.current))
#
#    # Battery.
#    if battery:
#        print("Battery:")
#        print("    charge:     %s%%" % round(battery.percent, 2))
#        if battery.power_plugged:
#            print("    status:     %s" % (
#                "charging" if battery.percent < 100 else "fully charged"))
#            print("    plugged in: yes")
#        else:
#            print("    left:       %s" % secs2hours(battery.secsleft))
#            print("    status:     %s" % "discharging")
#            print("    plugged in: no")

#if __name__ == '__main__':
#    DBusQtMainLoop(set_as_default=True) 
#    argv = sys.argv
#    app = QApplication(argv)
#    app.setApplicationName('statistics')
#    app.setFont(QFont('Microsoft JhengHei'))
#    w = win_stat()
#    w.show()
#    app.exec_()
