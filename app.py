from flask import Flask, request, make_response, jsonify, render_template, url_for, redirect
from db_connector import get_koncerti


from admin import admin
from user import user


app = Flask(__name__)
app.register_blueprint(admin)
app.register_blueprint(user)


# naslovnica


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
