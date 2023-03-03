from shop import app, db, photos
from datetime import datetime

class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id', ondelete='CASCADE'), nullable=False)
    marca = db.relationship('Marcas', backref=db.backref('marcas', lazy=True))
    
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id', ondelete='CASCADE'), nullable=False)
    categoria = db.relationship('Categorias', backref=db.backref('categorias', lazy=True))

    img1 = db.Column(db.String(150), nullable=False, default="image.jpeg")
    img2 = db.Column(db.String(150), nullable=False, default="image.jpeg")
    img3 = db.Column(db.String(150), nullable=False, default="image.jpeg")

    def __repr__(self):
        return '<Addproduto %r>' % self.name

class Marcas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


class Categorias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


with app.app_context():
    db.create_all()
