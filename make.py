# -*- coding: utf-8 -*-

import os, fnmatch, subprocess, codecs

os.chdir(os.path.dirname(__file__))
pr = os.path.basename(os.getcwd())
cat = os.path.join

def all_files(root, patterns='*', top_level=False, yield_folders=False):
    
    # Expand patterns from semicolon-separated string to list
    patterns = patterns.split(';')
    
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield cat(path, name)
                    break
        if top_level:
            break

QRC = '''<!DOCTYPE RCC>
<RCC version="1.0">
<qresource>
%s
</qresource>
</RCC>'''

# compose *.qrc
files = []
for tp in ('*.png', '*.ico'):
    for path in all_files('./res/img', tp, yield_folders=False):
        files.append(path.replace('\\', '/'))
open(cat('res', pr + '.qrc'), 'w').write(QRC % ('\n'.join(['<file>../%s</file>' % f[2:] for f in files])))

subprocess.call(['pyrcc5', '-o', './ui/%s_rc.py' % pr, cat('res', '%s.qrc' % pr)])

for i, path in enumerate(all_files('./designer', '*.ui')):
    f = os.path.basename(path)[:-3]
    ff = os.path.abspath(path)
    ft = codecs.open(ff, 'r', 'utf-8')
    s = ft.read()
    ft.close()
    
    codecs.open(ff, 'w', 'utf-8').write(s.replace('微軟正黑體', 'Microsoft JhengHei'))
    open(ff, 'w').write(s)    
    subprocess.call(['pyuic5', '--from-imports', '-x', '-o', './ui/%s.py' % f, ff])
