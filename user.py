from flask import request, make_response, jsonify, render_template, Blueprint
from db_connector import get_koncerti, get_koncert, patch_koncert, search_koncerti
from send_email import send_email


user = Blueprint("user", __name__)


# izlistavanje svih koncerata


@user.route("/user/svi-koncerti", methods=["GET"])
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
            return make_response(render_template("user-svi-koncerti.html", data=response["data"]), 200)
        else:
            return make_response(render_template("error.html", data=response["response"]), 400)


# dohvacanje koncerta


@user.route("/user/podaci-o-koncertu/<int:id>", methods=['GET'])
def podaci_koncert(id):
    response = get_koncert(id)
    if response["response"] == "Uspješno dohvaćanje!":
        return make_response(render_template("user-koncert.html", data=response["data"]), 200)
    else:
        return make_response(render_template("error.html", data=response["response"]), 400)


# slanje e-maila


@user.route("/user/potvrda/<int:id>", methods=["POST", "GET"])
def slanje_potvrde(id):
    response = get_koncert(id)
    if response["response"] == "Uspješno dohvaćanje!":
        data = response["data"]
        if data["kolicina_karata"] == 0:
            response = {
                "response": "Nema više ulaznica za odabrani koncert!"}
            return make_response(render_template("error.html", data=response["response"]), 400)
        send_email(data)
        data["kolicina_karata"] -= 1
        patch_koncert(id, data)
        response = {
            "response": "Uspješna kupnja karte, potvrda poslana na mail!"}
        return make_response(render_template("success.html", data=response["response"]), 200)
    else:
        response = {"response": "Neuspješna kupnja ulaznice!"}
        return make_response(render_template("error.html", data=response["response"]), 400)


# pretraga koncerata


@user.route("/user/pretraga", methods=["POST", "GET"])
def pretrazi_koncerte():
    if request.method == "POST":
        try:
            json_request = {}
            for key, value in request.form.items():
                if value == '':
                    json_request[key] = None
                else:
                    json_request[key] = value
        except Exception as e:
            response = {"response": str(e)}
            return make_response(render_template("error.html", data=response["response"]), 400)
        response = search_koncerti(json_request)
        if response["response"] == "Uspješno dohvaćanje!":
            return make_response(render_template("user-koncert.html", data=response["data"]), 200)
        else:
            return make_response(render_template("error.html", data=response["response"]), 400)
    else:
        response = get_koncerti()
        if response["response"] == "Uspješno dohvaćanje!":
            return make_response(render_template("user-pretraga.html", data=response["data"]), 200)
        else:
            return make_response(render_template("error.html", data=response["response"]), 400)
