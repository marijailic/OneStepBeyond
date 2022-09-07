from sys import base_prefix
from flask import request, make_response, jsonify, render_template, Blueprint
from db_connector import add_koncert, get_koncerti, delete_koncert, patch_koncert, get_koncert


admin = Blueprint("admin", __name__)


# dodavanje koncerata


@admin.route("/admin/dodavanje-koncerata", methods=["POST", "GET"])
def dodavanje_koncerata():
    if request.method == "POST":
        try:
            json_request = {}
            for key, value in request.form.items():
                if value == "":
                    json_request[key] = None
                else:
                    json_request[key] = value
        except Exception as e:
            response = {"response": str(e)}
            return make_response(render_template("error.html", data=response["response"]), 400)
        response = add_koncert(json_request)
        if response["response"] == "Uspješan unos koncerta!":
            return make_response(render_template("success.html", data=response["response"]), 200)
        else:
            return make_response(render_template("error.html", data=response["response"]), 400)
    else:
        return make_response(render_template("admin-dodavanje-koncerata.html"), 200)


# izlistavanje svih koncerata


@admin.route("/admin/svi-koncerti", methods=["GET"])
def svi_koncerti():
    if request.args:
        response = get_koncerti(request.args)
        if response["response"] == "Uspješno dohvaćanje!":
            return make_response(render_template("success.html", data=response["response"]), 200)
        else:
            return make_response(render_template("error.html", data=response["response"]), 400)
    else:
        response = get_koncerti()
        if response["response"] == "Uspješno dohvaćanje!":
            return make_response(render_template("admin-svi-koncerti.html", data=response["data"]), 200)
        else:
            return make_response(render_template("error.html", data=response["response"]), 400)


# brisanje koncerata


@admin.route('/admin/brisanje-koncerta/<id>', methods=['POST', 'GET'])
def brisanje_koncerta(id):
    response = delete_koncert(id)
    if response["response"] == "Uspješno izbrisan koncert!":
        return make_response(render_template("success.html", data=response["response"]), 200)
    else:
        return make_response(render_template("error.html", data=response["response"]), 400)


# promjena podataka koncerta


@admin.route('/admin/promjena-podataka/<id>', methods=['POST', 'GET'])
def promjena_podataka(id):
    if request.method == "POST":
        try:
            json_request = {}
            for key, value in request.form.items():
                if value == "":
                    json_request[key] = None
                else:
                    json_request[key] = value
        except Exception as e:
            response = {"response": str(e)}
            return make_response(render_template("error.html", data=response["response"]), 400)
        response = patch_koncert(id, json_request)
        if response["response"] == "Uspješna promjena!":
            return make_response(render_template("success.html", data=response["response"]), 200)
        else:
            return make_response(render_template("error.html", data=response["response"]), 400)
    else:
        response = get_koncert(id)
        if response["response"] == "Uspješno dohvaćanje!":
            return make_response(render_template("admin-promjena-podataka.html", data=response["data"]), 200)
        else:
            return make_response(render_template("error.html", data=response["response"]), 400)


# statistika


@admin.route('/admin/statistika', methods=['GET'])
def podaci_graf():
    response = get_koncerti()
    data = response["data"]
    suma_pula, b_p, suma_zagreb, b_z = 0, 0, 0, 0
    for d in data:
        if d["mjesto"] == "Arena, 52 100 Pula":
            suma_pula += d["cijena"]
            b_p += 1
        else:
            suma_zagreb += d["cijena"]
            b_z += 1
    cijene = [suma_pula/b_p, suma_zagreb/b_z]
    gradovi = ["Pula", "Zagreb"]
    mjeseci = ["Siječanj", "Veljača", "Ožujak", "Travanj", "Svibanj", "Lipanj",
               "Srpanj", "Kolovoz", "Rujan", "Listopad", "Studeni", "Prosinac"]
    kolicine = [0] * len(mjeseci)
    for d in data:
        kolicine[d["datum"].month - 1] += 1
    if response["response"] == "Uspješno dohvaćanje!":
        return make_response(render_template("admin-statistika.html", x=gradovi, y=cijene, x2=mjeseci, y2=kolicine), 200)
    else:
        return make_response(render_template("error.html", data=response["response"]), 400)
