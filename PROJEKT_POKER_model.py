import random
from itertools import combinations 
from datetime import time
import holdem_calc
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
    def __init__(self, ime="neimenovani igralec"):
        self.ime = ime
        self.karte = []
        self.kombinacija = []
        self.žetoni = 1000
        self.žetoni_v_igri = 0
        self.razlika_za_klicat = 0
        self.fold = False
        self.na_potezi = False
        #tle se mu šteje čas, če je True
        self.čas = "čas"
        self.all_in = False
        self.položaj = []
        self.verjetnost_zmage = 0
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
        self.žetoni_v_igri += koliko

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
        stevila.sort(reverse=True)
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
        return velikosti_preostalih_kart
    
    def lastnosti_kombinacije_igralca(self, kira_miza):
        moč_kombinacije = 0
        velikost_pomembne_karte = 0
        velikosti_preostalih_kart = []
        najmočnejše_kombinacije_brez_najvišje_karte = []
        najmočnejše_kombinacije_z_najvišjo_karto = []
        absolutno_najmočnejša_kombinacija = None
        #kakšna vrsta kombinacije je najvišja: npr.par
        for combination in self.seznam_kombinacij_kart(kira_miza):
            if self.kombinacija_od_peterke(combination) >= moč_kombinacije:
                moč_kombinacije = self.kombinacija_od_peterke(combination)
         #vse take kombinacije, npr.vsi pari
        for combination in self.seznam_kombinacij_kart(kira_miza):
            if self.kombinacija_od_peterke(combination) == moč_kombinacije:
                najmočnejše_kombinacije_brez_najvišje_karte.append(combination)
         #velikost pomembne karte, v paru je to velikost para
        for komb in najmočnejše_kombinacije_brez_najvišje_karte:
            if self.velikost_pomembne_karte(komb) >= velikost_pomembne_karte:
                velikost_pomembne_karte = self.velikost_pomembne_karte(komb)
         #take najvišje kombinacije, ki imajo najvišjo pomembno karto, v paru npr same kombinacije kjer je par ASOV
        for komb in najmočnejše_kombinacije_brez_najvišje_karte:
            if self.velikost_pomembne_karte(komb) == velikost_pomembne_karte:
                najmočnejše_kombinacije_z_najvišjo_karto.append(komb)
        #preveri celotno peterko, npr (AS, AS, KRALJ, DAMA, FANT)
        absolutno_najmočnejša_kombinacija = najmočnejše_kombinacije_z_najvišjo_karto[0]
        for kombinacija in najmočnejše_kombinacije_z_najvišjo_karto:
            if self.velikosti_preostalih_kart(kombinacija) > self.velikosti_preostalih_kart(absolutno_najmočnejša_kombinacija):
                absolutno_najmočnejša_kombinacija = kombinacija          
 
        velikost_pomembne_karte = self.velikost_pomembne_karte(absolutno_najmočnejša_kombinacija)
        velikosti_preostalih_kart = self.velikosti_preostalih_kart(absolutno_najmočnejša_kombinacija)
        kombinacija = [moč_kombinacije, velikost_pomembne_karte, velikosti_preostalih_kart]
        return kombinacija

    def kako_bo_odigral(self):
        #random.choices(population, weights=None, *, cum_weights=None, k=1)
        #s tem lahko na random izbiraš tako da daš eni izbira večjo verjetnost izbire
        pass

####################################################################################################

class kvazi_AI(igralec):
    "kvazi_AI pokaže verjetnosti zmage posameznih igralcev."
    def __init__(self, ime):
        super().__init__(ime)
        
    def zračunaj_verjetnost_zmage_igralca(self):
        holdem_calc.calculate(None, False, 20000, None, ["Ks", "As", "8c", "8d"], False)
        #karte na mizi, točno računanje-true\simulacija-false, število simulacij, datoteka, karte, false
        #prvo vrže tie, pol zmago prvega, pol zmago drugega
        #treba je spremenit imena kart, da jih bo lahko funkcija sprejela

class agresivnež(igralec):
    "Kot ime pove, agresivnež rad poseže globoko v žep in visoko stavi tudi v tveganih situacijah."
    def __init__(self, ime):
        super().__init__(ime)
        self.bo_stavil = False
        self.bo_checkal = False
        self.bo_foldal = False

class ravnodušnež(igralec):
    "Pač niso vsi za poker. Ravnodušneža kartanje ne zanima, zato je vsaka njegova poteza popolnoma naključna."
    def __init__(self, ime):
        super().__init__(ime)
        self.bo_stavil = False
        self.bo_checkal = False
        self.bo_foldal = False

class blefer(igralec):
    "Nekateri radi poskušajo pretentati soigralce in pogosto stavijo tudi v primerih, ko jim karte niso naklonjene. Blefer je prav tak."
    def __init__(self, ime):
        super().__init__(ime)
        self.bo_stavil = False
        self.bo_checkal = False
        self.bo_foldal = False

class nespametni_goljuf(igralec):
    """Nespametni goljuf se požvižga na moralo, zato si pogosto ogleduje nasprotnikove karte. \n
    Včasih se mu zgodi, da napačno oceni moč nasprotnikovih kart, saj je prespal učne ure o verjetnosti. """
    def __init__(self, ime):
        super().__init__(ime)
        self.bo_stavil = False
        self.bo_checkal = False
        self.bo_foldal = False

######################################################################################################################
######################################################################################################################

class runda():

    def __init__(self):
        self.dealer = igralec()
        self.small_blind = igralec()
        self.big_blind = igralec()
        self.first_actor = igralec()
        self.stave_so_poravnane = False
        #self.deck = deck()

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
        igralci = [ime_resničnega_igralca, nespametni_goljuf, ravnodušnež, agresivnež, blefer]
        igralci_z_novim_položajem = {}
        položaji = ["dealer", "small blind", "big blind", "first actor"]
        for i in range(5):
            for položaj in položaji:
                if položaj in igralci[i].položaj:
                    for j in range(1, 4):
                        if igralci[(i + j) % 5] in runda.kdo_je_živ(ime_resničnega_igralca):
                            if igralci[(i + j) % 5] in igralci_z_novim_položajem:
                                igralci_z_novim_položajem[igralci[(i + j) % 5]].append(položaj)
                            else:
                                igralci_z_novim_položajem[igralci[(i + j) % 5]] = položaj
                            break
        for igralec in igralci:
            igralec.položaj.clear()
        for igralec in igralci_z_novim_položajem.keys():
            igralec.položaj.append(igralci_z_novim_položajem[igralec])
            
        #spremeni kdo je small, big blind, dealer, first actor

    def razdeli_karte(self, ime_resničnega_igralca):
        igralci = [ime_resničnega_igralca, nespametni_goljuf, ravnodušnež, agresivnež, blefer]
        small_blind = False
        for igralec in igralci:
            if igralec in self.kdo_je_živ(ime_resničnega_igralca):
                if "small blind" in igralec.položaj:
                    small_blind = True
                if small_blind:
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
        igralci = [ime_resničnega_igralca, nespametni_goljuf, ravnodušnež, agresivnež, blefer]
        for igralec in igralci:
            pass
        #mora bit odvisno od odštevalnika 

    def krog_stav(self):
        while self.stave_so_poravnane == False:
            pass
#ime zavaja, ker ni nujno le en krog, saj se lahko igralci neprestalno višajo - raise
#trenutno nimam boljšega imena  

    def kdo_je_zmagal_rundo(self, ime_resničnega_igralca):
        igralci = self.kdo_je_v_igri(ime_resničnega_igralca)
        zmagovalci = []
        najboljši_hand = [0,0,0,0,0]
        for igralec in igralci:
            if igralec.kombinacija > najboljši_hand:
                najboljši_hand = igralec.kombinacija
        for igralec in igralci:
            if igralec.kombinacija == najboljši_hand:
                zmagovalci.append(igralec)
        for zmagovalec in zmagovalci:
            zmagovalec.zmaga = True    
        #lahko ni samo en, če pride do situacije, da ima več igralcev kombinacijo 5 istih kart   

    def make_side_pots(self, ime_resničnega_igralca):
        igralci = [ime_resničnega_igralca, nespametni_goljuf, ravnodušnež, agresivnež, blefer]
        stave_igralcev = set()
        side_pots = {}
        for igralec in igralci:
            stave_igralcev.add(igralec.žetoni_v_igri)
        #naraščajoče stave vseh igralcev so to spodi
        stave_igralcev = list(stave_igralcev)
        stave_igralcev.sort()

        stanje_stav = stave_igralcev
        #v tem bodo odšteti deli stav, ki pripadajo prejšnjem side pot-u
        for i in range(len(stave_igralcev)):
            side_pots[stave_igralcev[i]] = len(igralci) * stanje_stav[i]
            #side pot je odvisen od števila igralcev, ki še "pokrijejo to stavo" (to so igralci v seznamu igralci)
            #in odvisen je še od velikosti stave, os katere je odšteta vrednost prejšnjega stanja stave
            #stanje stave se zmanjša, ko se en del stave dodeli side potu za drugega igralca, z manj žetoni
            #side poti so dodeljeni začetnim žetonom v igri in ne igralcem
            #to niso še pravi side poti, ker moraš preverit še kdo je zmagal in posledično pobral svoj pot
            #če zmaga, pobere svoj side_pot in vse manjše side pote
            igralci_s_tako_stavo = []
            for igralec in igralci:
                if igralec.žetoni_v_igri == stave_igralcev[i]:
                    igralci_s_tako_stavo.append(igralec)
            for igralec in igralci_s_tako_stavo:
                igralci.remove(igralec)
            stanje_stav = list(map(lambda x:x-stanje_stav[i], stanje_stav))
            #spremeni stanje stav tako da odšteje del stave, ki se dodeli prejšnjemu side potu
        return side_pots

    def razdeli_pot(self, ime_resničnega_igralca):
        igralci = self.kdo_je_v_igri(ime_resničnega_igralca)
        side_pots = self.make_side_pots(ime_resničnega_igralca)
        for igralec in igralci:
            if igralec.zmaga:
                pass
        #treba je še upoštevat, da tisti ki zmaga ne nujno pobere vsega, če je all_in in so drugi stavli še dalje


    def počisti_rundo(self, ime_resničnega_igralca):
        igralci = [ime_resničnega_igralca, nespametni_goljuf, ravnodušnež, agresivnež, blefer]
        for igralec in igralci:
            igralec.karte.clear()
            igralec.kombinacija.clear()
            igralec.žetoni_v_igri = 0
            igralec.razlika_za_klicat = 0
            igralec.fold = False
            igralec.na_potezi = False
            igralec.čas = "čas"
            igralec.all_in = False
            igralec.zmaga = False
        miza.karte.clear()
        miza.pot = 0
        #self.deck = deck()
        #položaj pustiš pri miru, ker ga ureja že funkcija spremeni_položaj_igralcev
    
    def nova_runda(self):
        deck.premešaj_karte()
        #preflop
        self.spremeni_položaj_igralcev(janez)

        self.počisti_rundo()

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

        #tu so že zapisane, uporabljene tudi funkcije, ki jih še nisem definiral

class igra():

    def ustvari_igro(self, ime_resničnega_igralca):
        miza = miza()
        deck = deck()
        runda = runda()
        #ustvari 4 igralce
        nespametni_goljuf = nespametni_goljuf("nespametni_goljuf")
        blefer = blefer("blefer")
        agresivnež = agresivnež("agresivnež")
        ravnodušnež = ravnodušnež("ravnodušnež")
        #vzpostavi začetni položaj igralcev
        ime_resničnega_igralca.položaj.append("dealer")
        nespametni_goljuf.položaj.append("small blind")
        ravnodušnež.položaj.append("big blind")
        while ime_resničnega_igralca in self.kdo_je_živ():
            runda.kdo_je_živ()
            self.igraj_runde()
    
    def igraj_runde(self):
        pass


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
janez.položaj.append("small blind")
nespametni_goljuf.položaj.append("big blind")
blefer.položaj.append("dealer")
runda.razdeli_karte(janez)

#moraš dodat dek. ker je to metoda v classu deck, dek je objekt iz razreda deck
deck.deli_karto(miza, 3)
deck.deli_karto(miza, 1)
deck.deli_karto(miza, 1)
print(miza)
print("============")

runda.pripni_kombinacije(miza, janez)
runda.kdo_je_zmagal_rundo(janez)
for i in igrači:
    print(i)
    print(i.kombinacija)
    print(i.zmaga)
janez.stavi(10, miza)
ravnodušnež.stavi(20, miza)
blefer.stavi(100, miza)
blefer.folda()
nespametni_goljuf.stavi(100, miza)
agresivnež.stavi(150, miza)

print(runda.make_side_pots(janez))
#pri seznamih, slovarjih lahko narediš izpeljane ponekod in prišparaš vrstico ali dve


#na začetku daš resničnega igralca na pozicijo dealerja

#v vmesniku bi lahko bil tudi hand history kot v chatu