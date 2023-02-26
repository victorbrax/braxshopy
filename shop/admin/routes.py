from flask import render_template, session, request, url_for, flash, redirect
from shop import app, db
from .forms import RegistrationForm


@app.route('/')
def home():
    return "Seja bem vindo ao sistema em Flask."


@app.route('/registro', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # user = User(form.username.data, form.email.data,
        # form.password.data)
        # db_session.add(user)
        flash('Obrigado por Registrar')
        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form=form, title="Página de Registros")
