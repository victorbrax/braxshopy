from flask import render_template, redirect, url_for, flash, request
from shop import db, app
from .models import Marcas, Categorias


@app.route('/addmarca', methods=['GET', 'POST'])
def addmarca():
    
    if request.method == "POST":
        getmarca = request.form.get('marca')
        marca = Marcas(name=getmarca)
        db.session.add(marca)
        db.session.commit()
        flash(f"A marca {getmarca} foi cadastrada com sucesso", "success")

        return redirect(url_for('addmarca'))
    return render_template('/products/addmarca.html', marcas='marcas', title="Cadastrar marcas")
