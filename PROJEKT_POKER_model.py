import random
from itertools import combinations
import holdem_calc


class Karta:
    def __init__(self, znak, stevilo):
        self.znak = znak
        self.stevilo = stevilo

    def __repr__(self):
        slovar_stevil = {11: "'FANT'", 12: "'DAMA'", 13: "'KRALJ'", 14: "'AS'"}
        for i in range(2, 11):
            slovar_stevil[i] = i
        znakci = {0: "'križ'", 1: "'pik'", 2: "'srce'", 3: "'kara'"}
        return "({},{})".format(znakci.get(self.znak), slovar_stevil.get(self.stevilo))

    def __eq__(self, other):
        return self.znak == other.znak and self.stevilo == other.stevilo

    def __hash__(self):
        return hash((self.znak, self.stevilo))


class Deck(list):
    def __init__(self):
        super().__init__()
        for stevilo in range(2, 15):
            for znak in range(4):
                self.append(Karta(znak, stevilo))

    def premešaj_karte(self):
        random.shuffle(self)

    def deli_karto(self, komu, koliko_kart):
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
        self.na_potezi = False
        self.all_in = False
        self.položaj = []
        self.verjetnost_zmage = 0
        self.zmaga = False

    # položaj je če je big blind, small blind

    def __repr__(self):
        ime = self.ime
        return ime

    ##############################################################
    def check(self):
        pass

    def folda(self):
        self.fold = True

    def stavi(self, koliko):
        self.žetoni -= koliko
        miza.pot += koliko
        self.žetoni_v_igri += koliko

    ##############################################################

    def seznam_kombinacij_kart(self):
        izbira_iz = self.karte + miza.karte
        return list(combinations(izbira_iz, 5))
        # v metodo moraš napisat za katero mizo se gleda

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
            # ker je AS reprezentiran s 14, ampak je lahko tudi v vlogi 1
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

    def lastnosti_kombinacije_igralca(self):
        moč_kombinacije = 0
        velikost_pomembne_karte = 0
        velikosti_preostalih_kart = []
        najmočnejše_kombinacije_brez_najvišje_karte = []
        najmočnejše_kombinacije_z_najvišjo_karto = []
        absolutno_najmočnejša_kombinacija = None
        # kakšna vrsta kombinacije je najvišja: npr.par
        for combination in self.seznam_kombinacij_kart(miza):
            if self.kombinacija_od_peterke(combination) >= moč_kombinacije:
                moč_kombinacije = self.kombinacija_od_peterke(combination)
        # vse take kombinacije, npr.vsi pari
        for combination in self.seznam_kombinacij_kart(miza):
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
            if self.velikosti_preostalih_kart(kombinacija) > self.velikosti_preostalih_kart(
                absolutno_najmočnejša_kombinacija
            ):
                absolutno_najmočnejša_kombinacija = kombinacija

        velikost_pomembne_karte = self.velikost_pomembne_karte(absolutno_najmočnejša_kombinacija)
        velikosti_preostalih_kart = self.velikosti_preostalih_kart(absolutno_najmočnejša_kombinacija)
        kombinacija = [
            moč_kombinacije,
            velikost_pomembne_karte,
            velikosti_preostalih_kart,
        ]
        return kombinacija


####################################################################################################

# na koncu vsake runde moraš ponastavit te atribute, kako bodo igrali
class Agresivnež(Igralec):
    "Kot ime pove, agresivnež rad poseže globoko v žep in visoko stavi tudi v tveganih situacijah."

    def __init__(self, ime):
        super().__init__(ime)
        self.bo_raisal = False
        self.koliko_bo_raisal = 0
        self.bo_callal = False

    def kako_igra(self, ime_resničnega_igralca):
        verjetnost_zmage = runda.zračunaj_verjetnost_zmag(ime_resničnega_igralca).get(agresivnež)
        # to je približna verjetnost, če bi igral samo z enim nasprotnikom
        if len(runda.kdo_je_v_igri(ime_resničnega_igralca)) >= 3:
            # če je manjša verjetnost je raise in call itak false in check, fold pa True
            if verjetnost_zmage > 0.40 and verjetnost_zmage <= 0.75:
                self.bo_raisal = bool(random.choices([True, False], [1, 4], None, k=1))
                self.bo_callal = bool(random.choices([True, False], [4, 3], None, k=1))
                if self.razlika_za_klicat > 0:
                    self.koliko_bo_raisal = random.choice(list(range(1, 4))) * self.razlika_za_klicat
                else:
                    self.koliko_bo_raisal = 3 / random.choice(list(range(7, 12))) * self.žetoni
            elif verjetnost_zmage > 0.75:
                self.bo_raisal = bool(random.choices([True, False], [8, 1], None, k=1))
                if self.razlika_za_klicat > 0:
                    self.koliko_bo_raisal = random.choice(list(range(3, 8))) * self.razlika_za_klicat
                else:
                    self.koliko_bo_raisal = 1 / random.choice(list(range(1, 10))) * self.žetoni
                self.bo_raisal = True
        elif len(runda.kdo_je_v_igri(ime_resničnega_igralca)) < 3:
            if verjetnost_zmage <= 0.40 and verjetnost_zmage > 0.25:
                if self.razlika_za_klicat < (self.žetoni / 3):
                    self.bo_callal = bool(random.choices([True, False], [1, 6], None, k=1))
            elif verjetnost_zmage > 0.40 and verjetnost_zmage <= 0.75:
                self.bo_raisal = bool(random.choices([True, False], [3, 5], None, k=1))
                self.bo_callal = bool(random.choices([True, False], [3, 2], None, k=1))
                if self.razlika_za_klicat > 0:
                    self.koliko_bo_raisal = random.choice(list(range(1, 3))) * self.razlika_za_klicat
                else:
                    self.koliko_bo_raisal = 1 / random.choice(list(range(6, 10))) * self.žetoni
            elif verjetnost_zmage > 0.75:
                self.bo_raisal = bool(random.choices([True, False], [8, 1], None, k=1))
                self.bo_callal = True
                if self.razlika_za_klicat > 0:
                    self.koliko_bo_raisal = random.choice(list(range(5, 10))) * self.razlika_za_klicat
                else:
                    self.koliko_bo_raisal = 1 / random.choice(list(range(1, 5))) * self.žetoni


class Ravnodušnež(Igralec):
    "Pač niso vsi za poker. Ravnodušneža kartanje ne zanima, zato je vsaka njegova poteza popolnoma naključna."

    def __init__(self, ime):
        super().__init__(ime)
        self.bo_raisal = False
        self.koliko_bo_raisal = 0
        self.bo_callal = False

    def kako_igra(self):
        self.bo_raisal = bool(random.choice([True, False]))
        self.koliko_bo_raisal = 0
        self.bo_callal = bool(random.choice([True, False]))
        if self.razlika_za_klicat > 0:
            self.koliko_bo_raisal = random.choice(list(range(1, 5))) * self.razlika_za_klicat
        else:
            self.koliko_bo_raisal = 4 / random.choice(list(range(1, 12))) * self.žetoni


class Blefer(Igralec):
    "Nekateri radi poskušajo pretentati soigralce in pogosto stavijo tudi v primerih, ko jim karte niso naklonjene. Blefer je prav tak."

    def __init__(self, ime):
        super().__init__(ime)
        self.bo_raisal = False
        self.koliko_bo_raisal = 0
        self.bo_callal = False

    def kako_igra(self, ime_resničnega_igralca):
        verjetnost_zmage = runda.zračunaj_verjetnost_zmag(ime_resničnega_igralca).get(blefer)
        # to je približna verjetnost, če bi igral samo z enim nasprotnikom
        if len(runda.kdo_je_v_igri(ime_resničnega_igralca)) >= 3:
            # če je manjša verjetnost je raise in call itak false in check, fold pa True
            if verjetnost_zmage > 0.40 and verjetnost_zmage <= 0.75:
                self.bo_raisal = bool(random.choices([True, False], [1, 3], None, k=1))
                self.bo_callal = bool(random.choices([True, False], [4, 3], None, k=1))
                if self.razlika_za_klicat > 0:
                    self.koliko_bo_raisal = random.choice(list(range(1, 12))) * self.razlika_za_klicat
                else:
                    self.koliko_bo_raisal = 3 / random.choice(list(range(3, 10))) * self.žetoni
            elif verjetnost_zmage > 0.75:
                self.bo_raisal = bool(random.choices([True, False], [8, 1], None, k=1))
                self.bo_raisal = True
                self.koliko_bo_raisal = random.choice([self.žetoni, 0.5 * self.žetoni])
        elif len(runda.kdo_je_v_igri(ime_resničnega_igralca)) < 3:
            if verjetnost_zmage <= 0.40 and verjetnost_zmage > 0.25:
                if self.razlika_za_klicat < (self.žetoni / 3):
                    self.bo_raisal = bool(random.choices([True, False], [5, 1], None, k=1))
                    if self.razlika_za_klicat > 0:
                        self.koliko_bo_raisal = random.choices(
                            [self.razlika_za_klicat * 3, self.razlika_za_klicat * 5], [3, 1], None, k=1
                        )
                    else:
                        self.koliko_bo_raisal = 3 / random.choice(list(range(8, 12))) * self.žetoni
            elif verjetnost_zmage > 0.40 and verjetnost_zmage <= 0.75:
                self.bo_raisal = bool(random.choices([True, False], [10, 1], None, k=1))
                self.bo_callal = True
                if self.razlika_za_klicat > 0:
                    self.koliko_bo_raisal = random.choices(
                        [self.razlika_za_klicat * 5, self.razlika_za_klicat * 8], [3, 1], None, k=1
                    )
                else:
                    self.koliko_bo_raisal = 3 / random.choice(list(range(3, 7))) * self.žetoni
            elif verjetnost_zmage > 0.75:
                self.bo_raisal = True
                self.bo_callal = True
                self.koliko_bo_raisal = self.žetoni


class Nespametni_goljuf(Igralec):
    """Nespametni goljuf se požvižga na moralo, zato si pogosto ogleduje nasprotnikove karte. \n
    Pri igranju vedno izkorišče izračunano verjetnost zmag igralcev, kar pa se mu ne obnese v zadnjem krogu, ko bi lahko sam ugotovil, kdo je zmagovalec."""

    def __init__(self, ime):
        super().__init__(ime)
        self.bo_raisal = False
        self.bo_callal = False

    def kako_igra(self, ime_resničnega_igralca):
        verjetnost_zmag_igralcev = runda.zračunaj_verjetnost_zmag(ime_resničnega_igralca)
        # to je približna verjetnost, če bi igral samo z enim nasprotnikom
        ima_najboljše_karte = False
        if verjetnost_zmag_igralcev.get(nespametni_goljuf) == max(verjetnost_zmag_igralcev.values()):
            ima_najboljše_karte = True
        if ima_najboljše_karte:
            self.bo_raisal = bool(random.choices([True, False], [7, 1], None, k=1))
            self.bo_callal = True
            if self.razlika_za_klicat > 0:
                self.koliko_bo_raisal = random.choices(
                    [self.razlika_za_klicat * 5, self.razlika_za_klicat * 9], [3, 1], None, k=1
                )
            else:
                self.koliko_bo_raisal = 3 / random.choice(list(range(6, 10))) * self.žetoni
        else:
            if verjetnost_zmag_igralcev.get(nespametni_goljuf) < 30:
                self.bo_callal = bool(random.choices([True, False], [1, 7], None, k=1))
            elif verjetnost_zmag_igralcev.get(nespametni_goljuf) < 50:
                self.bo_raisal = bool(random.choices([True, False], [4, 3], None, k=1))
                self.bo_callal = bool(random.choices([True, False], [5, 2], None, k=1))
                if self.razlika_za_klicat > 0:
                    self.koliko_bo_raisal = random.choices(
                        [self.razlika_za_klicat * 2, self.razlika_za_klicat * 3], [3, 1], None, k=1
                    )
                else:
                    self.koliko_bo_raisal = 4 / random.choice(list(range(10, 20))) * self.žetoni
            else:
                self.bo_raisal = bool(random.choices([True, False], [5, 1], None, k=1))
                self.bo_callal = True
                if self.razlika_za_klicat > 0:
                    self.koliko_bo_raisal = random.choice(list(range(1, 5))) * self.razlika_za_klicat
                else:
                    self.koliko_bo_raisal = 3 / random.choice(list(range(3, 10))) * self.žetoni


######################################################################################################################
######################################################################################################################


class Runda:
    def __init__(self, igralci):
        self.stave_so_poravnane = False
        self.deck = Deck()
        self.igralci = igralci

    ######################################################################################################################

    def spremeni_zapis_kart(self):
        dek = Deck()
        slovar_kart = {}
        slovar_znakcev = {0: "c", 1: "s", 2: "h", 3: "d"}
        slovar_stevilk = {11: "J", 12: "Q", 13: "K", 14: "A"}
        # znaki so club, spade, heart, diamond
        # stevila so jack, queen, king in ace
        for i in range(2, 11):
            slovar_stevilk[i] = str(i)
        for karta in dek:
            slovar_kart[karta] = slovar_stevilk.get(karta.stevilo) + slovar_znakcev.get(karta.znak)
        return slovar_kart
        # vrne zapis kart primeren za računanje verjetnosti s holdem_calc

    def zračunaj_verjetnost_zmag(self, ime_resničnega_igralca):
        verjetnost_zmag = {}
        igralci = runda.kdo_je_v_igri(ime_resničnega_igralca)
        for igralec in igralci:
            karti_igralca = igralec.karte
            karta_1 = runda.spremeni_zapis_kart().get(karti_igralca[0])
            karta_2 = runda.spremeni_zapis_kart().get(karti_igralca[1])
            karte_miza = miza.karte
            spremenjene_karte_miza = [runda.spremeni_zapis_kart().get(karta) for karta in karte_miza]
            if len(miza.karte) == 0:
                holdem = holdem_calc.calculate(None, False, 20000, None, [karta_1, karta_2, "?", "?"], False)
                verjetnost_zmag[igralec] = holdem[1]
            elif len(miza.karte) == 3:
                holdem = holdem_calc.calculate(
                    spremenjene_karte_miza,
                    False,
                    20000,
                    None,
                    [karta_1, karta_2, "?", "?"],
                    False,
                )
                verjetnost_zmag[igralec] = holdem[1]
            elif len(miza.karte) == 4:
                holdem = holdem_calc.calculate(
                    spremenjene_karte_miza,
                    False,
                    20000,
                    None,
                    [karta_1, karta_2, "?", "?"],
                    False,
                )
                verjetnost_zmag[igralec] = holdem[1]
            elif len(miza.karte) == 5:
                holdem = holdem_calc.calculate(
                    spremenjene_karte_miza,
                    False,
                    20000,
                    None,
                    [karta_1, karta_2, "?", "?"],
                    False,
                )
                verjetnost_zmag[igralec] = holdem[1]
        # karte na mizi, točno računanje-true\simulacija-false, število simulacij, datoteka, karte, false
        # prvo vrže tie, pol zmago prvega, pol zmago drugega
        # treba je spremenit imena kart, da jih bo lahko funkcija sprejela
        return verjetnost_zmag

    #####################################################################################################################

    def kdo_je_živ(self, ime_resničnega_igralca):
        igralci_v_igri = []
        for igralec in self.igralci:
            if igralec.žetoni > 0:
                if not igralec.all_in:
                    igralci_v_igri.append(igralec)
        return igralci_v_igri
        # igralci, ki imajo še kaj žetonov

    def kdo_je_v_igri(self, ime_resničnega_igralca):
        return [igralec for igralec in self.kdo_je_živ(ime_resničnega_igralca) if not igralec.fold]
        # igralci, ki še niso foldali

    def spremeni_položaj_igralcev(self, ime_resničnega_igralca):
        igralci = self.igralci
        igralci_z_novim_položajem = {}
        položaji = ["dealer", "small blind", "big blind", "first actor"]
        for i in range(5):
            for položaj in položaji:
                if položaj in igralci[i].položaj:
                    for j in range(1, 5):
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

        # spremeni kdo je small, big blind, dealer, first actor

    def razdeli_karte(self, ime_resničnega_igralca):
        začni_delit = False
        for igralec in self.igralci:
            if igralec in self.kdo_je_živ(ime_resničnega_igralca):
                if "small blind" in igralec.položaj:
                    začni_delit = True
                    self.deck.deli_karto(igralec, 2)
                elif začni_delit:
                    self.deck.deli_karto(igralec, 2)

    def stavi_small_in_big_blind(self, ime_resničnega_igralca):
        for igralec in self.kdo_je_živ(ime_resničnega_igralca):
            if "small blind" in igralec.položaj:
                igralec.žetoni -= miza.small_blind
                miza.pot += miza.small_blind
            elif "big blind" in igralec.položaj:
                igralec.žetoni -= miza.big_blind
                miza.pot += miza.big_blind

    def pripni_kombinacije(self, ime_resničnega_igralca):
        for igralec in self.igralci:
            igralec.kombinacija.extend(igralec.lastnosti_kombinacije_igralca(miza))

    def stave_so_poravnane(self, kira_runda, ime_resničnega_igralca):
        stava = 0
        for igralec in self.igralci:
            stava = max(stava, igralec.žetoni_v_igri)
        for igralec in kira_runda.kdo_je_v_igri(ime_resničnega_igralca):
            if igralec.žetoni_v_igri != stava:
                if not igralec.all_in:
                    self.stave_so_poravnane = True

    def pokaži_kako_igralci_igrajo(self, ime_resničnega_igralca):
        for igralec in self.igralci:
            igralec.kako_igra(ime_resničnega_igralca)

    def krog_stav(self, ime_resničnega_igralca):
        gremo_dalje = False
        while self.stave_so_poravnane == False:
            for igralec in self.igralci:
                if "first actor" in igralec.položaj:
                    if igralec in self.kdo_je_v_igri(ime_resničnega_igralca):
                        self.vprašaj_igralca_za_potezo(igralec, ime_resničnega_igralca)
                        gremo_dalje = True
                elif gremo_dalje:
                    if igralec in self.kdo_je_v_igri(ime_resničnega_igralca):
                        self.vprašaj_igralca_za_potezo(igralec, ime_resničnega_igralca)

    def vprašaj_igralca_za_potezo(self, kateri_igralec, ime_resničnega_igralca):
        # resnični igralec sam pove kako bo igral
        self.pokaži_kako_igralci_igrajo(ime_resničnega_igralca)
        if kateri_igralec == ime_resničnega_igralca:
            if ime_resničnega_igralca.razlika_za_klicat > 0:
                if ime_resničnega_igralca.razlika_za_klicat > ime_resničnega_igralca.žetoni:
                    ime_resničnega_igralca.stavi(ime_resničnega_igralca.žetoni)
                    ime_resničnega_igralca.all_in = True
                else:
                    ime_resničnega_igralca.stavi(ime_resničnega_igralca.razlika_za_klicat)
            else:
                ime_resničnega_igralca.check
        # če je računalnik pa igra tako
        if kateri_igralec.razlika_za_klicat > 0:
            if kateri_igralec.bo_raisal:
                if kateri_igralec.koliko_bo_raisal < kateri_igralec.žetoni:
                    kateri_igralec.stavi(kateri_igralec.koliko_bo_raisal)
                else:
                    kateri_igralec.stavi(kateri_igralec.žetoni)
                    kateri_igralec.all_in = True
            elif kateri_igralec.bo_callal:
                if kateri_igralec.razlika_za_klicat >= kateri_igralec.žetoni:
                    kateri_igralec.stavi(kateri_igralec.žetoni)
                    kateri_igralec.all_in = True
                else:
                    kateri_igralec.stavi(kateri_igralec.razlika_za_klicat)
            else:
                kateri_igralec.fold
        else:
            kateri_igralec.check
        # spremeni razlike za klicat, po vsaki potezi
        self.pokaži_razlike_za_klicat(ime_resničnega_igralca)

    def pokaži_razlike_za_klicat(self, ime_resničnega_igralca):
        največja_količina_žetonov_v_igri = 0
        for igralec in self.kdo_je_v_igri(ime_resničnega_igralca):
            največja_količina_žetonov_v_igri = max(največja_količina_žetonov_v_igri, igralec.žetoni_v_igri)
        for igralec in self.kdo_je_v_igri(ime_resničnega_igralca):
            if največja_količina_žetonov_v_igri > igralec.žetoni_v_igri:
                igralec.razlika_za_klicat = največja_količina_žetonov_v_igri - igralec.žetoni_v_igri

    def kdo_je_zmagal_rundo(self, ime_resničnega_igralca, kiri_igralci):
        igralci = kiri_igralci
        zmagovalci = []
        najboljši_hand = [0, 0, 0, 0, 0]
        for igralec in igralci:
            if igralec.kombinacija > najboljši_hand:
                najboljši_hand = igralec.kombinacija
        for igralec in igralci:
            if igralec.kombinacija == najboljši_hand:
                zmagovalci.append(igralec)
        for zmagovalec in zmagovalci:
            zmagovalec.zmaga = True
        # lahko ni samo en, če pride do situacije, da ima več igralcev kombinacijo 5 istih kart
        # če ni side_potov --> kiri_igralci = self.kdo_je_v_igri(ime_resničnega_igralca)

    def make_side_pots(self, ime_resničnega_igralca):
        igralci = self.igralci
        stave_igralcev = set()
        side_pots = {}
        for igralec in igralci:
            stave_igralcev.add(igralec.žetoni_v_igri)
        # naraščajoče stave vseh igralcev so to spodi
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
                igralci.remove(igralec)
            stanje_stav = list(map(lambda x: x - stanje_stav[i], stanje_stav))
            # spremeni stanje stav tako da odšteje del stave, ki se dodeli prejšnjemu side potu
        return side_pots

    def razdeli_pot(self, ime_resničnega_igralca):
        igralci = self.kdo_je_v_igri(ime_resničnega_igralca)
        side_pots = self.make_side_pots(ime_resničnega_igralca)
        vse_stave = list(side_pots.keys()).sort()
        kiri_igralci = [
            ime_resničnega_igralca,
            nespametni_goljuf,
            ravnodušnež,
            agresivnež,
            blefer,
        ]
        for igralec in igralci:
            igralec.zmaga = False
            self.kdo_je_zmagal_rundo(ime_resničnega_igralca, kiri_igralci)
            if igralec.zmaga:
                dodaj = 0
                for stava in vse_stave:
                    if stava <= side_pots.get(igralec.žetoni_v_igri):
                        dodaj += stava
            igralec.žetoni += dodaj
            kiri_igralci.remove(igralec)

        # treba je še upoštevat, da tisti ki zmaga ne nujno pobere vsega, če je all_in in so drugi stavli še dalje

    def počisti_rundo(self, ime_resničnega_igralca):
        for igralec in self.igralci:
            igralec.karte.clear()
            igralec.kombinacija.clear()
            igralec.žetoni_v_igri = 0
            igralec.razlika_za_klicat = 0
            igralec.fold = False
            igralec.na_potezi = False
            igralec.all_in = False
            igralec.zmaga = False
            igralec.verjetnost_zmage = 0
        miza.karte.clear()
        miza.pot = 0
        self.deck = Deck()

        # položaj pustiš pri miru, ker ga ureja že funkcija spremeni_položaj_igralcev

    def nova_runda(self, ime_resničnega_igralca):
        # preflop
        self.spremeni_položaj_igralcev(janez)
        self.počisti_rundo(ime_resničnega_igralca)
        self.deck.premešaj_karte()
        self.razdeli_karte(ime_resničnega_igralca)
        self.stavi_small_in_big_blind(ime_resničnega_igralca)
        self.krog_stav(ime_resničnega_igralca)
        # flop
        self.deck.deli_karto(miza, 3)
        self.krog_stav(ime_resničnega_igralca)
        self.stave_so_poravnane = False
        # na turnu je nov krog stav od začetka
        # turn, river
        for i in range(2):
            self.deck.deli_karto(miza, 1)
            self.krog_stav(ime_resničnega_igralca)
            self.stave_so_poravnane = False
            # na koncu sicer kaže false tudi če so poravnane, ampak ni s tem nič narobe
        self.pripni_kombinacije(ime_resničnega_igralca)
        self.kdo_je_zmagal_rundo(ime_resničnega_igralca, self.kdo_je_v_igri)
        self.razdeli_pot(ime_resničnega_igralca)


class Igra:
    def __init__(self, resnicni_igralec):
        self.konec_igre = False
        self.runda = None

        self.miza = Miza()

        self.resnicni_igralec = resnicni_igralec
        self.nespametni_goljuf = Nespametni_goljuf("nespametni_goljuf")
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
        self.runda = Runda(self.igralci)
        self.runda.deck = Deck()

        self.resnicni_igralec.položaj.append("dealer")
        self.nespametni_goljuf.položaj.append("small blind")
        self.ravnodušnež.položaj.append("big blind")


igra = Igra(janez)

# igra.ustvari_igro(ime_resničnega_igralca)


# TEST:
# miza = Miza()
# runda = Runda()
# runda.deck.premešaj_karte()
# janez = Igralec("janez")
# nespametni_goljuf = Nespametni_goljuf("nespametni_goljuf")
# blefer = Blefer("blefer")
# agresivnež = Agresivnež("agresivnež")
# ravnodušnež = Ravnodušnež("ravnodušnež")
# print("============")
# igrači = [janez, nespametni_goljuf, ravnodušnež, agresivnež, blefer]
# janez.položaj.append("small blind")
# nespametni_goljuf.položaj.append("big blind")
# blefer.položaj.append("dealer")
#
# runda.razdeli_karte(janez)
## moraš dodat dek. ker je to metoda v classu Deck, dek je objekt iz razreda Deck
# runda.deck.deli_karto(miza, 3)
# runda.deck.deli_karto(miza, 1)
# runda.deck.deli_karto(miza, 1)
# print(miza)
# print("============")
# runda.pripni_kombinacije(miza, janez)
# runda.kdo_je_zmagal_rundo(janez, runda.kdo_je_v_igri(janez))
# runda.pokaži_razlike_za_klicat(janez)
# for i in igrači:
#    print(i)
#    print(i.karte)
#    print(i.razlika_za_klicat)
#    print(i.kombinacija)
#    print(i.zmaga)
# janez.stavi(10)
# ravnodušnež.stavi(20)
# nespametni_goljuf.stavi(100)
# agresivnež.stavi(150)
# print(runda.make_side_pots(janez))
# print(runda.zračunaj_verjetnost_zmag(janez))


# na začetku daš resničnega igralca na pozicijo dealerja
# pri seznamih, slovarjih lahko narediš izpeljane ponekod in prišparaš vrstico ali dve

# kako bi naredu da se igralec odloči al calla, raisa
# koliko
# in to cifro pol uporabu v modelu