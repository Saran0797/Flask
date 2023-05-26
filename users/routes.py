from flask import Blueprint, request, render_template, redirect, flash, url_for
from package import db
from flask_login import login_user, login_required, logout_user, current_user
from package.models import User, Post
from users.forms import RegistrationForm, LoginForm, UpdateAccountForm, Requestresetform, Resetpasswordform
from package import bcrypt
from users.utils import save_picture, send_reset_email

users = Blueprint("users", __name__)


@users.route("/register", methods=["post", "get"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.Password.data).decode("utf-8")
        user = User(username=form.Username.data, email=form.Email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in!', "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@users.route("/login", methods=["post", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.Email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.Password.data):
            login_user(user, remember=form.remember.data, duration=None)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        flash("Login Unsuccessful. Please Check your Email and Password!", "danger")
    return render_template("login.html", form=form)


@users.route("/logout", methods=["GET", "post"])
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/account", methods=["GET", "post"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.Picture.data:
            profile_picture = save_picture(form.Picture.data)
            current_user.image_file = profile_picture
        current_user.username = form.Username.data
        current_user.email = form.Email.data
        db.session.commit()
        flash("Your Account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.Username.data = current_user.username
        form.Email.data = current_user.email
    image_file = url_for("static", filename="profile_pic/" + current_user.image_file)
    return render_template("account.html", title="account", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=["GET", "post"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = Requestresetform()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.Email.data).first()
        send_reset_email(user)
        flash("Email has been sent for verification", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", form=form)


@users.route("/reset_password/<token>", methods=["GET", "post"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token=token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = Resetpasswordform()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.Password.data)
        User.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template("reset_token.html", form=form)
