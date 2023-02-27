from flask import render_template, redirect, url_for, flash, request, session
from shop import db, app, photos
from .models import Marcas, Categorias, Produtos
from .forms import AddProdutos
import secrets


@app.route('/addmarca', methods=['GET', 'POST'])
def addmarca():
    if 'email' not in session:
        flash(f'Por favor, faça o login antes.', 'success')
        return redirect(url_for('login'))
    
    if request.method == "POST":
        getmarca = request.form.get('marca')
        marca = Marcas(name=getmarca)
        db.session.add(marca)
        db.session.commit()
        flash(f"A marca {getmarca} foi cadastrada com sucesso", "success")

@app.route('/updatemarca/<int:id>', methods=['GET', 'POST'])
def updatemarca(id):
    if 'email' not in session:
        flash(f'Por favor, faça o login antes.', 'success')
        return redirect(url_for('login'))
    
    old_marca = Marcas.query.get_or_404(id)
    marca = request.form.get('marca')
    
    if request.method=='POST':
        old_marca.name = marca
        db.session.commit()

        flash(f"A marca {marca} foi atualizada com sucesso", "success")
        return redirect(url_for('marcas'))

    return render_template('/products/updateclassificacao.html', content=old_marca, escopo='updatemarca', title="Atualizar Marcas")

@app.route('/updatecategoria/<int:id>', methods=['GET', 'POST'])
def updatecategoria(id):
    if 'email' not in session:
        flash(f'Por favor, faça o login antes.', 'success')
        return redirect(url_for('login'))
    
    old_categoria = Categorias.query.get_or_404(id)
    categoria = request.form.get('categoria')
    
    if request.method=='POST':
        old_categoria.name = categoria
        db.session.commit()

        flash(f"A categoria {categoria} foi atualizada com sucesso", "success")
        return redirect(url_for('categorias'))

    return render_template('/products/updateclassificacao.html', content=old_categoria, escopo='updatecategoria', title="Atualizar Categorias")

@app.route('/addcategoria', methods=['GET', 'POST'])
def addcategoria():
    if 'email' not in session:
        flash(f'Por favor, faça o login antes.', 'success')
        return redirect(url_for('login'))
    
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
    if 'email' not in session:
        flash(f'Por favor, faça o login antes.', 'success')
        return redirect(url_for('login'))
    
    categorias = Categorias.query.all()
    form = AddProdutos(request.form)

    if request.method == "POST":

        name = form.name.data
        price= form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        description = form.description.data
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')
        img1 = photos.save(request.files.get('img1'), name=secrets.token_hex(10) + ".")
        img2 = photos.save(request.files.get('img2'), name=secrets.token_hex(10) + ".")
        img3 = photos.save(request.files.get('img3'), name=secrets.token_hex(10) + ".")
        produto = Produtos(name=name, price=price, discount=discount, stock=stock, colors=colors, description=description, marca_id=marca, categoria_id=categoria, img1=img1, img2=img2, img3=img3)

        db.session.add(produto)
        db.session.commit()

        flash(f"O produto {name} foi cadastrado com sucesso", "success")
        return redirect(url_for('admin'))

    return render_template('/products/addproduto.html', form=form, title="Cadastrar Produtos", marcas=marcas, categorias=categorias)
