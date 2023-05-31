from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from manage import User, db
from forms import LoginForm, RegisterForm
import os

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash(f"Добро пожаловть в ITMS, {form.username.data}", 'success')
                return redirect(url_for('main.home'))
        flash('Неверный логин или пароль!', 'warning')
    return render_template('login.html', form=form)

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_key(form.secret_word):
            if form.validate_username(form.username):
                hashed_password = generate_password_hash(form.password.data, method='scrypt')
                new_user = User(username=form.username.data, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash(f'Новый пользователь: {form.username.data} успешно создан!', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash(f'Пользователь: {form.username.data} уже существует!', 'warning')
                return redirect(url_for('auth.signup'))
        else:
            flash(f"Неверный ключ доступа!", 'danger')
            return redirect(url_for('auth.signup'))

    return render_template('signup.html', form=form)

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

