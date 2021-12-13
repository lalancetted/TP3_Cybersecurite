# Source : github.com/testdrivenio/csrf-example

from flask import Flask, Response, abort, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY="enoughIsEnough",
    FLAG="FLAG-11991199",
    FLAG_TWO="FLAG-22882288",
    FLAG_THREE="FLAG-33773377"
)

login_manager = LoginManager()
login_manager.init_app(app)

csrf = CSRFProtect()
csrf.init_app(app)


# database
users = [
    {
        "id": 1,
        "username": "test",
        "password": "test",
        "flag": app.config["FLAG"] + app.config["FLAG_TWO"],
        "balance": 2000,
    },
    {
        "id": 2,
        "username": "Kevin Mitnick",
        "password": "Kevin Mitnick",
        "flag": "DO NOT SEND YOUR PERSONAL INFORMATION ON THE INTERNET. IT IS COMMON SENSE.",
        "balance": 0,
    },
]


class User(UserMixin):
    ...


def get_user(user_id: int):
    for user in users:
        if int(user["id"]) == int(user_id):
            return user
    return None


@login_manager.user_loader
def user_loader(id: int):
    user = get_user(id)
    if user:
        user_model = User()
        user_model.id = user["id"]
        return user_model
    return None


@app.errorhandler(401)
def unauthorized(error):
    return Response("Login failed, i know your first flag, "+app.config["FLAG_THREE"]+". \n Go on test's account next!")
@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        flag = request.form.get("flag")

        for user in users:
            if user["username"] == username and user["password"] == password:
                user_model = User()
                user_model.id = user["id"]
                login_user(user_model)
                return redirect(url_for("you_got_hacked_haha"))
            else:
                return abort(401)

    return render_template("index.html")


@app.route("/you-got-hacked-haha", methods=["GET", "POST"])
@login_required
def you_got_hacked_haha():
    user = get_user(current_user.id)

    if request.method == "POST":
        amount = int(request.form.get("amount"))
        account = int(request.form.get("receiver"))
        flag = str(request.form.get("flag"))

        transfer_to = get_user(account)

        if amount <= user["balance"] and transfer_to:
            user["balance"] -= amount
            transfer_to["balance"] += amount

    return render_template(
        "accounts.html",
        balance=user["balance"],
        username=user["username"],
        flag=user["flag"]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5551, debug=True)