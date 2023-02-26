from shop import app, db


class Marcas(db.Model):
    id = db.Column(db.integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


class Categorias(db.Model):
    id = db.Column(db.integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


with app.app_context():
    db.create_all()
