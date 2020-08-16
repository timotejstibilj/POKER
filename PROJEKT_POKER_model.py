import random
from itertools import combinations 
       
class karta():
    def __init__(self, znak, stevilo):
        self.znak = znak
        self.stevilo = stevilo

    def __repr__(self):
        slovar = {1: "AS", 11: "FANT", 12: "DAMA", 13: "KRALJ"}
        for i in range(2, 11):
            slovar[i] = i
        return "({},{})".format(self.znak, slovar.get(self.stevilo))

class deck(list):
    def __init__(self):
        super().__init__()
        for stevilo in range(1, 14):
            for znak in ["KRIŽ", "PIK", "KARA", "SRCE"]:
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
    
    def __repr__(self):
        return "Karte na mizi so {}".format(self.karte)

class igralec():
    def __init__(self, ime=None):
        self.ime = ime
        self.karte = []
        self.žetoni = 0
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
        return "Igralec {} s kartami {} in {} žetoni.".format(self.ime, self.karte, self.žetoni)

##############################################################
    
    def seznam_kombinacij_kart(self):
        izbira_iz = self.karte + deck.karte_na_mizi()
        #to ni niti malo prav napisano
        return list(combinations(izbira_iz, 5))

    def karte_na_pol(self):
        pass

    def stevilo_pojavitev(self):
        pass

    def kraljeva_lestvica(self):
        pass

    def barvna_lestvica(self):
        pass

    def poker(self):
        pass

    def full_house(self):
        pass

    def barva(self):
        pass

    def lestvica(self):
        pass

    def tris(self):
        pass

    def dva_para(self):
        pass

    def par(self):
        pass

    def visoka_karta(self):
        pass

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

