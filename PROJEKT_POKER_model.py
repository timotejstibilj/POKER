import random
from itertools import combinations 
from datetime import time
#rabil bom odštevalnik za osebe

class karta():
    def __init__(self, znak, stevilo):
        self.znak = znak
        self.stevilo = stevilo

    def __repr__(self):
        slovar_stevil = {11: "'FANT'", 12: "'DAMA'", 13: "'KRALJ'", 14: "'AS'"}
        for i in range(2, 11):
            slovar_stevil[i] = i
        znakci = {0: "'križ'", 1: "'pik'", 2: "'srce'", 3: "'kara'"}
        return "({},{})".format(znakci.get(self.znak), slovar_stevil.get(self.stevilo))

class deck(list):
    def __init__(self):
        super().__init__()
        for stevilo in range(2, 15):
            for znak in range(4):
                self.append(karta(znak, stevilo))
    
    def premešaj_karte(self):
        random.shuffle(self)
    
    def deli_karto(self, komu, koliko_kart):
        for i in range(koliko_kart):
            komu.karte.append(self.pop(0))
    
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
        self.kombinacija = []
        self.miza = ""
        self.žetoni = 1000
        self.žetoni_v_igri = 0
        self.razlika_za_klicat = 0
        self.fold = False
        self.na_potezi = False
        #tle se mu šteje čas, če je True
        self.čas = "čas"
        self.all_in = False
        self.položaj = "položaj"
        self.zmaga = False
    #položaj je če je big blind, small blind
    
    def __repr__(self):
        ime = self.ime
        return ime

##############################################################
    def check(self):
        pass

    def folda(self):
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
        vrni = []
        for card in peterka:
            znaki.append(card.znak)
            stevila.append(card.stevilo)
        vrni.append(znaki)
        vrni.append(stevila)
        return vrni

    def max_stevilo_pojavitev_v_peterki(self, peterka):
        max = 0
        stevila = self.karte_na_pol_od_peterke(peterka)[1]
        for i in range(2, 15):
            if stevila.count(i) > max:
                    max = stevila.count(i)
        return max

    #hand-i definirani za izbrano peterko in ne še najboljši hand igralca
    def barvna_lestvica(self, peterka):
        return self.barva(peterka) and self.lestvica(peterka)

    def poker(self, peterka):
        return self.max_stevilo_pojavitev_v_peterki(peterka) == 4

    def full_house(self, peterka):
        return self.tris(peterka) and len(set(self.velikosti_preostalih_kart(peterka))) == 1

    def barva(self, peterka):
        return len(set(self.karte_na_pol_od_peterke(peterka)[0])) == 1

    def lestvica(self, peterka):
        najmanjša = 14
        vrni = False
        številke = self.karte_na_pol_od_peterke(peterka)[1]
        for številka in številke:
            if številka < najmanjša:
                najmanjša = številka
        if številke.sort() == list(range(najmanjša, najmanjša + 5)):
            vrni = True
        elif številke.sort() == [2, 3, 4, 5, 14]:
            vrni = True
            #ker je AS reprezentiran s 14, ampak je lahko tudi v vlogi 1
        return vrni

    def tris(self, peterka):
        return self.max_stevilo_pojavitev_v_peterki(peterka) == 3

    def dva_para(self, peterka):
        druge_karte = set()
        for stevilo in self.velikosti_preostalih_kart(peterka):
            druge_karte.add(stevilo)
        return self.max_stevilo_pojavitev_v_peterki(peterka) == 2 and len(druge_karte) == 2

    def par(self, peterka):
        return self.max_stevilo_pojavitev_v_peterki(peterka) == 2

    def kombinacija_od_peterke(self, peterka):
        if self.barvna_lestvica(peterka):
            moč_hand_a = 8
        elif self.poker(peterka):
            moč_hand_a = 7
        elif self.full_house(peterka):
            moč_hand_a = 6
        elif self.barva(peterka):
            moč_hand_a = 5
        elif self.lestvica(peterka):
            moč_hand_a = 4
        elif self.tris(peterka):
            moč_hand_a = 3
        elif self.dva_para(peterka):
            moč_hand_a = 2
        elif self.par(peterka):
            moč_hand_a = 1
        else:
            moč_hand_a = 0
        return moč_hand_a

    def velikost_pomembne_karte(self, peterka):
        velikost_pomembne_karte = 0
        stevila = self.karte_na_pol_od_peterke(peterka)[1]
        for i in range(2, 15):
            if stevila.count(i) == self.max_stevilo_pojavitev_v_peterki(peterka):
                if i > velikost_pomembne_karte:
                    velikost_pomembne_karte = i
        return velikost_pomembne_karte
    
    def velikosti_preostalih_kart(self, peterka):
        velikosti_preostalih_kart = []
        stevila = self.karte_na_pol_od_peterke(peterka)[1]
        for stevilo in stevila:
            if stevilo != self.velikost_pomembne_karte(peterka):
                velikosti_preostalih_kart.append(stevilo)
        velikosti_preostalih_kart.sort(reverse=True)
        return velikosti_preostalih_kart
    
    def lastnosti_kombinacije_igralca(self, kira_miza):
        moč_kombinacije = 0
        velikost_pomembne_karte = 0
        velikosti_preostalih_kart = []
        najmočnejše_kombinacije = []
        najmočnejša_kombinacija = []
        for combination in self.seznam_kombinacij_kart(kira_miza):
            if self.kombinacija_od_peterke(combination) >= moč_kombinacije:
                moč_kombinacije = self.kombinacija_od_peterke(combination)
        for combination in self.seznam_kombinacij_kart(kira_miza):
            if self.kombinacija_od_peterke(combination) == moč_kombinacije:
                najmočnejše_kombinacije.append(combination)
        for komb in najmočnejše_kombinacije:
            if self.velikost_pomembne_karte(komb) >= velikost_pomembne_karte:
                najmočnejša_kombinacija = komb
        velikost_pomembne_karte = self.velikost_pomembne_karte(najmočnejša_kombinacija)
        velikosti_preostalih_kart = (self.velikosti_preostalih_kart(najmočnejša_kombinacija))
        kombinacija = [moč_kombinacije, velikost_pomembne_karte, velikosti_preostalih_kart]
        return kombinacija     
        
####################################################################################################

class kvazi_AI(igralec):
    "kvazi_AI pokaže verjetnosti zmage posameznih igralcev."
    def __init__(self, ime):
        super().__init__(ime)
        
class agresivnež(igralec):
    "Kot ime pove, agresivnež rad poseže globoko v žep in visoko stavi tudi v tveganih situacijah."
    def __init__(self, ime):
        super().__init__(ime)

class ravnodušnež(igralec):
    "Pač niso vsi za poker. Ravnodušneža kartanje ne zanima, zato je vsaka njegova poteza popolnoma naključna."
    def __init__(self, ime):
        super().__init__(ime)

class blefer(igralec):
    "Nekateri radi poskušajo pretentati soigralce in pogosto stavijo tudi v primerih, ko jim karte niso naklonjene. Blefer je prav tak."
    def __init__(self, ime):
        super().__init__(ime)

class nespametni_goljuf(igralec):
    """Nespametni goljuf se požvižga na moralo, zato si pogosto ogleduje nasprotnikove karte. \n
    Včasih se mu zgodi, da napačno oceni moč nasprotnikovih kart, saj je prespal učne ure o verjetnosti. """
    def __init__(self, ime):
        super().__init__(ime)

######################################################################################################################
######################################################################################################################

class runda():

    def __init__(self):
        self.dealer = igralec()
        self.small_blind = igralec()
        self.big_blind = igralec()
        self.first_actor = igralec()
        self.stave_so_poravnane = False

    def kdo_je_živ(self, ime_resničnega_igralca):
        igralci = [ime_resničnega_igralca, nespametni_goljuf, ravnodušnež, agresivnež, blefer]
        igralci_v_igri = []
        for igralec in igralci:
            if igralec.žetoni > 0:
                if not igralec.all_in:
                    igralci_v_igri.append(igralec)
        return igralci_v_igri
        #igralci, ki imajo še kaj žetonov

    def kdo_je_v_igri(self, ime_resničnega_igralca):
        return [igralec for igralec in self.kdo_je_živ(ime_resničnega_igralca) if not igralec.fold]
        #igralci, ki še niso foldali

    def spremeni_položaj_igralcev(self, ime_resničnega_igralca):
        igralci_v_igri = self.kdo_je_živ(ime_resničnega_igralca)
        mesto = 0
        self.dealer.položaj.append("dealer")
        pass
        #spremeni kdo je small, big blind, dealer, first actor

    def razdeli_karte(self, ime_resničnega_igralca):
        igralci = [ime_resničnega_igralca, nespametni_goljuf, ravnodušnež, agresivnež, blefer]
        for igralec in igralci:
            if igralec in self.kdo_je_živ(ime_resničnega_igralca):
                deck.deli_karto(igralec, 2)

    def stavi_small_in_big_blind(self, kira_miza, ime_resničnega_igralca):
        for igralec in self.kdo_je_živ(ime_resničnega_igralca):
            if "small blind" in igralec.položaj:
                igralec.žetoni -= kira_miza.small_blind
                kira_miza.pot += kira_miza.small_blind
            elif "big blind" in igralec.položaj:
                igralec.žetoni -= kira_miza.big_blind
                kira_miza.pot += kira_miza.big_blind
    
    def pripni_kombinacije(self, kira_miza, ime_resničnega_igralca):
        igralci = [ime_resničnega_igralca, nespametni_goljuf, ravnodušnež, agresivnež, blefer]
        for igralec in igralci:
            igralec.kombinacija.extend(igralec.lastnosti_kombinacije_igralca(kira_miza))   

    def stave_so_poravnane(self, kira_runda, kira_miza, ime_resničnega_igralca):
        igralci = [ime_resničnega_igralca, nespametni_goljuf, ravnodušnež, agresivnež, blefer]
        stava = 0
        for igralec in igralci:
            stava = max(stava, igralec.žetoni_v_igri)
        for igralec in kira_runda.kdo_je_v_igri(ime_resničnega_igralca):
            if igralec.žetoni_v_igri != stava:
                if not igralec.all_in:
                    self.stave_so_poravnane = True

    def igralec_na_potezi(self):
        pass

    def krog_stav(self):
        while self.stave_so_poravnane == False:
            pass
#ime zavaja, ker ni nujno le en krog, saj se lahko igralci neprestalno višajo - raise
#trenutno nimam boljšega imena  

    def kdo_je_zmagal_rundo(self, ime_resničnega_igralca):
        igralci = [ime_resničnega_igralca, nespametni_goljuf, ravnodušnež, agresivnež, blefer]
        zmagovalci = []
        najboljši_hand = [0,0,0,0,0]
        for igralec in igralci:
            if igralec in self.kdo_je_v_igri(ime_resničnega_igralca):
                if igralec.kombinacija > najboljši_hand:
                    najboljši_hand = igralec.kombinacija
        for igralec in igralci:
            if igralec.kombinacija == najboljši_hand:
                zmagovalci.append(igralec)
        return zmagovalci

                    
        #lahko ni samo en, če pride do situacije, da ima več igralcev kombinacijo 5 istih kart        

class igra():

    def ustvari_igro(self, ime_resničnega_igralca):
        miza = miza()
        deck = deck()
        #ustvari 4 igralce
        nespametni_goljuf = nespametni_goljuf("nespametni_goljuf")
        blefer = blefer("blefer")
        agresivnež = agresivnež("agresivnež")
        ravnodušnež = ravnodušnež("ravnodušnež")
        while ime_resničnega_igralca in self.kdo_je_živ():
            #tu mogoče ne bo self.kdo_je_živ ampak runda.kdo_je_živ, odvisno v kirem razredu definiram to funkcijo
            self.igraj_runde()
    
    def igraj_runde(self):
        pass
    
    def nova_runda(self):
        deck.premešaj_karte()
        #preflop
        self.spremeni_položaj_igralcev()
        self.razdeli_karte()
        izračunaj_verjetnost_zmage()
        #nekaterim se pokaže
        self.stavi_small_in_big_blind()
        self.krog_stav()
        #flop
        deck.deli_karto(kira_miza, 3)
        self.kdo_je_živ()
        self.kdo_je_v_igri()
        izračunaj_verjetnost_zmage()
        self.krog_stav()
        #turn, river
        for i in range(2):
            deck.deli_karto(kira_miza, 1)
            self.kdo_je_živ()
            self.kdo_je_v_igri()
            izračunaj_verjetnost_zmage()
            self.krog_stav()


        self.kdo_je_zmagal_rundo(ime_resničnega_igralca)
        self.razdeli_pot()

        #na koncu runde se morajo igralci znebit nekaterih atributov, npr. fold, kart itd.
        #tu so že zapisane, uporabljene tudi funkcije , ki jih še nisem definiral


#TEST:
miza = miza()
deck = deck()
runda = runda()
deck.premešaj_karte()
janez = igralec("janez")

nespametni_goljuf = nespametni_goljuf("nespametni_goljuf")
blefer = blefer("blefer")
agresivnež = agresivnež("agresivnež")
ravnodušnež = ravnodušnež("ravnodušnež")

print("============")
igrači = [janez, nespametni_goljuf, ravnodušnež, agresivnež, blefer]

runda.razdeli_karte(janez)

##moraš dodat dek. ker je to metoda v classu deck, dek je objekt iz razreda deck
deck.deli_karto(miza, 3)
deck.deli_karto(miza, 1)
deck.deli_karto(miza, 1)
print(miza)
print("============")



runda.pripni_kombinacije(miza, janez)
for i in igrači:
    print(i.kombinacija)

print(runda.kdo_je_zmagal_rundo(janez))
#pri seznamih, slovarjih lahko narediš izpeljane ponekod in prišparaš vrstico ali dve


#Dodane nove funkcije za potek ene runde. Rešil problem dvojne vloge asa: 1,14. Popravljen potek igre.