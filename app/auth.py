from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from .forms import LoginForm
from sqlalchemy.exc import IntegrityError
from .models.User import User
from . import db

auth = Blueprint("auth", __name__)


def new_user():
    user = User(username="admin", email="admin@gmail.com", password_plaintext="admin")
    user.save()

@auth.route("/")
@login_required
def home():
    return render_template("home.html", user=current_user)


@auth.route("/login", methods=["GET", "POST"])
def login():
    # new_user()
    if current_user.is_authenticated:
        return redirect(url_for("auth.home"))

    form = LoginForm()
    login_failed = False
    if request.method == "POST" and form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.is_password_correct(password):
            login_user(user)
            return redirect(url_for("auth.home"))

        login_failed = True


    return render_template("auth/login.html", form=form, user=current_user, login_failed=login_failed)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
