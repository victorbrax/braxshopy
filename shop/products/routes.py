from flask import render_template, redirect, url_for, flash, request
from shop import db, app, photos
from .models import Marcas, Categorias
from .forms import AddProdutos


@app.route('/addmarca', methods=['GET', 'POST'])
def addmarca():
    
    if request.method == "POST":
        getmarca = request.form.get('marca')
        marca = Marcas(name=getmarca)
        db.session.add(marca)
        db.session.commit()
        flash(f"A marca {getmarca} foi cadastrada com sucesso", "success")

        return redirect(url_for('addmarca'))
    return render_template('/products/additems.html', escopo='marcas', title="Cadastrar Marcas")

@app.route('/addcategoria', methods=['GET', 'POST'])
def addcategoria():
    
    if request.method == "POST":
        getcategoria = request.form.get('categoria')
        categoria = Categorias(name=getcategoria)
        db.session.add(categoria)
        db.session.commit()
        flash(f"A categoria {getcategoria} foi cadastrada com sucesso", "success")

        return redirect(url_for('addcategoria'))
    return render_template('/products/additems.html', escopo='categorias', title="Cadastrar Categorias")

@app.route('/addproduto', methods=['GET', 'POST'])
def addproduto():
    marcas = Marcas.query.all()
    categorias = Categorias.query.all()
    form = AddProdutos(request.form)

    if request.method == "POST":
        photos.save(request.files.get('img1'))
        photos.save(request.files.get('img2'))
        photos.save(request.files.get('img3'))

    return render_template('/products/addproduto.html', form=form, title="Cadastrar Produtos", marcas=marcas, categorias=categorias)
