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

    bottle.redirect("/igra/")


def ugotovi_igro():
    id = bottle.request.get_cookie(IME_PISKOTKA, secret=SKRIVNOST)
    if id is None or id not in igre:
        bottle.response.delete_cookie(IME_PISKOTKA, path="/")
        bottle.redirect("/")
    else:
        return igre[id]


@bottle.get("/igra/")
def igraj():
    igra = ugotovi_igro()
    return bottle.template("igra.html", igra=igra)


@bottle.post("/povisaj/")
def povisaj():
    igra = ugotovi_igro()

    vrednost = int(bottle.request.forms.getunicode("koliko"))
    igra.povisaj(vrednost)

    bottle.redirect("/igra/")


@bottle.post("/check/")
def check():
    igra = ugotovi_igro()

    igra.check()

    bottle.redirect("/igra/")


@bottle.post("/klici/")
def klici():
    igra = ugotovi_igro()

    igra.klici()

    bottle.redirect("/igra/")


@bottle.post("/odstopi/")
def odstopi():
    igra = ugotovi_igro()

    igra.odstopi()

    bottle.redirect("/igra/")


@bottle.get("/prekini_igro/")
def zbrisi_piskotek():
    bottle.response.delete_cookie(IME_PISKOTKA, path="/")
    bottle.redirect("/")


# Zaženi ---------------------------------------------------------------------

if __name__ == "__main__":
    # Zaženi spletni vmesnik.
    bottle.run(debug=True, reloader=True)
