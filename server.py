"""Flask server for diary card app."""

from flask import Flask, session, request, flash, render_template, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "")
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """View function for homepage."""

    return render_template("login.html")


@app.route('/login')
def login():
    """Log user in."""

    email = request.args.get("email")
    password = request.args.get("password")

    print(email)
    print(password)

    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
