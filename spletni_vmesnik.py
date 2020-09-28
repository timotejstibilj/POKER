import bottle
import uuid
from model import Igralec, Igra

IME_PISKOTKA = "Igra"
SKRIVNOST = "To je ena velika skrivnost."
igre = {}

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


def ugotovi_igro():
    id = bottle.request.get_cookie(IME_PISKOTKA, secret=SKRIVNOST)

    if id is None or id not in igre:
        bottle.response.delete_cookie(IME_PISKOTKA, path="/")
        bottle.redirect("/")
    else:
        return igre[id]


@bottle.get("/celotna_igra/")
def igra():
    igra = ugotovi_igro()

    if igra.resnicni_igralec not in igra.runda.kdo_je_živ() or len(igra.igralci) == 1:
        return bottle.template("ponovna_igra", ime=igra.resnicni_igralec.ime, igra=igra)
    else:
        return bottle.template("celotna_igra.html")


def odpri_karte():
    igra = ugotovi_igro()
    if igra.runda.kje_smo_v_igri == "flop":
        stevilo_kart = 3
    if igra.runda.kje_smo_v_igri == "turn" or igra.runda.kje_smo_v_igri == "river":
        stevilo_kart == 1
    igra.runda.deck.deli_karto(igra.runda.miza, stevilo_kart)


def pokazi_stevilo_zetonov():
    igra = ugotovi_igro()
    return bottle.template("število_žetonov.html", igra=igra)


def poskrbi_za_konec_runde():
    igra.runda.pripni_kombinacije(igra.runda.miza)
    igra.runda.razdeli_pot()
    pokazi_stevilo_zetonov()
    igra.nova_runda()
    bottle.redirect("/celotna_igra/")


@bottle.post("/celotna_runda/")
def celotna_runda():
    igra = ugotovi_igro()

    if igra.runda.pojdi_v_naslednji_krog():
        odpri_karte()
    if igra.runda.imamo_predcasnega_zmagovalca():
        poskrbi_za_konec_runde()
    if igra.runda.kje_smo_v_igri != "konec":
        bottle.redirect("/odigraj_krog/")
    else:
        poskrbi_za_konec_runde()


@bottle.get("/odigraj_krog/")
def igraj():
    igra = ugotovi_igro()
    if not igra.runda.stave_so_poravnane():
        return bottle.template("odigraj_krog.html", igra=igra)
    else:
        bottle.redirect("/celotna_runda/")


@bottle.post("/povisaj/")
def povisaj():
    igra = ugotovi_igro()

    vrednost = int(bottle.request.forms.getunicode("koliko"))
    igra.povisaj(vrednost)

    bottle.redirect("/odigraj_krog/")


@bottle.post("/check/")
def check():
    igra = ugotovi_igro()

    igra.check()

    bottle.redirect("/odigraj_krog/")


@bottle.post("/klici/")
def klici():
    igra = ugotovi_igro()

    igra.klici()

    bottle.redirect("/odigraj_krog/")


@bottle.post("/odstopi/")
def odstopi():
    igra = ugotovi_igro()

    igra.odstopi()

    bottle.redirect("/odigraj_krog/")


@bottle.get("/prekini_igro/")
def zbrisi_piskotek():
    bottle.response.delete_cookie(IME_PISKOTKA, path="/")
    bottle.redirect("/")


# Zaženi ---------------------------------------------------------------------

if __name__ == "__main__":
    # Zaženi spletni vmesnik.
    bottle.run(debug=True, reloader=True)