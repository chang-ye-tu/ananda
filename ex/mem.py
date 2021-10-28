import os, itertools

cat = os.path.join
root = cat(os.getcwd(), 'ex')

img_s = '<img src="%s" class="image"/>'
nr_type = {'s': '0', 
           'd': '1', 
           'a': '2', 
           'm': '3', 
           'r': '4', 
           'l': '5', 
           'j': '6', 
           'c': '7', 
           'g': '8', 
           'b': '9'}

def gets(s):
    d = nr_type if s.isalpha() else dict([(v, k) for k, v in nr_type.items()]) 
    return ''.join([d[i] for i in s])

def img(s, typ='person'):    
    return img_s % cat(root, 'nr', typ, '%s.jpg' % gets(s))

sn = [str(nn).zfill(2) for nn in range(100)]  # 0, 1, 2, ..., 99

sn1 = [str(nn).zfill(2) for nn in itertools.chain.from_iterable([(reversed([10*n + i for n in range(10)]) if i%2 else [10*n + i for n in range(10)]) for i in range(10)])]   # 0, 10, 20, 30, ..., 90, 91, 81, 71, ..., 11, 12, 22, 32, ... 

nr_person = [(s, img(s)) for s in sn]
nr_action = [(s, img(s, typ='action')) for s in sn]
nr_action_1 = [(s, img(s, typ='action')) for s in sn1]
person_nr = [(b, a) for a, b in nr_person]
action_nr = [(b, a) for a, b in nr_action]

# 4 digits: person-action, 2 tuple; d4:  fix 1, var 2; d4_: var 1, fix 2
d4 = [(ssm + ssn,  img(ssm) + img(ssn, typ='action')) for ssn in sn for ssm in sn]
d4_ = [(ssn + ssm, img(ssn) + img(ssm, typ='action')) for ssn in sn for ssm in sn]

d41 = [(ssm + ssn,  img(ssm) + img(ssn, typ='action')) for ssn in sn1 for ssm in sn1]
d41_ = [(ssn + ssm, img(ssn) + img(ssm, typ='action')) for ssn in sn1 for ssm in sn1]

def card():
    card_suite = ['spades', 'hearts', 'diamonds', 'clubs']
    card_type = range(1, 11)
    card_type.extend(['jack', 'queen', 'king'])
    card = ['%s of %s' % (i, j) for i in card_type for j in card_suite]
    return [cat(root, 'cards', '%s.jpg' % i) for i in card]

def mj():
    mj_suite = ['bamboo', 'character', 'circle']
    mj_type = range(1, 10)
    mj = ['%s_%s' % (i, j) for i in mj_suite for j in mj_type] 
    mj.extend(['dragon_1', 'dragon_2', 'dragon_3', 
               'wind_1', 'wind_2', 'wind_3', 'wind_4'])
    return [cat(root, 'mj', '%s.png' % i) for i in mj]

#mj_card = [(img_s % i, img_s % j) for i in mj() for j in card()]
