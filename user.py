from flask import request, make_response, jsonify, render_template, Blueprint
from db_connector import get_koncerti, get_koncert, search_koncerti
from send_email import send_email


user = Blueprint("user", __name__)


# izlistavanje svih koncerata


@user.route("/user/svi-koncerti", methods=["GET"])
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
            return make_response(render_template("user-svi-koncerti.html", data=response["data"]), 200)
        else:
            return make_response(jsonify(response), 400)


# dohvacanje koncerta


@user.route("/user/podaci-o-koncertu/<int:id>", methods=['GET'])
def podaci_koncert(id):
    response = get_koncert(id)
    if response["response"] == "Uspjesno dohvacanje!":
        return make_response(render_template("user-koncert.html", data=response["data"]), 200)
    else:
        return make_response(jsonify(response), 400)


# slanje e-maila


@user.route("/user/potvrda/<int:id>", methods=["POST", "GET"])
def slanje_potvrde(id):
    response = get_koncert(id)
    if response["response"] == "Uspjesno dohvacanje!":
        data = response["data"]
        send_email(data)
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(response), 400)


# pretraga

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
            return make_response(jsonify(response), 400)
        response = search_koncerti(json_request)
        if response["response"] == "Uspjesno dohvacanje!":
            return make_response(render_template("user-koncert.html", data=response["data"]), 200)
        else:
            return make_response(jsonify(response), 400)
    else:
        return make_response(render_template("user-pretraga.html"), 200)
