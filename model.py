import random
from itertools import combinations
import holdem_calc
import math

################################################################################################


def spremeni_zapis_kart():
    """Vrne zapis kart primeren za računanje verjetnosti s holdem_calc."""
    dek = Deck()
    slovar_kart = {}
    slovar_znakcev = {0: "c", 1: "s", 2: "h", 3: "d"}
    slovar_stevilk = {10: "T", 11: "J", 12: "Q", 13: "K", 14: "A"}
    # znaki so club, spade, heart, diamond
    # stevila so ten, jack, queen, king in ace
    slovar_stevilk.update({i: str(i) for i in range(2, 10)})
    for karta in dek:
        slovar_kart[karta] = slovar_stevilk.get(karta.stevilo) + slovar_znakcev.get(karta.znak)
    return slovar_kart


##################################################################################################


class Karta:
    def __init__(self, znak, stevilo):
        self.znak = znak
        self.stevilo = stevilo

    def __repr__(self):

        slovar_stevil = {11: "'FANT'", 12: "'DAMA'", 13: "'KRALJ'", 14: "'AS'"}
        slovar_stevil.update({i: i for i in range(2, 11)})
        znakci = {0: "'križ'", 1: "'pik'", 2: "'srce'", 3: "'kara'"}
        return "({},{})".format(znakci.get(self.znak), slovar_stevil.get(self.stevilo))

    def __eq__(self, other):
        return self.znak == other.znak and self.stevilo == other.stevilo

    def __hash__(self):
        return hash((self.znak, self.stevilo))

    # naslednje 3 funkcije so za uporabo v html-ju
    def povej_barvo_karte(self):
        if self.znak == 0 or self.znak == 1:
            return "black"
        else:
            return "red"

    def povej_znak_karte(self):
        if self.znak == 0:
            return "clubs"
        elif self.znak == 1:
            return "spades"
        elif self.znak == 2:
            return "hearts"
        else:
            return "diams"

    def povej_število_karte(self):
        števila = {11: "J", 12: "Q", 13: "K", 14: "A"}
        return števila.get(self.stevilo, self.stevilo)


class Deck(list):
    def __init__(self):
        super().__init__()
        for stevilo in range(2, 15):
            for znak in range(4):
                self.append(Karta(znak, stevilo))

        random.shuffle(self)

    def deli_karto(self, komu, koliko_kart):
        """za deljenje bodisi na mizo bodisi igralcem"""
        if koliko_kart == 0:
            return
        for i in range(koliko_kart):
            komu.karte.append(self.pop(0))


class Miza:
    def __init__(self):
        self.karte = []
        self.pot = 0
        self.small_blind = 10
        self.big_blind = 20

    def __repr__(self):
        return "Karte na mizi so {}".format(self.karte)


class Igralec:
    def __init__(self, ime="neimenovani igralec"):
        self.ime = ime
        self.karte = []
        self.kombinacija = []
        self.žetoni = 1000
        self.žetoni_v_igri = 0
        self.razlika_za_klicat = 0
        self.fold = False
        self.check = False
        self.all_in = False
        self.položaj = []
        self.verjetnost_zmage = 0
        self.zmaga = False
        self.je_bil_na_potezi = False

    def __repr__(self):
        ime = self.ime
        return ime

    ##############################################################

    def zračunaj_verjetnost_zmage(self):
        """Izračuna približno verjetnost zmage igralca s pomočjo simulacije."""
        karti_igralca = self.karte
        karta_1 = spremeni_zapis_kart().get(karti_igralca[0])
        karta_2 = spremeni_zapis_kart().get(karti_igralca[1])
        holdem = holdem_calc.calculate(None, False, 5, None, [karta_1, karta_2, "?", "?"], False)
        return holdem[1]
        # karte na mizi, točno računanje-true\simulacija-false, število simulacij, datoteka, karte, false
        # prvo vrže tie, potem zmago prvega, potem zmago drugega

    ##############################################################

    def folda(self):
        self.fold = True

    ##############################################################

    def seznam_kombinacij_kart(self, kira_miza):
        if kira_miza.karte == []:
            # umetno narejen seznam, ki ga potrebujemo takrat, ko flop-a še ni na mizi, vendar že imamo zmagovalca
            izbira_iz = 3 * self.karte
        else:
            izbira_iz = self.karte + kira_miza.karte
        return list(combinations(izbira_iz, 5))

    def karte_na_pol_od_peterke(self, peterka):
        """Razdeli karte na znake in stevila."""
        znaki = []
        stevila = []
        for karta in peterka:
            znaki.append(karta.znak)
            stevila.append(karta.stevilo)
        stevila.sort(reverse=True)
        return [znaki, stevila]

    def max_stevilo_pojavitev_v_peterki(self, peterka):
        max = 0
        stevila = self.karte_na_pol_od_peterke(peterka)[1]
        for i in range(2, 15):
            if stevila.count(i) > max:
                max = stevila.count(i)
        return max

    # hand-i definirani za izbrano peterko in ne še najboljši hand igralca
    def barvna_lestvica(self, peterka):
        return self.barva(peterka) and self.lestvica(peterka)

    def poker(self, peterka):
        return self.max_stevilo_pojavitev_v_peterki(peterka) == 4

    def full_house(self, peterka):
        return self.tris(peterka) and len(set(self.velikosti_preostalih_kart(peterka))) == 1

    def barva(self, peterka):
        return len(set(self.karte_na_pol_od_peterke(peterka)[0])) == 1

    def lestvica(self, peterka):
        stevilke = self.karte_na_pol_od_peterke(peterka)[1]
        if sorted(stevilke) == list(range(min(stevilke), max(stevilke) + 1)):
            return True
        elif sorted(stevilke) == [2, 3, 4, 5, 14]:
            return True
            # ker je AS reprezentiran s 14, ampak je lahko tudi v vlogi 1
        return False

    def tris(self, peterka):
        return self.max_stevilo_pojavitev_v_peterki(peterka) == 3

    def dva_para(self, peterka):
        druge_karte = {stevilo for stevilo in self.velikosti_preostalih_kart(peterka)}
        return self.max_stevilo_pojavitev_v_peterki(peterka) == 2 and len(druge_karte) == 2

    def par(self, peterka):
        return self.max_stevilo_pojavitev_v_peterki(peterka) == 2

    def kombinacija_od_peterke(self, peterka):
        """Vrne najmočnejši hand-kombinacijo dane peterke."""
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
        """Vrne velikost karte, ki ima glavno vlogo v kombinaciji, npr. pri trisu vrne velikost karte iz trisa."""
        velikost_pomembne_karte = 0
        stevila = self.karte_na_pol_od_peterke(peterka)[1]
        for i in range(2, 15):
            if stevila.count(i) == self.max_stevilo_pojavitev_v_peterki(peterka) and i > velikost_pomembne_karte:
                velikost_pomembne_karte = i
        return velikost_pomembne_karte

    def velikosti_preostalih_kart(self, peterka):
        stevila = self.karte_na_pol_od_peterke(peterka)[1]
        return [stevilo for stevilo in stevila if stevilo != self.velikost_pomembne_karte(peterka)]

    def lastnosti_kombinacije_igralca(self, kira_miza):
        """Vsakemu igralcu dodeli njegovo najboljšo kombinacijo."""
        moč_kombinacije = 0
        velikost_pomembne_karte = 0
        velikosti_preostalih_kart = []
        najmočnejše_kombinacije_brez_najvišje_karte = []
        najmočnejše_kombinacije_z_najvišjo_karto = []
        absolutno_najmočnejša_kombinacija = None
        # kakšna vrsta kombinacije je najvišja: npr.par
        for combination in self.seznam_kombinacij_kart(kira_miza):
            if self.kombinacija_od_peterke(combination) >= moč_kombinacije:
                moč_kombinacije = self.kombinacija_od_peterke(combination)
        # vse take kombinacije, npr.vsi pari
        for combination in self.seznam_kombinacij_kart(kira_miza):
            if self.kombinacija_od_peterke(combination) == moč_kombinacije:
                najmočnejše_kombinacije_brez_najvišje_karte.append(combination)
        # velikost pomembne karte, v paru je to velikost para
        for komb in najmočnejše_kombinacije_brez_najvišje_karte:
            if self.velikost_pomembne_karte(komb) >= velikost_pomembne_karte:
                velikost_pomembne_karte = self.velikost_pomembne_karte(komb)
        # take najvišje kombinacije, ki imajo najvišjo pomembno karto, v paru npr same kombinacije kjer je par ASOV
        for komb in najmočnejše_kombinacije_brez_najvišje_karte:
            if self.velikost_pomembne_karte(komb) == velikost_pomembne_karte:
                najmočnejše_kombinacije_z_najvišjo_karto.append(komb)
        # preveri celotno peterko, npr (AS, AS, KRALJ, DAMA, FANT)
        absolutno_najmočnejša_kombinacija = najmočnejše_kombinacije_z_najvišjo_karto[0]
        for kombinacija in najmočnejše_kombinacije_z_najvišjo_karto:
            if self.velikosti_preostalih_kart(kombinacija) > self.velikosti_preostalih_kart(absolutno_najmočnejša_kombinacija):
                absolutno_najmočnejša_kombinacija = kombinacija

        velikost_pomembne_karte = self.velikost_pomembne_karte(absolutno_najmočnejša_kombinacija)
        velikosti_preostalih_kart = self.velikosti_preostalih_kart(absolutno_najmočnejša_kombinacija)
        kombinacija = [
            moč_kombinacije,
            velikost_pomembne_karte,
            velikosti_preostalih_kart,
        ]
        return kombinacija

    def ponastavi_raise_in_call(self):
        self.bo_raisal = False
        self.bo_callal = False


####################################################################################################

# na koncu vsake runde moraš ponastavit te atribute, kako bodo igrali
class Agresivnež(Igralec):
    "Kot ime pove, agresivnež rad poseže globoko v žep in visoko stavi."

    def __init__(self, ime):
        super().__init__(ime)
        self.bo_raisal = False
        self.koliko_bo_raisal = 0
        self.bo_callal = False
        self.žetoni = 1020

    def kako_igra(self, stevilo_potez):
        self.ponastavi_raise_in_call()
        verjetnost_zmage = self.zračunaj_verjetnost_zmage()
        # to je približna verjetnost, če bi igral samo z enim nasprotnikom

        if stevilo_potez > 7:
            # če je manjša verjetnost je raise in call ni težav, saj je raise, call apriori nastavljen na false
            if verjetnost_zmage > 0.60 and verjetnost_zmage <= 0.80:
                if self.razlika_za_klicat > 0:
                    self.bo_raisal = bool(random.choices([True, False], [1, 65], k=1))
                    self.bo_callal = bool(random.choices([True, False], [7, 1], k=1))
                    self.koliko_bo_raisal = math.floor(14 / random.choice(list(range(7, 12))) * self.razlika_za_klicat)
                else:
                    self.bo_raisal = bool(random.choices([True, False], [1, 40], k=1))
                    self.koliko_bo_raisal = math.floor(3 / random.choice(list(range(8, 12))) * self.žetoni)
            elif verjetnost_zmage > 0.80:
                self.bo_raisal = bool(random.choices([True, False], [1, 10], k=1))
                self.bo_callal = True
                if self.razlika_za_klicat > 0:
                    self.koliko_bo_raisal = random.choice(list(range(2, 4))) * self.razlika_za_klicat
                else:
                    self.koliko_bo_raisal = math.floor(1 / random.choice(list(range(1, 10))) * self.žetoni)
                self.bo_raisal = True
        else:
            if verjetnost_zmage <= 0.60 and verjetnost_zmage > 0.40:
                if self.razlika_za_klicat < (self.žetoni / 3):
                    self.bo_callal = bool(random.choices([True, False], [1, 10], k=1))
            elif verjetnost_zmage > 0.60 and verjetnost_zmage <= 0.70:
                self.bo_raisal = bool(random.choices([True, False], [3, 11], k=1))
                self.bo_callal = bool(random.choices([True, False], [5, 1], k=1))
                if self.razlika_za_klicat > 0:
                    self.koliko_bo_raisal = math.floor(8 / random.choice(list(range(4, 7))) * self.razlika_za_klicat)
                else:
                    self.koliko_bo_raisal = math.floor(1 / random.choice(list(range(8, 15))) * self.žetoni)
            elif verjetnost_zmage > 0.70 and verjetnost_zmage < 0.85:
                self.bo_raisal = bool(random.choices([True, False], [7, 2], k=1))
                self.bo_callal = True
                if self.razlika_za_klicat > 0:
                    self.koliko_bo_raisal = random.choice(list(range(1, 6))) * self.razlika_za_klicat
                else:
                    self.koliko_bo_raisal = math.floor(1 / random.choice(list(range(1, 5))) * self.žetoni)
            elif verjetnost_zmage > 0.85:
                self.bo_raisal = True
                self.bo_callal = True
                self.koliko_bo_raisal = self.žetoni


class Ravnodušnež(Igralec):
    "Pač niso vsi za poker. Ravnodušneža kartanje ne zanima, zato je vsaka njegova poteza naključna."

    def __init__(self, ime):
        super().__init__(ime)
        self.bo_raisal = False
        self.koliko_bo_raisal = 0
        self.bo_callal = False

    def kako_igra(self, stevilo_potez):
        # Igra je nastavljena na skorajda naključno, vendar vseeno tako, da ne viša stav prepogosto.

        self.ponastavi_raise_in_call()
        self.bo_callal = random.choice([True, False])
        if stevilo_potez < 7:
            self.bo_raisal = random.choice([True, False])
            if self.razlika_za_klicat > 0:
                self.koliko_bo_raisal = math.floor(25 / random.choice(list(range(15, 24))) * self.razlika_za_klicat)
            else:
                self.koliko_bo_raisal = math.floor(4 / random.choice(list(range(4, 30))) * self.žetoni)


class Blefer(Igralec):
    "Nekateri radi poskušajo pretentati soigralce in pogosto stavijo v primerih, ko jim karte niso naklonjene. Blefer je prav tak."

    def __init__(self, ime):
        super().__init__(ime)
        self.bo_raisal = False
        self.koliko_bo_raisal = 0
        self.bo_callal = False
        self.žetoni = 1010

    def kako_igra(self, stevilo_potez):
        self.ponastavi_raise_in_call()
        verjetnost_zmage = self.zračunaj_verjetnost_zmage()
        # to je približna verjetnost, če bi igral samo z enim nasprotnikom

        if stevilo_potez >= 7:
            # če je manjša verjetnost je raise in call itak false in check, fold pa True
            if verjetnost_zmage < 0.45:
                self.bo_raisal = bool(random.choices([True, False], [1, 40], k=1))
                self.koliko_bo_raisal = self.žetoni
            elif verjetnost_zmage > 0.45 and verjetnost_zmage <= 0.65:
                self.bo_callal = bool(random.choices([True, False], [4, 3], k=1))
            elif verjetnost_zmage > 0.65:
                self.bo_callal = bool(random.choices([True, False], [5, 1]))
        else:
            if verjetnost_zmage <= 0.45 and verjetnost_zmage > 0.35:
                if self.razlika_za_klicat < (self.žetoni / 10):
                    if self.razlika_za_klicat > 0:
                        self.bo_raisal = bool(random.choices([True, False], [1, 25], k=1))
                        self.koliko_bo_raisal = random.choices(
                            [self.razlika_za_klicat * 3, self.razlika_za_klicat * 5, self.žetoni], [30, 17, 1], k=1
                        ).pop()
                    else:
                        self.bo_raisal = bool(random.choices([True, False], [1, 5], k=1))
                        self.koliko_bo_raisal = math.floor(3 / random.choice(list(range(8, 12))) * self.žetoni)
            elif verjetnost_zmage > 0.45 and verjetnost_zmage <= 0.65:
                self.bo_callal = bool(random.choice([True, False]))
                if self.razlika_za_klicat == 0:
                    self.bo_raisal = bool(random.choices([True, False], [2, 3], k=1))
                    self.koliko_bo_raisal = math.floor(3 / random.choice(list(range(3, 7))) * self.žetoni)
            elif verjetnost_zmage > 0.65:
                self.bo_raisal = bool(random.choice([True, False]))
                self.bo_callal = True
                if self.razlika_za_klicat > 0:
                    self.koliko_bo_raisal = random.choices([self.razlika_za_klicat * 2, self.razlika_za_klicat * 5], [3, 1], k=1).pop()
                else:
                    self.koliko_bo_raisal = math.floor(3 / random.choice(list(range(3, 7))) * self.žetoni)


class NespametniGoljuf(Igralec):
    """Nespametni goljuf se požvižga na moralo, zato si pogosto ogleduje nasprotnikove karte.
    Pri igranju vedno izkorišče izračunano verjetnost zmag igralcev, vendar se včasih kljub dobri verjetnosti nespametno odloči, da odloži karte."""

    def __init__(self, ime, kira_igra):
        super().__init__(ime)
        self.bo_raisal = False
        self.bo_callal = False
        self.koliko_bo_raisal = 0
        self.igra = kira_igra

    def ima_najboljše_karte(self):
        verjetnosti = []
        for igralec in self.igra.igralci:
            verjetnosti.append(igralec.zračunaj_verjetnost_zmage())
        return max(verjetnosti) == self.zračunaj_verjetnost_zmage()

    def kako_igra(self, stevilo_potez):
        self.ponastavi_raise_in_call()
        verjetnost_zmage = self.zračunaj_verjetnost_zmage()
        # to je približna verjetnost, če bi igral samo z enim nasprotnikom

        if self.ima_najboljše_karte():
            self.bo_raisal = bool(random.choices([True, False], [7, 2], k=1))
            self.bo_callal = True
            if self.razlika_za_klicat > 0:
                self.koliko_bo_raisal = random.choices(
                    [self.razlika_za_klicat * 2, self.razlika_za_klicat * 4, self.razlika_za_klicat * 5],
                    [3, 1, 1],
                    k=1,
                ).pop()
            else:
                self.koliko_bo_raisal = math.floor(3 / random.choice(list(range(6, 10))) * self.žetoni)
        else:
            if verjetnost_zmage < 0.50 and verjetnost_zmage > 0.25:
                if self.razlika_za_klicat < self.žetoni // 10:
                    self.bo_callal = bool(random.choices([True, False], [5, 11], k=1))
                else:
                    self.bo_callal = bool(random.choices([True, False], [1, 18], k=1))
            elif verjetnost_zmage < 0.65 and verjetnost_zmage >= 0.50:
                self.bo_callal = bool(random.choices([True, False], [5, 1], k=1))
                if self.razlika_za_klicat > 0 and stevilo_potez < 10:
                    self.koliko_bo_raisal = math.floor(
                        random.choices(
                            [
                                self.razlika_za_klicat * 2,
                                self.razlika_za_klicat * 3,
                                self.razlika_za_klicat * 1.4,
                            ],
                            [3, 1, 2],
                            k=1,
                        ).pop()
                    )
                    self.bo_raisal = bool(random.choices([True, False], [2, 11], k=1))
            elif verjetnost_zmage >= 0.65:
                self.bo_callal = True
                if stevilo_potez < 10:
                    self.bo_raisal = bool(random.choices([True, False], [5, 3], k=1))
                if self.razlika_za_klicat > 0:
                    self.koliko_bo_raisal = random.choice(list(range(1, 5))) * self.razlika_za_klicat
                else:
                    self.koliko_bo_raisal = math.floor(3 / random.choice(list(range(3, 10))) * self.žetoni)


######################################################################################################################


class Runda:
    def __init__(self, igralci):
        if len(igralci) < 1:
            raise ValueError("Poker je igra za dva ali več igralcev. Igraj pasijanso.")

        self.igralci = igralci

        self.možni_deli_igre = iter(["preflop", "flop", "turn", "river", "konec", "nova"])
        self.kje_smo_v_igri = next(self.možni_deli_igre)

        self.stevilo_potez = 0

        for i, igralec in enumerate(self.igralci):
            if type(igralec) == Igralec:
                break

        self.igralec_resnicni = i

        # Ničti iz seznama igralcev bo dealer in bo prvi na potezi.
        self.igralec_na_potezi = 0

        # Ob začetku vsake runde ponastavimo nekatere atribute.
        for igralec in self.igralci:
            igralec.karte.clear()
            igralec.kombinacija.clear()
            igralec.žetoni_v_igri = 0

            igralec.razlika_za_klicat = 0
            igralec.fold = False
            igralec.all_in = False
            igralec.zmaga = False
            igralec.verjetnost_zmage = 0
            igralec.je_bil_na_potezi = False

        self.miza = Miza()
        self.deck = Deck()

        self.razdeli_karte()
        self.stavi_small_in_big_blind()

    #####################################################################################################################

    def kdo_je_živ(self):
        """Igralci, ki imajo še kaj žetonov"""
        for igralec in self.igralci:
            if igralec.žetoni > 0 or igralec.all_in:
                yield igralec

    def kdo_je_v_igri(self):
        """Igralci, ki še niso foldali"""
        return [igralec for igralec in self.kdo_je_živ() if not igralec.fold]

    def razdeli_karte(self):
        """Razdeli karte začenši z igralcem na small blind-u."""
        igralci_po_vrsti = self.igralci[1:] + [self.igralci[0]]
        # igralec s small blindom je na 1. mestu, takoj za dealerjem, ki je vedno na 0-tem mestu.
        for igralec in igralci_po_vrsti:
            self.deck.deli_karto(igralec, 2)

    def naslednji_na_potezi(self):
        """Nastavi igralca na potezi na prvega igralca v krogu, ki sedi po trenutnem igralcu na potezi."""
        # če so vsi v igri, da naslednjega
        self.igralec_na_potezi = (self.igralec_na_potezi + 1) % len(self.igralci)
        igralec = self.igralci[self.igralec_na_potezi]
        self.pokaži_razlike_za_klicat()
        # če niso vsi v igri pa se pomika dalje po seznamu
        if self.stave_so_poravnane() and (self.imamo_predcasnega_zmagovalca() or self.predcasno_zakljucena_runda()):
            return
        primerni_igralci = [igralec for igralec in self.kdo_je_v_igri() if not igralec.all_in]
        while igralec not in primerni_igralci:
            self.igralec_na_potezi = (self.igralec_na_potezi + 1) % len(self.igralci)
            igralec = self.igralci[self.igralec_na_potezi]

        return igralec

    def stavi_small_in_big_blind(self):
        igralec = self.naslednji_na_potezi()
        if self.miza.small_blind > igralec.žetoni:
            self.miza.pot += igralec.žetoni
            igralec.žetoni_v_igri = igralec.žetoni
            igralec.all_in = True
            igralec.žetoni = 0

        else:
            self.miza.pot += self.miza.small_blind
            igralec.žetoni_v_igri += self.miza.small_blind
            igralec.žetoni -= self.miza.small_blind

        igralec = self.naslednji_na_potezi()
        if igralec.žetoni < self.miza.big_blind:
            self.miza.pot += igralec.žetoni
            igralec.žetoni_v_igri = igralec.žetoni
            igralec.all_in = True
            igralec.žetoni = 0
        else:
            self.miza.pot += self.miza.big_blind
            igralec.žetoni_v_igri += self.miza.big_blind
            igralec.žetoni -= self.miza.big_blind
        self.naslednji_na_potezi()

    def pripni_kombinacije(self, kira_miza):
        for igralec in self.igralci:
            igralec.kombinacija.extend(igralec.lastnosti_kombinacije_igralca(kira_miza))

    def stave_so_poravnane(self):
        stava = 0
        for igralec in self.kdo_je_v_igri():
            stava = max(stava, igralec.žetoni_v_igri)
            # če niso še vsi bili na potezi, stave niso poravnane.
            # Na začetku vsakega dela igre(preflop, flop, turn, river) se atribut .je_bil_na_potezi nastavi na False.
            if not igralec.je_bil_na_potezi and not igralec.all_in:
                return False

        for igralec in self.kdo_je_v_igri():
            if igralec.žetoni_v_igri != stava and not igralec.all_in:
                return False
        return True

    def imamo_predcasnega_zmagovalca(self):
        return len(self.kdo_je_v_igri()) == 1

    def predcasno_zakljucena_runda(self):
        """Pove ali sta v igri vsaj dva igralca, s še kaj žetoni - taka igralca, ki še lahko stavita ali so že vsi all in."""
        for igralec in self.kdo_je_v_igri():
            if not igralec.je_bil_na_potezi and not igralec.all_in:
                return False
        igralci_all_in = [igralec for igralec in self.kdo_je_v_igri() if igralec.all_in]
        return len(igralci_all_in) == len(self.kdo_je_v_igri()) or len(igralci_all_in) == (len(self.kdo_je_v_igri()) - 1)

    def pojdi_v_naslednji_krog(self):
        igralec_s_small_blindom = self.igralci[1]

        if self.stave_so_poravnane():
            # če so stave poravnane, se začne nov del igre
            self.stevilo_potez = 0
            self.igralec_na_potezi = 1
            if igralec_s_small_blindom not in self.kdo_je_v_igri() or igralec_s_small_blindom.all_in:
                self.naslednji_na_potezi()
            # nastavimo tako, da bo nov del igre začel igralec s small blindom, če je še v igri
            for i in self.igralci:
                i.je_bil_na_potezi = False
                i.razlika_za_klicat = 0
                i.check = False
            self.kje_smo_v_igri = next(self.možni_deli_igre)
            return True
        return False

    def pokaži_razlike_za_klicat(self):
        """Vsakemu igralcu pripne vrednost, ki jo mora klicati, če želi ostati v igri."""
        največja_količina_žetonov_v_igri = 0
        for igralec in self.igralci:
            največja_količina_žetonov_v_igri = max(največja_količina_žetonov_v_igri, igralec.žetoni_v_igri)
        for igralec in self.kdo_je_živ():
            if največja_količina_žetonov_v_igri >= igralec.žetoni_v_igri:
                igralec.razlika_za_klicat = največja_količina_žetonov_v_igri - igralec.žetoni_v_igri

    def igralec_na_potezi_stavi(self, vrednost):
        igralec = self.igralci[self.igralec_na_potezi]

        if igralec.žetoni > vrednost:
            igralec.žetoni -= vrednost
            self.miza.pot += vrednost
            igralec.žetoni_v_igri += vrednost
        else:
            igralec.žetoni_v_igri += igralec.žetoni
            self.miza.pot += igralec.žetoni
            igralec.žetoni = 0
            igralec.all_in = True

    def vprasaj_racunalnik_za_potezo(self):
        """Odigra potezo računalniškega igralca."""
        igralec = self.igralci[self.igralec_na_potezi]
        self.pokaži_razlike_za_klicat()
        igralec.kako_igra(self.stevilo_potez)
        igralec.je_bil_na_potezi = True
        if igralec.fold:
            return
        if igralec.razlika_za_klicat > 0:
            if igralec.bo_raisal:
                if igralec.koliko_bo_raisal < igralec.žetoni:
                    self.igralec_na_potezi_stavi(igralec.koliko_bo_raisal)
                else:
                    self.igralec_na_potezi_stavi(igralec.žetoni)
                    igralec.all_in = True

            elif igralec.bo_callal:
                if igralec.razlika_za_klicat >= igralec.žetoni:
                    self.igralec_na_potezi_stavi(igralec.žetoni)
                    igralec.all_in = True
                else:
                    self.igralec_na_potezi_stavi(igralec.razlika_za_klicat)
            else:
                igralec.folda()
        else:
            if igralec.bo_raisal:
                if igralec.koliko_bo_raisal < igralec.žetoni:
                    self.igralec_na_potezi_stavi(igralec.koliko_bo_raisal)
                else:
                    self.igralec_na_potezi_stavi(igralec.žetoni)
                    igralec.all_in = True
            else:
                igralec.check = True

    def kdo_je_zmagal_rundo(self, kiri_igralci):
        """Pokaže kateri igralci imajo najboljšo kombinacijo. Izbira med igralci, ki jih podamo (ne nujno med vsemi)."""
        igralci = kiri_igralci
        najboljši_hand = [0, 0, 0, 0, 0]
        for igralec in igralci:
            if igralec.kombinacija > najboljši_hand:
                najboljši_hand = igralec.kombinacija
        for igralec in igralci:
            if igralec.kombinacija == najboljši_hand:
                igralec.zmaga = True
        # lahko ni samo en, če pride do situacije, da ima več igralcev kombinacijo 5 istih kart
        # če ni side_potov --> kiri_igralci = self.kdo_je_v_igri()

    def kdo_je_glavni_zmagovalec(self):
        self.kdo_je_zmagal_rundo(self.kdo_je_v_igri())
        sez = [igralec.ime for igralec in self.igralci if igralec.zmaga]
        return self.vrni_niz(sez) + ", ".join(sez)

    def vrni_niz(self, seznam):
        rezultat = ""
        if len(seznam) == 1:
            rezultat = "Zmagal/a je "
        elif len(seznam) == 2:
            rezultat = "Zmagovalca sta "
        else:
            rezultat = "Zmagovalci so "

        return rezultat

    def make_side_pots(self):
        igralci = self.igralci
        stave_igralcev = set()
        side_pots = {}
        for igralec in igralci:
            stave_igralcev.add(igralec.žetoni_v_igri)
        stave_igralcev = list(stave_igralcev)
        stave_igralcev.sort()

        stanje_stav = stave_igralcev
        # v tem bodo odšteti deli stav, ki pripadajo prejšnjem side pot-u
        for i in range(len(stave_igralcev)):
            side_pots[stave_igralcev[i]] = len(igralci) * stanje_stav[i]
            # side pot je odvisen od števila igralcev, ki še "pokrijejo to stavo" (to so igralci v seznamu igralci)
            # in odvisen je še od velikosti stave, os katere je odšteta vrednost prejšnjega stanja stave
            # stanje stave se zmanjša, ko se en del stave dodeli side potu za drugega igralca, z manj žetoni
            # side poti so dodeljeni začetnim žetonom v igri in ne igralcem
            # to niso še pravi side poti, ker moraš preverit še kdo je zmagal in posledično pobral svoj pot
            # če zmaga, pobere svoj side_pot in vse manjše side pote
            igralci_s_tako_stavo = []
            for igralec in igralci:
                if igralec.žetoni_v_igri == stave_igralcev[i]:
                    igralci_s_tako_stavo.append(igralec)
            for igralec in igralci_s_tako_stavo:
                igralci = [player for player in igralci if player != igralec]
            stanje_stav = list(map(lambda x: x - stanje_stav[i], stanje_stav))
            # spremeni stanje stav tako da odšteje del stave, ki se dodeli prejšnjemu side potu
        return side_pots

    def razdeli_pot(self):
        """Razdeli vse side pot-e."""
        igralci = [igralec for igralec in self.kdo_je_v_igri()]
        side_pots = self.make_side_pots()
        vse_stave = list(side_pots.keys())
        vse_stave.sort()
        while len(vse_stave) != 0:
            for igralec in self.kdo_je_v_igri():
                igralec.zmaga = False

            self.kdo_je_zmagal_rundo(igralci)
            # ne glede kdo je absolutno zmagal rundo, ampak kdo ima najboljšo kombinacijo izmed igralcev v listu igralci
            zmagovalci = [igralec for igralec in igralci if igralec.zmaga]
            # v seznamu zmagovalcu so igralci s popolnoma enako (najmočnejšo) kombinacijo petih kart

            že_štete_stave = set()
            poti_od_igralcev = []
            for zmagovalec in zmagovalci:
                zmagovalec_pot = 0
                for stava in vse_stave:
                    if stava <= zmagovalec.žetoni_v_igri:
                        zmagovalec_pot += side_pots.get(stava)
                        že_štete_stave.add(stava)
                poti_od_igralcev.append(zmagovalec_pot)

            zmagovalci.sort(key=lambda x: x.žetoni_v_igri)
            dolzina = len(zmagovalci)
            for i in range(len(zmagovalci)):
                zmagovalci[i].žetoni += poti_od_igralcev[i] // dolzina
                poti_od_igralcev = list(map(lambda x: x - (poti_od_igralcev[i] // dolzina), poti_od_igralcev))
                dolzina -= 1

            for stava in že_štete_stave:
                vse_stave.remove(stava)
                # side poti od teh stav so bili že upoštevani
            for zmagovalec in zmagovalci:
                igralci.remove(zmagovalec)


class Igra:
    def __init__(self, resnicni_igralec):
        self.runda = None

        self.resnicni_igralec = resnicni_igralec
        self.nespametni_goljuf = NespametniGoljuf("goljuf", self)
        self.blefer = Blefer("blefer")
        self.agresivnež = Agresivnež("agresivnež")
        self.ravnodušnež = Ravnodušnež("ravnodušnež")

        self.igralci = [
            self.resnicni_igralec,
            self.nespametni_goljuf,
            self.blefer,
            self.agresivnež,
            self.ravnodušnež,
        ]

    def nova_runda(self):
        self.igralci.append(self.igralci.pop(0))  # Rotiraj igralce, da dobimo novega dealer-ja.
        self.runda = Runda(self.igralci)

    def shrani_potezo(self):
        self.resnicni_igralec.je_bil_na_potezi = True
        self.runda.stevilo_potez += 1

    def povisaj(self, koliko):
        self.runda.igralec_na_potezi_stavi(koliko)
        self.shrani_potezo()

    def klici(self):
        razlika = self.resnicni_igralec.razlika_za_klicat
        self.runda.igralec_na_potezi_stavi(razlika)
        self.shrani_potezo()

    def odstopi(self):
        self.resnicni_igralec.folda()
        self.shrani_potezo()

    def check(self):
        self.resnicni_igralec.check = True
        self.shrani_potezo()

    # uporabimo v html-ju, ker sicer posamezen igralec ne ostaja na istem mestu v novi rundi, saj se igralci rotirajo.
    def vsi_igralci(self):
        return [
            self.resnicni_igralec,
            self.nespametni_goljuf,
            self.blefer,
            self.agresivnež,
            self.ravnodušnež,
        ]


if __name__ == "__main__":

    janez = Igralec("janez")
    igra = Igra(janez)
    igra.nova_runda()