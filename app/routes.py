import flask_login
from flask import Blueprint, render_template, flash, redirect, session, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from app.models import SignupForm, LoginForm, UserDB, ChangePasswordForm
from app.extensions import db
import requests
import os


main = Blueprint("main", __name__)
bcrypt = Bcrypt()

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/terms")
def terms():
    return render_template("terms.html")

@main.route("/privacy")
def privacy():
    return render_template("privacy.html")

@main.route("/cookies")
def cookies():
    return render_template("cookies.html")

@main.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    user = current_user  # Flask-Login ensures the user is logged in
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Check current password
        if not check_password_hash(user.password, form.current_password.data):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for('main.change_password'))

        # Update password
        user.password = generate_password_hash(form.new_password.data).decode('utf-8')
        db.session.commit()
        flash("Password successfully changed!", "success")
        return redirect(url_for('main.home'))

    return render_template('change_password.html', form=form)
@main.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form['email']
        password = request.form['password']
        postcode = request.form['postcode']
        address = request.form['address']
        terms = request.form['terms']
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        checkemail = UserDB.query.filter(UserDB.email == email).first()
        checkuser = UserDB.query.filter(UserDB.fname == fname).first()

        if not terms:
            flash("Please accept our terms to continue")

        if checkemail != None:
            flash("Please register using a different email.")

            return render_template("signup.html", subtitle="Register")
        elif checkuser is not None:
            flash("Username already exists !")

            return render_template("signup.html")

        else:
            new_customer = UserDB(fname=fname, lname=lname, email=email, password=hashed_password, postcode=postcode, address=address)
            db.session.add(new_customer)
            db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('signup.html')

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        customer = UserDB.query.filter_by(email=email).first()
        if customer and bcrypt.check_password_hash(customer.password, password):
    #    db.session["user_id"] = customer.id
            login_user(customer)
            return redirect(url_for('main.home'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('main.login'))
    return render_template('login.html', subtitle="Login")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "info")
    return redirect("/login")