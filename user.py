from flask import request, make_response, jsonify, render_template, Blueprint
from db_connector import get_koncerti


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
