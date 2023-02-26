from flask import render_template, redirect, url_for, flash, request
from shop import db, app


@app.route('/addmarca', methods=['GET', 'POST'])
def addmarca():
    return render_template('/products/addmarca.html', title="Cadastrar marcas")
