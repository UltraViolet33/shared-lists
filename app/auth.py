from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from .forms import LoginForm
from .models.User import User
from .models.Task import Task
from app import limiter


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per hour")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("lists.index"))

    form = LoginForm()
    login_failed = False
    if request.method == "POST" and form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.is_password_correct(password):
            login_user(user, remember=True)
            return redirect(url_for("lists.index"))

        login_failed = True

    return render_template(
        "auth/login.html", form=form, user=current_user, login_failed=login_failed
    )


@auth.errorhandler(429)
def ratelimit_error(e):
    return {"error": 429}, 429


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
