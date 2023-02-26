from flask import render_template, session, request, url_for
from shop import app, db


@app.route('/')
def home():
    return "Seja bem vindo ao sistema em Flask."


@app.route('/registro')
def registrar():
    return render_template('admin/registrar.html', title="Registro de Usuários")
