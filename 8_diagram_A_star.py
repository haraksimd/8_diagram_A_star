'''
created by: Daniel Haraksim
project: 8-diagram solved by A* algorithm
description: Solving n x m diagram with A* algorithm
'''
import copy
import time

#definovanie vstupu a rozmerov plochy
M = 3
N = 2

start = ['m',1,2,3,4,5]
ciel = [3,4,5,'m',1,2]


velkost_q = [0]


#deklarovanie objektu Uzol
class Uzol:
    def __init__(self,stav,rodic,hlbka,odhad,predosly):
        self.stav = stav
        self.rodic = rodic
        self.hlbka = hlbka
        self.odhad = odhad
        self.predosly = predosly

#funkcia na vyvorenie pociatocneho uzla
def pociatocny_uzol():
    uzol = Uzol(start, None, 0, 0, "")

    #deklarovanie fronty a listu spracovanych statov
    queue = []
    spracovane = []
    #ulozenie pociatocneho uzlu na zaciatok fronty
    queue.insert(0,uzol)
    velkost_q[0] += 1

    return uzol,queue,spracovane

#funkcia pre vypocet heuristiky
def heuristika(stav):
    h_hodnota = 0
    #prehladavanie stavu
    for i in range(0,len(stav)):
        #preskakovanie prazdnych policok aby hodnota nebola vyssia ako ma byt
        if stav[i] == 'm':
            continue
        #ak sa policko stavu nerovna policku v cieli tak pridaj hodnotu cesty
        if stav[i] != ciel[i]:
            h_hodnota += 1
    return h_hodnota

def heuristika2(stav):
    h_hodnota = 0
    index_stav = 0
    index_ciel = 0

    #hladanie indexu v aktualnom uzle
    for i in range(len(stav)):
        # preskakovanie prazdnych policok aby hodnota nebola vyssia ako ma byt
        if stav[i] == 'm':
            continue
        #hladanie indexu v cielovom stave
        for x in range(len(stav)):
            #ak je stavova hodnota v aktualnom uzle a cielovom stave rovnaka tak ich prirad do premennych
            if stav[i] == ciel[x]:
                index_stav = i
                index_ciel = x
                break
        # pocitanie dlzky
        div1 = index_stav // M
        div2 = index_ciel // M
        abs_div = abs(div1 - div2)
        mod1 = index_stav % M
        mod2 = index_ciel % M
        abs_mod = abs(mod1 - mod2)
        h_hodnota = h_hodnota + (abs_div+abs_mod)
    return h_hodnota

def odhad(stav,hlbka):
    #A* algoritmus
    f_hodnota = heuristika(stav) + hlbka

    return f_hodnota

def zarad_do_q(uzol,queue):
    #prehladavanie vo queue
    for i in range(0,velkost_q[0]):
        #ak je odhad ceny cesty vacsi ako aktualny uzol tak akt. uzol pridaj do fronty pred vacsi odhad vo fronte
        if queue[i].odhad > uzol.odhad:
            queue.insert(i,uzol)
            velkost_q[0] += 1
            return
    #ak su vsetky mensie pridaj akt. uzol na koniec fronty
    queue.append(uzol)
    velkost_q[0] += 1

"""tieto komentare plati pre zvysne operatory"""
def hore(uzol,queue):
    #kopirovanie stavu uzla do pomocnej premennej
    novy_stav = copy.deepcopy(uzol.stav)
    #ak predosli operator bol opacny od aktualneho, nevykonam ho aby sme nekontrolovali rovnaky stav
    if uzol.predosly != "dole":
        #hladanie prazdneho policka v stave
        for i in range(0,len(novy_stav)):
            #ak sme nasli prazdne policko vymenime ho pomocou systemu 3 poharov inac pokracujem v hladani
            if novy_stav[i] == 'm' :
                if i+M < len(novy_stav) :
                    temp = novy_stav[i]
                    novy_stav[i] = novy_stav[i+M]
                    novy_stav[i+M] = temp
                    break
                else :
                    return
        #vytvorime novy uzol s novym stavom, hlbkou, odhadom ceny cesty a predoslym operatorom
        novy_uzol = Uzol(novy_stav,uzol,uzol.hlbka+1, odhad(novy_stav,uzol.hlbka+1),"hore")
        #zavolame funkciu na zaradenie do fronty
        zarad_do_q(novy_uzol,queue)
    else:
        return

def dole(uzol,queue):
    novy_stav = copy.deepcopy(uzol.stav)
    if uzol.predosly != "hore":
        for i in range(0, len(novy_stav)):
            if novy_stav[i] == 'm':
                if i-M > -1:
                    temp = novy_stav[i]
                    novy_stav[i] = novy_stav[i-M]
                    novy_stav[i-M]= temp
                    break
                else:
                    return
        novy_uzol = Uzol(novy_stav,uzol,uzol.hlbka+1, odhad(novy_stav,uzol.hlbka+1),"dole")
        zarad_do_q(novy_uzol,queue)
    else:
        return

def vlavo(uzol,queue):
    novy_stav = copy.deepcopy(uzol.stav)
    if uzol.predosly != "vpravo":
        for i in range(0,len(novy_stav)):
            if novy_stav[i]=='m':
                if i%M != M-1 :
                    temp = novy_stav[i]
                    novy_stav[i] = novy_stav[i+1]
                    novy_stav[i+1] = temp
                    break
                else: return
        novy_uzol = Uzol(novy_stav,uzol,uzol.hlbka+1, odhad(novy_stav,uzol.hlbka+1),"vlavo")
        zarad_do_q(novy_uzol,queue)
    else: return

def vpravo(uzol,queue):
    novy_stav = copy.deepcopy(uzol.stav)
    if uzol.predosly != "vlavo":
        for i in range(0,len(novy_stav)):
            if novy_stav[i] == 'm':
                if i%M == 0:
                    return
                else :
                    temp = novy_stav[i]
                    novy_stav[i] = novy_stav[i-1]
                    novy_stav[i - 1] = temp
                    break
        novy_uzol = Uzol(novy_stav,uzol,uzol.hlbka+1, odhad(novy_stav,uzol.hlbka+1),"vpravo")
        zarad_do_q(novy_uzol,queue)
    else: return

def sprav_uzol(uzol,queue):
    #zavolame vsetky operatory aby sme vyvorili uzly
    vpravo(uzol,queue)
    dole(uzol, queue)
    vlavo(uzol, queue)
    hore(uzol, queue)

def spatny_vypis(uzol):
    #rekurzivny spatny vypis stavov cesty
    if uzol is None:
        return
    print(uzol.stav)

    spatny_vypis(uzol.rodic)

def kontrola_akt(queue,spracovane):
    #popnutie aktualneho uzla zo zaciatku fronty
    akt_uzol = queue.pop(0)
    velkost_q[0] -= 1

    #ak bol uzol v liste spracovane ukoncime funkciu a vratime False
    if akt_uzol.stav in spracovane:
        return False
    #ak uzol sa zhoduje s cielovym vypisem spatny vypis, potrebne udaje a vratime True
    if akt_uzol.stav == ciel:
        spatny_vypis(akt_uzol)
        print("Počet spracovaných: %s" % len(spracovane))
        print("Hĺbka výsledného uzla je : %s" % akt_uzol.hlbka)
        print("Program trval %s sekund" % (time.time() - start_time))
        return True
    #ak sa nezhoduje sprav dalsi uzol a potom pridaj akt. uzol do spracovanych a returni False
    else:
        sprav_uzol(akt_uzol,queue)
    spracovane.append(akt_uzol.stav)

    return False

#definovanie vstupu pomocou command line
"""print("Zadaj rozmer pola MxN\nM:")
M = int(input())
print("N:")
N = int(input())
print("Velkost pola je {}x{}".format(M,N))
puz_velkost = M * N
print("Zadaj vstupný stav")
for i in range(puz_velkost):
    start.append(input())
print("Zadaj vystupny stav")
for i in range(puz_velkost):
    ciel.append(input())"""

#startovanie pocitania casu
start_time = time.time()
#deklaracia pociatocneho uzla do premennych
uzol, queue, spracovane = pociatocny_uzol()
#deklarovanie premennej na kontrolu
kontrola = False
#pokial funkcia kontrola_akt nevrati True volaj ju
while kontrola != True:
    kontrola = kontrola_akt(queue,spracovane)

