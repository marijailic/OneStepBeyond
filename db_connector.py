from pony import orm
from datetime import datetime, date, time
from global_vars import default_img


DB = orm.Database()


class Koncert(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    ime_izvodaca = orm.Required(str)
    naziv_koncerta = orm.Required(str)
    opis = orm.Optional(str)
    slika = orm.Required(str)
    mjesto = orm.Required(str)
    datum = orm.Required(date)
    vrijeme = orm.Required(time)
    kolicina_karata = orm.Required(int)
    cijena = orm.Required(float)
    kreirano = orm.Required(datetime, sql_default='CURRENT_TIMESTAMP')
    #orm.composite_key(ime_izvodaca, mjesto, datum)


DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)


# dodavanje koncerata


def add_koncert(json_request):
    try:
        ime_izvodaca = json_request["ime_izvodaca"]
        naziv_koncerta = json_request["naziv_koncerta"]
        opis = json_request["opis"]
        slika = json_request["slika"]
        mjesto = json_request["mjesto"]
        datum = json_request["datum"]
        vrijeme = json_request["vrijeme"]
        kolicina_karata = json_request["kolicina_karata"]
        cijena = json_request["cijena"]
        with orm.db_session:
            Koncert(
                ime_izvodaca=ime_izvodaca,
                naziv_koncerta=naziv_koncerta,
                opis=opis if opis != None else "",
                slika=slika if slika != None else default_img,
                mjesto=mjesto,
                datum=datum,
                vrijeme=vrijeme,
                kolicina_karata=kolicina_karata,
                cijena=cijena
            )
            response = {"response": "Uspješan unos koncerta!"}
            return response
    except Exception as e:
        return {"response": "Neuspješan unos koncerta!", "error": str(e)}


# izlistavanje svih koncerata


def get_koncerti():
    try:
        with orm.db_session:
            result = orm.select(x for x in Koncert)[:]
            list_of_all = []
            for x in result:
                list_of_all.append(x.to_dict())
            response = {
                "response": "Uspješno dohvaćanje!",
                "data": list_of_all
            }
            return response
    except Exception as e:
        return {"response": "Neuspješno izlistavanje!", "error": str(e)}


# dohvacanje koncerta


def get_koncert(odabrani_koncert):
    try:
        with orm.db_session:
            result = Koncert.get(id=odabrani_koncert)
            result = result.to_dict()
            response = {"response": "Uspješno dohvaćanje!", "data": result}
            return response
    except Exception as e:
        return {"response": "Neuspješno dohvaćanje!", "error": str(e)}


# brisanje koncerata


def delete_koncert(odabrani_koncert):
    try:
        with orm.db_session:
            to_delete = Koncert.get(id=odabrani_koncert)
            to_delete.delete()
            response = {"response": "Uspješno izbrisan koncert!"}
            return response
    except Exception as e:
        return {"response": "Neuspješno brisanje koncerta!", "error": str(e)}


# promjena podataka koncerta


def patch_koncert(odabrani_koncert, json_request):
    try:
        with orm.db_session:
            to_update = Koncert.get(id=odabrani_koncert)
            to_update.ime_izvodaca = json_request["ime_izvodaca"]
            to_update.naziv_koncerta = json_request["naziv_koncerta"]
            to_update.opis = json_request["opis"] if json_request["opis"] != None else ""
            to_update.slika = json_request["slika"] if json_request["slika"] != None else default_img
            to_update.mjesto = json_request["mjesto"]
            to_update.datum = json_request["datum"]
            to_update.vrijeme = json_request["vrijeme"]
            to_update.kolicina_karata = json_request["kolicina_karata"]
            to_update.cijena = json_request["cijena"]
            response = {"response": "Uspješna promjena!"}
            return response
    except Exception as e:
        return {"response": "Neuspješna promjena!", "error": str(e)}


# pretrazivanje koncerata


def search_koncerti(json_request):
    try:
        with orm.db_session:
            result = list(orm.select(
                x for x in Koncert if str(getattr(x, "ime_izvodaca")) == json_request["item"]))[0]
            result_json = result.to_dict()
            response = {"response": "Uspješno dohvaćanje!",
                        "data": result_json}
            return response
    except Exception as e:
        return {"response": "Neuspješno dohvaćanje!", "error": str(e)}
