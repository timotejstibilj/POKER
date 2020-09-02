from model import Igralec, Igra

pomoc = """Vpisati moraš ukaz: stanje, klici, povisaj, odstopi, check.
Če želiš višati moraš dopisati še vrednost."""

janez = Igralec("janez")
igra = Igra(janez)
igra.nova_runda()


def odigraj_krog():
    while not igra.runda.stave_so_poravnane():
        print("============================================================= \n")
        tekst = input("> Prosim za ukaz. \n")
        tekst = tekst.split()
        ukaz = tekst[0]
        vrednost = tekst[1] if len(tekst) == 2 else None
        igra.stanje()
        if ukaz == "klici":
            igra.klici()
        elif ukaz == "povisaj":
            igra.povisaj(int(vrednost))
        elif ukaz == "odstopi":
            igra.odstopi()
        elif ukaz == "check":
            igra.check()
        elif ukaz == "stanje":
            igra.stanje()
        else:
            print(pomoc)


def deli_in_igraj(stevilo_kart):
    igra.stanje()
    if igra.runda.imamo_predcasnega_zmagovalca():
        return "Zmagovalec je častitljivi{}.".format(igra.runda.kdo_je_v_igri())
    igra.runda.deck.deli_karto(igra.runda.miza, stevilo_kart)
    odigraj_krog()


def zakljucek_igre():
    igra.runda.pripni_kombinacije(igra.runda.miza)
    igra.runda.razdeli_pot()
    igra.stanje()
    print("Runda se je zaključila.")
    print("=============================================================")
    print("\n")


while True:
    tekst = input("Začni novo rundo? \n")
    if tekst != "ja":
        print("Kaj potem počneš tukaj?")
        break
    igra.nova_runda()
    print("============================================================= \n")
    print("Si v preflop-u.")
    deli_in_igraj(0)
    print("============================================================= \n")
    print("Si v flop-u.")
    deli_in_igraj(3)
    print("============================================================= \n")
    print("Si na turn-u.")
    deli_in_igraj(1)
    print("============================================================= \n")
    print("Si na river-ju.")
    deli_in_igraj(1)
    print("============================================================= \n")
    zakljucek_igre()
