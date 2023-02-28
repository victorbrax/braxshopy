from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, DecimalField, BooleanField, TextAreaField, validators 

class AddProdutos(Form):
    name = StringField('Nome :', [validators.DataRequired()])
    price = DecimalField('Preço :', [validators.DataRequired()])
    discount = IntegerField('Desconto :', [validators.DataRequired()])
    stock = IntegerField('Estoque :', [validators.DataRequired()])
    description = TextAreaField('Descrição :', [validators.DataRequired()])
    colors = TextAreaField('Cor :', [validators.DataRequired()])

    img1 = FileField('Imagem 1 :', validators=[FileRequired(), FileAllowed(['jpeg', 'jpg', 'png', 'gif'])])
    img2 = FileField('Imagem 2 :', validators=[FileRequired(), FileAllowed(['jpeg', 'jpg', 'png', 'gif'])])
    img3 = FileField('Imagem 3 :', validators=[FileRequired(), FileAllowed(['jpeg', 'jpg', 'png', 'gif'])])