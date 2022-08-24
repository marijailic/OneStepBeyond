from flask import request, make_response, jsonify, render_template, Blueprint
from db_connector import add_koncert, get_koncerti, delete_koncert, patch_koncert


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
            return make_response(jsonify(response), 400)
        response = add_koncert(json_request)
        if response["response"] == "Uspjesan unos koncerta!":
            return make_response(jsonify(response), 200)
        else:
            return make_response(jsonify(response), 400)
    else:
        return make_response(render_template("admin-dodavanje-koncerata.html"), 200)


# izlistavanje svih koncerata


@admin.route("/admin/svi-koncerti", methods=["GET"])
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


# brisanje koncerata


@admin.route('/admin/brisanje-koncerta/<id>', methods=['POST', 'GET'])
def brisanje_koncerta(id):
    response = delete_koncert(id)
    if response["response"] == "Uspjesno izbrisan koncert!":
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(response), 400)


# !promjena podataka koncerta


@admin.route('/admin/promjena-podataka/<id>', methods=['POST', 'GET'])
def promjena_podataka(id):
    response = patch_koncert(id)
    if response["response"] == "Uspjesna promjena!":
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(response), 400)
