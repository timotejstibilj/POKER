#ponekod kjer piše kira_miza je to nesmiselno uporabljeno, ker je že določen objekt miza = miza()
#popravi

import random
from itertools import combinations 

class igra():
    def nova_igra(self):
        miza = miza()
        deck = deck()
        deck.premešaj_karte()
        
        #preflop
        self.spremeni_položaj_igralcev()
        self.razdeli_karte()

        self.izračunaj_verjetnost_zmage()
        #nekaterim se pokaže

        self.stavi_small_in_big_blind()
        self.krog_stav()
        #flop
        deck.položi_flop(kira_miza)
        self.kdo_je_živ()
        self.kdo_je_v_igri()

        self.izračunaj_verjetnost_zmage()

        self.krog_stav()
        #turn
        deck.položi_eno_na_mizo(kira_miza)
        self.kdo_je_živ()
        self.kdo_je_v_igri()

        self.izračunaj_verjetnost_zmage()

        self.krog_stav()
        #river
        deck.položi_eno_na_mizo(kira_miza)
        self.kdo_je_živ
        self.kdo_je_v_igri

        self.izračunaj_verjetnost_zmage()

        self.krog_stav
        #tu bi prišla kakšna zanka prav

        self.kdo_je_zmagal()
        #ovrednosti kombinacije, pove kdo ima najboljšo

        self.razdeli_pot()
        self.spremeni_položaj_igralcev()

        



    #na koncu runde se morajo igralci znebit nekaterih atributov, npr. fold, kart itd.
    #class igro premakni na dno, ko so vsi objekti in funkcije že definirani
    #tu so že zapisane, uporabljene tudi funkcije , ki jih še nisem definiral

    def kdo_je_živ(self, ime_resničnega_igralca):
        igralci = ["ime_resničnega_igralca", "nespameten_goljuf", "ravnodušnež", "agresivnež", "blefer"]
        igralci_v_igri = []
        for igralec in igralci:
            if igralec.žetoni > 0:
                igralci_v_igri.append(igralec)
        return igralci_v_igri
        #igralci, ki imajo še kaj žetonov

    def kdo_je_v_igri(self):
        [igralec for igralec in kdo_je_živ(self, ime_resničnega_igralca) if not igralec.fold]
        #igralci, ki še niso foldali

    def spremeni_položaj_igralcev(self):
        pass
        #spremeni kdo je small, big blind, dealer, first actor
    
    def stavi_small_in_big_blind(self, kira_miza):
        for igralec in self.kdo_je_živ(ime_resničnega_igralca):
            if igralec.položaj == "small blind":
                igralec.žetoni -= 10
                kira_miza.pot += 10
            elif igralec.položaj == "big blind":
                igralec.žetoni -= 20
                kira_miza.pot +=20  

    def razdeli_karte(self):
        pass      

    def igralec_na_potezi(self):
        pass

    def krog_stav(self):
        pass
    #ime zavaja, ker ni nujno le en krog, saj se lahko igralci neprestalno višajo - raise
    #trenutno nimam boljšega imena  
    


class karta():
    def __init__(self, znak, stevilo):
        self.znak = znak
        self.stevilo = stevilo

    def __repr__(self):
        slovar_stevil = {1: "'AS'", 11: "'FANT'", 12: "'DAMA'", 13: "'KRALJ'"}
        for i in range(2, 11):
            slovar_stevil[i] = i
        znakci = {0: "'križ'", 1: "'pik'", 2: "'srce'", 3: "'kara'"}
        return "({},{})".format(znakci.get(self.znak), slovar_stevil.get(self.stevilo))

class deck(list):
    def __init__(self):
        super().__init__()
        for stevilo in range(1, 14):
            for znak in range(4):
                self.append(karta(znak, stevilo))
    
    def premešaj_karte(self):
        random.shuffle(self)
    
    def razdeli_eno_karto(self, komu):
        komu.karte.append(self.pop(0))

    def položi_flop(self, kira_miza):
        for i in range(3):
            kira_miza.karte.append(self.pop(0))
    
    def položi_eno_na_mizo(self, kira_miza):
        kira_miza.karte.append(self.pop(0))
    #turn, river in pred flopom, med flopom/turnom, turnom/riverjem

class miza():
    def __init__(self):
        self.karte = []
        self.pot = 0
        self.small_blind = 10
        self.big_blind = 20
    
    def __repr__(self):
        return "Karte na mizi so {}".format(self.karte)

class igralec():
    def __init__(self, ime=None):
        self.ime = ime
        self.karte = []
        self.kombinacija = 0
        self.miza = ""
        self.žetoni = 1000
        self.žetoni_v_igri = 0
        self.razlika_za_klicat = 0
        self.fold = False
        self.na_potezi = False
        self.all_in = False
        #tle se mu šteje čas, če je True
        self.položaj = "položaj"
        self.čas = "čas"
        self.zmaga = False
    #tle je kr neki napisano, moraš popravit
    #položaj je če je big blind, small blind
    
    def __repr__(self):
        return "Igralec {} s kartama {} in {} žetoni.".format(self.ime, self.karte, self.žetoni)
##############################################################
    def check(self):
        pass

    def fold(self):
        self.fold = True

    def stavi(self, koliko, kira_miza):
        self.žetoni -= koliko
        kira_miza.pot += koliko
    
    def poberi_celoten_pot(self, kira_miza):
        self.žetoni += kira_miza.pot
        #if self.zmaga

##############################################################
    
    def seznam_kombinacij_kart(self, kira_miza):
        izbira_iz = self.karte + kira_miza.karte
        return list(combinations(izbira_iz, 5))
        #v metodo moraš napisat za katero mizo se gleda

    def karte_na_pol_od_peterke(self, peterka):
        znaki = []
        stevila = []
        for karta in peterka:
            znaki.append(karta[0])
            stevila.append(karta[1])
        return znaki, stevila

    def max_stevilo_pojavitev_v_peterki(self, peterka):
        max = 0
        for i in range(14):
            if self.karte_na_pol_od_peterke(peterka)[1].count(i) > max:
                max = self.karte_na_pol_od_peterke(peterka)[1].count(i)
        return max

    def barvna_lestvica(self, peterka):
        return self.barva and self.lestvica

    def poker(self, peterka):
        #max stevilo pojavitev = 4
        return self.max_stevilo_pojavitev_v_peterki(peterka) == 4

    def full_house(self, peterka):
        pass

    def barva(self, peterka):
        return len(set(self.karte_na_pol_od_peterke(peterka)[0])) == 1

    def lestvica(self, peterka):
        pass

    def tris(self, peterka):
        return self.max_stevilo_pojavitev_v_peterki(peterka) == 3

    def dva_para(self, peterka):
        pass

    def par(self, peterka):
        #max_Stevilo_ponovitev = 1
        pass

    def kombinacija(self, kira_miza):
        for kombinacija in self.seznam_kombinacij_kart(kira_miza):
            if self.barvna_lestvica(kombinacija):
                self.kombinacija = 8
            elif self.poker(kombinacija):
                self.kombinacija = 7
            elif self.full_house(kombinacija):
                self.kombinacija = 6
            elif self.barva(kombinacija):
                self.kombinacija = 5
            elif self.lestvica(kombinacija):
                self.kombinacija = 4
            elif self.tris(kombinacija):
                self.kombinacija = 3
            elif self.dva_para(kombinacija):
                self.kombinacija = 2
            elif self.par(kombinacija):
                self.kombinacija = 1
            else:
                self.kombinacija = 0
        #v primeru visoke karte vrne 0, močnejši kot je hand. več točk dobiš
        #pazi na možnost iste kombinacije z drugo močjo, npr. močnješa barva in primera, da pride do istega hand-a

class agresivnež(igralec):
    pass
    #dosti stavi

class ravnodušnež(igralec):
    pass
    #random

class blefer(igralec):
    pass
    #rad blefira

class nespameten_goljuf(igralec):
    pass
    #vidi vse karte, ampak pri odločanju ne upošteva pogojne verjetnosti (pri računanju ne upošteva kart ostalih igralec),
    #temveč se zanaša na verjetnost zmage posameznega igralca



#TEST:
dek = deck()
miza = miza()
for karta in dek:
    print(karta)
dek.premešaj_karte()
print("============")
print(dek)
print("============")
janez = igralec("janez")
print(janez)
lojze = igralec(("lojze"))
print(lojze)
print("============")


dek.razdeli_eno_karto(janez)   
#moraš dodat dek. ker je to metoda v classu deck, dek je objekt iz razreda deck    


dek.razdeli_eno_karto(janez)  
print(janez)
print("============")
dek.razdeli_eno_karto(lojze)
dek.razdeli_eno_karto(lojze)
print(lojze)
print("============")

dek.položi_flop(miza)
print(miza)
print("============")
dek.položi_eno_na_mizo(miza)
print(miza)
print("============")
dek.položi_eno_na_mizo(miza)
print(miza)
print("============")

for kombinacija in lojze.seznam_kombinacij_kart(miza):
    print(lojze.seznam_kombinacij_kart(miza).index(kombinacija) + 1, kombinacija)

print("============")
print("============")

peter = igralec("peter")
dek.razdeli_eno_karto(peter)
dek.razdeli_eno_karto(peter)
print(peter.seznam_kombinacij_kart(miza)[0])
print(peter.karte_na_pol_od_peterke((('kara',10), ('križ',6), ('pik',2), ('pik',9), ('srce',2))))

print("============")
janez.stavi(122, miza)
print(janez.žetoni)
print(miza.pot)

#dodal še nedelujoče kombinacije, 4 tipe igralcev in začel graditi strukturo poteka igre