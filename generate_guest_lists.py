from random import randint

Guests = []
LIST_MAX_LENGHT = 999
GUESTS_QTT = 0

if input('Should emails be generated randomly? [y/n]... ')[0] in 'yY':    
    GUESTS_QTT = 999
    for _ in range (GUESTS_QTT):
        email = ''
        for __ in range (8):
            email += 'abcdefghijklmnopqrstuvwxyz0123456789'[randint(0, 35)]
        Guests.append(email + '@test.smt')
else:
    try:
        with open('guests.txt', 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                Guests.append(line)
                GUESTS_QTT += 1
            f.close()
    except:
        print('File not found.')

rng = GUESTS_QTT // LIST_MAX_LENGHT
if GUESTS_QTT % LIST_MAX_LENGHT > 0: rng += 1
print(GUESTS_QTT, Guests)

for i in range (rng):
    with open(f'guests_list_{i}.txt', 'w+') as f:
        for j in range(GUESTS_QTT - (LIST_MAX_LENGHT * i), max(0, GUESTS_QTT - (LIST_MAX_LENGHT * (i + 1))), -1):
            f.write(Guests[j - 1] + '\n')
