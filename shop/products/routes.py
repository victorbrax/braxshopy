from flask import render_template, redirect, url_for, flash, request, session, current_app
from shop import db, app, photos
from .models import Marcas, Categorias, Produtos
from .forms import AddProdutos
import secrets
import os


def conferir_login():
    if 'email' not in session:
        flash(f'Por favor, faça o login antes.', 'success')
        return redirect(url_for('login'))


@app.route('/')
def home():
    pagina = request.args.get('pagina', 1, type=int)
    produtos = Produtos.query.filter(Produtos.stock > 0).paginate(page=pagina, per_page=1)
    marcas = Marcas.query.join(Produtos, (Marcas.id == Produtos.marca_id)).all()
    categorias = Categorias.query.join(Produtos, (Categorias.id == Produtos.categoria_id)).all()

    return render_template('products/index.html', produtos=produtos, marcas=marcas, categorias=categorias)


@app.route('/marca/<int:id>')
def get_marca(id):
    get_mar = Marcas.query.filter_by(id=id).first_or_404()
    pagina = request.args.get('pagina', 1, type=int)
    marca = Produtos.query.filter_by(marca=get_mar).paginate(page=pagina, per_page=1)
    categorias = Categorias.query.join(Produtos, (Categorias.id == Produtos.categoria_id)).all()
    marcas = Marcas.query.join(Produtos, (Marcas.id == Produtos.marca_id)).all()
    return render_template('/products/index.html', marca=marca, marcas=marcas, categorias=categorias, get_mar=get_mar, title="Add title dps")


@app.route('/addmarca', methods=['GET', 'POST'])
def addmarca():
    conferir_login()
    if request.method == "POST":
        getmarca = request.form.get('marca')
        marca = Marcas(name=getmarca)
        db.session.add(marca)
        db.session.commit()
        flash(f"A marca {getmarca} foi cadastrada com sucesso", "success")
    return render_template('/products/additems.html', escopo='marcas', title="Cadastrar Marcas")


@app.route('/addcategoria', methods=['GET', 'POST'])
def addcategoria():
    conferir_login()
    if request.method == "POST":
        getcategoria = request.form.get('categoria')
        categoria = Categorias(name=getcategoria)
        db.session.add(categoria)
        db.session.commit()
        flash(
            f"A categoria {getcategoria} foi cadastrada com sucesso", "success")

        return redirect(url_for('addcategoria'))
    return render_template('/products/additems.html', escopo='categorias', title="Cadastrar Categorias")


@app.route('/categoria/<int:id>')
def get_categoria(id):
    pagina = request.args.get('pagina', 1, type=int)
    get_cat = Categorias.query.filter_by(id=id).first_or_404()
    categoria = Produtos.query.filter_by(categoria=get_cat).paginate(page=pagina, per_page=1)
    categorias = Categorias.query.join(Produtos, (Categorias.id == Produtos.categoria_id)).all()
    marcas = Marcas.query.join(Produtos, (Marcas.id == Produtos.marca_id)).all()
    return render_template('/products/index.html',
                           categoria=categoria,
                           categorias=categorias,
                           marcas=marcas,
                           get_cat=get_cat,
                           title="Add title dps")


@app.route('/addproduto', methods=['GET', 'POST'])
def addproduto():
    marcas = Marcas.query.all()
    conferir_login()
    categorias = Categorias.query.all()
    form = AddProdutos(request.form)

    if request.method == "POST":

        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        description = form.description.data
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')

        img1 = photos.save(request.files.get('img1'),
                           name=secrets.token_hex(10) + ".")
        img2 = photos.save(request.files.get('img2'),
                           name=secrets.token_hex(10) + ".")
        img3 = photos.save(request.files.get('img3'),
                           name=secrets.token_hex(10) + ".")

        produto = Produtos(name=name, price=price, discount=discount, stock=stock, colors=colors,
                           description=description, marca_id=marca, categoria_id=categoria, img1=img1, img2=img2, img3=img3)

        db.session.add(produto)
        db.session.commit()

        flash(f"O produto {name} foi cadastrado com sucesso", "success")
        return redirect(url_for('addproduto'))

    return render_template('/products/addproduto.html', form=form, title="Cadastrar Produtos", marcas=marcas, categorias=categorias)


@app.route('/updatemarca/<int:id>', methods=['GET', 'POST'])
def updatemarca(id):
    conferir_login()
    old_marca = Marcas.query.get_or_404(id)
    marca = request.form.get('marca')

    if request.method == 'POST':
        old_marca.name = marca
        db.session.commit()

        flash(f"A marca {marca} foi atualizada com sucesso", "success")
        return redirect(url_for('marcas'))

    return render_template('/products/updateclassificacao.html', content=old_marca, escopo='updatemarca', title="Atualizar Marcas")


@app.route('/deletemarca/<int:id>', methods=['POST'])
def deletemarca(id):
    conferir_login()

    marca = Marcas.query.get_or_404(id)
    if request.method == 'POST':
        Produtos.query.filter_by(marca_id=marca.id).delete()
        db.session.delete(marca)
        db.session.commit()

        flash(f"A marca foi deletada com sucesso", "success")
        return redirect(url_for('admin'))
    flash(f"A marca {marca.name} não foi deletada", "warning")
    return redirect(url_for('admin'))


@app.route('/updatecategoria/<int:id>', methods=['GET', 'POST'])
def updatecategoria(id):
    conferir_login()
    old_categoria = Categorias.query.get_or_404(id)
    categoria = request.form.get('categoria')

    if request.method == 'POST':
        old_categoria.name = categoria
        db.session.commit()

        flash(f"A categoria {categoria} foi atualizada com sucesso", "success")
        return redirect(url_for('categorias'))

    return render_template('/products/updateclassificacao.html', content=old_categoria, escopo='updatecategoria', title="Atualizar Categorias")


@app.route('/deletecategoria/<int:id>', methods=['POST'])
def deletecategoria(id):
    conferir_login()

    categoria = Categorias.query.get_or_404(id)
    if request.method == 'POST':
        Produtos.query.filter_by(categoria_id=categoria.id).delete()
        db.session.delete(categoria)
        db.session.commit()

        flash(f"A categoria foi deletada com sucesso", "success")
        return redirect(url_for('admin'))
    flash(f"A categoria {categoria.name} não foi deletada", "warning")
    return redirect(url_for('admin'))


# Estudar mais depois
@app.route('/updateproduto/<int:id>', methods=['GET', 'POST'])
def updateproduto(id):
    conferir_login()
    marcas = Marcas.query.all()
    categorias = Categorias.query.all()
    produto = Produtos.query.get_or_404(id)
    form = AddProdutos(request.form)

    if request.method == "POST":
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')

        produto.marca_id = marca
        produto.categoria_id = categoria

        form.name.data = produto.name
        form.price.data = produto.price
        form.stock.data = produto.stock
        form.colors.data = produto.colors
        form.discount.data = produto.discount
        form.description.data = produto.description

        if request.files.get('img1'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                          "static/images/" + produto.img1))
                produto.img1 = photos.save(request.files.get(
                    'img1'), name=secrets.token_hex(10) + ".")
            except:
                produto.img1 = photos.save(request.files.get(
                    'img1'), name=secrets.token_hex(10) + ".")
        if request.files.get('img2'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                          "static/images/" + produto.img2))
                produto.img2 = photos.save(request.files.get(
                    'img2'), name=secrets.token_hex(10) + ".")
            except:
                produto.img2 = photos.save(request.files.get(
                    'img2'), name=secrets.token_hex(10) + ".")
        if request.files.get('img3'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                          "static/images/" + produto.img3))
                produto.img3 = photos.save(request.files.get(
                    'img3'), name=secrets.token_hex(10) + ".")
            except:
                produto.img3 = photos.save(request.files.get(
                    'img3'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash(
            f"O produto {produto.name} foi atualizado com sucesso", "success")
        return redirect('/')

    form.name.data = produto.name
    form.price.data = produto.price
    form.stock.data = produto.stock
    form.colors.data = produto.colors
    form.discount.data = produto.discount
    form.description.data = produto.description

    return render_template('/products/updateproduto.html',
                           form=form,
                           produto=produto,
                           categorias=categorias,
                           marcas=marcas,
                           title="Atualizar Produtos")


@app.route('/deleteproduto/<int:id>', methods=['POST'])
def deleteproduto(id):
    conferir_login()

    produto = Produtos.query.get_or_404(id)

    if request.method == 'POST':

        try:
            os.unlink(os.path.join(current_app.root_path,
                      "static/images/" + produto.img1))
            os.unlink(os.path.join(current_app.root_path,
                      "static/images/" + produto.img2))
            os.unlink(os.path.join(current_app.root_path,
                      "static/images/" + produto.img3))
        except Exception as e:
            print(e)

        db.session.delete(produto)
        db.session.commit()

        flash(f"O produto foi deletado com sucesso", "success")
        return redirect(url_for('admin'))
    flash(f"O produto {produto.name} não foi deletado", "warning")
    return redirect(url_for('admin'))
