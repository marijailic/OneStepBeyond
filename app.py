import json
from flask import Flask, request, make_response, jsonify, render_template, url_for, redirect
from pony import orm
from datetime import datetime, date, time
from globalVars import defaultImgUrl

DB = orm.Database()

app = Flask(__name__)


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
                slika=slika if slika != None else defaultImgUrl,
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


# dodavanje koncerata - admin

@app.route("/admin/dodavanje-koncerata", methods=["POST", "GET"])
def dodavanje_koncerata():
    if request.method == "POST":
        try:
            json_request = {}
            for key, value in request.form.items():
                """
                if value == "":
                    json_request[key] = None
                else:
                    json_request[key] = value
                """

                json_request[key] = None if value == "" else value

        except Exception as e:
            response = {"response": str(e)}
            return make_response(jsonify(response), 400)
        response = add_koncert(json_request)
        if response["response"] == "Uspjesan unos koncerta!":
            return make_response(jsonify(response), 200)
        else:
            return make_response(jsonify(response), 400)
    else:
        return make_response(render_template("admin-dodavanje-koncerata.html"), 200)


# izlistavanje svih koncerata - admin

@app.route("/admin/svi-koncerti", methods=["GET"])
def svi_koncerti():
    if request.args:
        response = get_koncerti(request.args)
        if response["response"] == "Uspjesno dohvacanje!":
            return make_response(jsonify(response), 200)
        else:
            return make_response(jsonify(response), 400)
    else:
        response = get_koncerti()
        if response["response"] == "Uspjesno dohvacanje!":
            return make_response(render_template("admin-svi-koncerti.html", data=response["data"]), 200)
        else:
            return make_response(jsonify(response), 400)


# izlistavanje svih koncerata - naslovnica

@app.route("/", methods=["GET"])
def naslovnica():
    if request.args:
        response = get_koncerti(request.args)
        if response["response"] == "Uspjesno dohvacanje!":
            return make_response(jsonify(response), 200)
        else:
            return make_response(jsonify(response), 400)
    else:
        response = get_koncerti()
        if response["response"] == "Uspjesno dohvacanje!":
            return make_response(render_template("index.html", data=response["data"]), 200)
        else:
            return make_response(jsonify(response), 400)


@app.route("/")
def home():
    return redirect(url_for("naslovnica"))


if __name__ == "__main__":
    app.run(port=8080)
