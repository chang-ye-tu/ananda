import os, codecs, re
os.chdir(os.path.dirname(__file__))

def groups():
    def is_ex(t):
        b = False
        for i in t:
            # this is a sentence
            ti = i[1]
            if ti[-1] == '?' or ti[-1] == '!' or ti[-1] == '.' or ti[-1] == '"':
                b = True
                break
        return b
    
    lines = 0
    dic = {'def': '', 'ex': []}
    t, all_dic = [], []
    tag = ''
    for ii, i in enumerate(codecs.open('/home/cytu/usr/doc/lang/txt/Grundwortschatz.txt', 'r', 'utf-8')):
        if i.strip():
            lines += 1
            t.append((ii + 1, i.strip()))

        else:
            if lines:
                s = '\n'.join([ti[1] for ti in t])
                if lines == 2:
                    # possibly sentence 
                    if re.search(r'^\d+', ''.join([ti[1] for ti in t])):
                        if is_ex(t):
                            dic['ex'].append(s)
                        
                        else:
                            # section: eg '1.1 Körper'
                            pass

                    else:                        
                        if is_ex(t):
                            dic['ex'].append(s)

                        else:
                            all_dic.append(dic)
                            dic = {'def': s, 'ex': []}

                elif lines >= 3:
                    all_dic.append(dic)
                    dic = {'def': s, 'ex': []}
                
                else:
                    # freq: '1-2000', '2001-4000'
                    pass

                lines, t = 0, []

    return all_dic 
