import bottle
import uuid
from model import Igralec, Igra

IME_PISKOTKA = "Igra"
SKRIVNOST = "To je ena velika skrivnost."
igre = {}

# pomožne funkcije -----------------------------------------------------------


def ugotovi_igro():
    id = bottle.request.get_cookie(IME_PISKOTKA, secret=SKRIVNOST)

    if id is None or id not in igre:
        bottle.response.delete_cookie(IME_PISKOTKA, path="/")
        bottle.redirect("/")
    else:
        return igre[id]


def odpri_karte():
    igra = ugotovi_igro()

    stevilo_kart = 1
    if igra.runda.imamo_predcasnega_zmagovalca():
        stevilo_kart = 0
    elif igra.runda.kje_smo_v_igri == "flop":
        stevilo_kart = 3
    igra.runda.deck.deli_karto(igra.runda.miza, stevilo_kart)


# Static files ---------------------------------------------------------------


@bottle.get("/static/<path:path>")
def files(path):
    return bottle.static_file(path, root="static/")


# Routes ---------------------------------------------------------------------


@bottle.get("/")
def vpisi_se():
    return bottle.template("zacetek.html")


@bottle.post("/nova_igra/")
def ustvari_igro():
    ime_igralca = bottle.request.forms.getunicode("ime_igralca")
    id_igre = str(uuid.uuid4())

    resnicni_igralec = Igralec(ime_igralca)
    igra = Igra(resnicni_igralec)
    igra.nova_runda()
    igre[id_igre] = igra
    bottle.response.set_cookie(IME_PISKOTKA, id_igre, path="/", secret=SKRIVNOST)

    bottle.redirect("/celotna_igra/")


@bottle.get("/celotna_igra/")
def igra():
    igra = ugotovi_igro()
    igra.nova_runda()

    if igra.resnicni_igralec not in igra.runda.kdo_je_živ() or len(igra.igralci) == 1:
        return bottle.template("ponovna_igra", ime=igra.resnicni_igralec.ime, igra=igra)
    else:
        bottle.redirect("/krog_stav/")


@bottle.get("/krog_stav/")
def krog_stav():
    """Stavijo računalniški igralci.
    Krog se prekine, ko pridemo do resničnega igralca
    ali ko so stave poravnane.
    """

    igra = ugotovi_igro()

    igra.runda.pokaži_razlike_za_klicat()
    if igra.runda.stave_so_poravnane():
        bottle.redirect("/celotna_runda/")

    elif igra.runda.igralec_na_potezi != igra.runda.igralec_resnicni:
        # Ob začetku novega dela igre, vrne gumb za potezo
        if (
            igra.runda.stevilo_potez == 0
            and not igra.igralci[igra.runda.igralec_na_potezi].fold
            and not igra.igralci[igra.runda.igralec_na_potezi].all_in
        ):
            igra.runda.stevilo_potez = 1
            return bottle.template("poteza_naslednjega_igralca.html", igra=igra)

        else:
            igra.runda.vprasaj_racunalnik_za_potezo()
            igra.runda.stevilo_potez += 1
            igra.igralci[igra.runda.igralec_na_potezi].je_bil_na_potezi = True
            igra.runda.pokaži_razlike_za_klicat()

            igra.runda.naslednji_na_potezi()
            if igra.runda.igralec_na_potezi != igra.runda.igralec_resnicni and not igra.runda.stave_so_poravnane():
                return bottle.template("poteza_naslednjega_igralca.html", igra=igra)

    bottle.redirect("/celotna_runda/")


@bottle.get("/celotna_runda/")
def celotna_runda():
    igra = ugotovi_igro()

    if igra.runda.imamo_predcasnega_zmagovalca():
        igra.runda.pripni_kombinacije(igra.runda.miza)
        return bottle.template("pokazi_zmagovalca.html", igra=igra)
    if igra.runda.predcasno_zakljucena_runda():
        while len(igra.runda.miza.karte) != 5:
            igra.runda.deck.deli_karto(igra.runda.miza, 1)
        igra.runda.kje_smo_v_igri = "konec"
        igra.runda.pripni_kombinacije(igra.runda.miza)
        return bottle.template("pokazi_zmagovalca.html", igra=igra)
    if igra.runda.pojdi_v_naslednji_krog() and igra.runda.kje_smo_v_igri != "konec":
        igra.blefer.je_bil_na_potezi = False
        bottle.redirect("/odpri_karte/")
    elif igra.runda.kje_smo_v_igri != "konec":
        return bottle.template("odigraj_krog.html", igra=igra)
    else:
        igra.runda.pripni_kombinacije(igra.runda.miza)
        return bottle.template("pokazi_zmagovalca.html", igra=igra)


@bottle.get("/odigraj_krog/")
def odigraj():
    igra = ugotovi_igro()

    return bottle.template("odigraj_krog.html", igra=igra)


@bottle.get("/odpri_karte/")
def odpri():
    odpri_karte()
    bottle.redirect("/krog_stav/")


@bottle.post("/konec_runde/")
def konec():
    igra = ugotovi_igro()

    igra.runda.razdeli_pot()

    bottle.redirect("/celotna_igra/")


@bottle.post("/povisaj/")
def povisaj():
    igra = ugotovi_igro()

    vrednost = int(bottle.request.forms.getunicode("koliko"))
    if vrednost < igra.resnicni_igralec.razlika_za_klicat:
        return bottle.template("premajhna_stava.html", igra=igra)

    igra.povisaj(vrednost)
    igra.runda.naslednji_na_potezi()

    return bottle.template("poteza_naslednjega_igralca.html", igra=igra)


@bottle.post("/check/")
def check():
    igra = ugotovi_igro()

    igra.check()
    igra.runda.naslednji_na_potezi()

    return bottle.template("poteza_naslednjega_igralca.html", igra=igra)


@bottle.post("/klici/")
def klici():
    igra = ugotovi_igro()

    igra.klici()
    igra.runda.naslednji_na_potezi()

    return bottle.template("poteza_naslednjega_igralca.html", igra=igra)


@bottle.post("/odstopi/")
def odstopi():
    igra = ugotovi_igro()

    igra.odstopi()
    igra.runda.naslednji_na_potezi()

    return bottle.template("poteza_naslednjega_igralca.html", igra=igra)


@bottle.post("/prekini_igro/")
def zbrisi_piskotek():
    bottle.response.delete_cookie(IME_PISKOTKA, path="/")
    bottle.redirect("/")


# Zaženi ---------------------------------------------------------------------

if __name__ == "__main__":
    # Zaženi spletni vmesnik.
    bottle.run(debug=True, reloader=True)
