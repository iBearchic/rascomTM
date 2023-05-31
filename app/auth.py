from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from manage import User, db
from forms import LoginForm, RegisterForm

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    if request.method == "POST":
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash(f"Добро пожаловть в ITMS, {form.username.data}", 'success')
                return redirect(url_for('main.home'))
        flash('Invalid username or password', 'warning')
    return render_template('login.html', form=form)

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='scrypt')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'New user: {form.username.data} was created!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

