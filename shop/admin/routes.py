from flask import render_template, session, request, url_for, flash, redirect
from shop import app, db, bcrypt
from .forms import RegistrationForm
from .models import User
import os


@app.route('/')
def home():
    return render_template("Página Administrativa")


@app.route('/registro', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        flash('Obrigado por Registrar', 'success')
        return redirect(url_for('home'))
    return render_template('admin/registrar.html', form=form, title="Página de Registros")
