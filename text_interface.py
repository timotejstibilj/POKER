from model import Igralec, Igra

pomoc = "Ukazi: stanje, klici, povisaj, odstopi, check"

janez = Igralec("janez")
igra = Igra(janez)
igra.nova_runda()


def odigraj_krog():
    while not igra.runda.stave_so_poravnane():
        tekst = input("> ")
        tekst = tekst.split()
        ukaz = tekst[0]
        vrednost = tekst[1] if len(tekst) == 2 else None
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
    if igra.runda.imamo_predcasnega_zmagovalca():
        return
    igra.runda.deck.deli_karto(igra.runda.miza, stevilo_kart)
    odigraj_krog()


while True:
    tekst = input("Začni rundo? ")
    if tekst != "ja":
        break
    igra.nova_runda()
    deli_in_igraj(0)
    deli_in_igraj(3)
    deli_in_igraj(1)
    deli_in_igraj(1)