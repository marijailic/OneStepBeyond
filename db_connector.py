from pony import orm
from datetime import datetime, date, time
from global_vars import default_img


DB = orm.Database()


class Koncert(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    ime_izvodaca = orm.Required(str)
    opis = orm.Optional(str)
    slika = orm.Required(str)
    mjesto = orm.Required(str)
    datum = orm.Required(date)
    vrijeme = orm.Required(time)
    cijena = orm.Required(float)
    kreirano = orm.Required(datetime, sql_default='CURRENT_TIMESTAMP')
    #orm.composite_key(ime_izvodaca, mjesto, datum)


DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)


# dodavanje koncerata


def add_koncert(json_request):
    try:
        ime_izvodaca = json_request["ime_izvodaca"]
        opis = json_request["opis"]
        slika = json_request["slika"]
        mjesto = json_request["mjesto"]
        datum = json_request["datum"]
        vrijeme = json_request["vrijeme"]
        cijena = json_request["cijena"]
        with orm.db_session:
            Koncert(
                ime_izvodaca=ime_izvodaca,
                opis=opis if opis != None else "",
                slika=slika if slika != None else default_img,
                mjesto=mjesto,
                datum=datum,
                vrijeme=vrijeme,
                cijena=cijena
            )
            response = {"response": "Uspjesan unos koncerta!"}
            return response
    except Exception as e:
        return {"response": "Neuspjesan unos koncerta!", "error": str(e)}


# izlistavanje svih koncerata


def get_koncerti():
    try:
        with orm.db_session:
            result = orm.select(x for x in Koncert)[:]
            list_of_all = []
            for x in result:
                list_of_all.append(x.to_dict())
            response = {
                "response": "Uspjesno dohvacanje!",
                "data": list_of_all
            }
            return response
    except Exception as e:
        return {"response": "Neuspjesno izlistavanje!", "error": str(e)}


# !dohvacanje koncerta


def get_koncert(odabrani_koncert):
    try:
        with orm.db_session:
            result = Koncert.get(id=odabrani_koncert)
            result = result.to_dict()
            response = {"response": "Uspjesno dohvacanje!", "data": result}
            return response
    except Exception as e:
        return {"response": "Neuspjesno dohvacanje!", "error": str(e)}


# brisanje koncerata


def delete_koncert(odabrani_koncert):
    try:
        with orm.db_session:
            to_delete = Koncert.get(id=odabrani_koncert)
            to_delete.delete()
            response = {"response": "Uspjesno izbrisan koncert!"}
            return response
    except Exception as e:
        return {"response": "Neuspjesno brisanje koncerta!", "error": str(e)}


# promjena podataka koncerta


def patch_koncert(odabrani_koncert, json_request):
    try:
        with orm.db_session:
            to_update = Koncert.get(id=odabrani_koncert)
            to_update.ime_izvodaca = json_request["ime_izvodaca"]
            to_update.opis = json_request["opis"]
            to_update.slika = json_request["slika"]
            to_update.mjesto = json_request["mjesto"]
            to_update.datum = json_request["datum"]
            to_update.vrijeme = json_request["vrijeme"]
            to_update.cijena = json_request["cijena"]
            response = {"response": "Uspjesna promjena!"}
            return response
    except Exception as e:
        return {"response": "Neuspjesna promjena!", "error": str(e)}
