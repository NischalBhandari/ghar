from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , PasswordField , IntegerField  
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField , DateField
from flask_wtf.file import FileField , FileRequired


class MyForm(FlaskForm):
	name=StringField('name',validators=[DataRequired()])
	email=StringField('email',validators=[DataRequired()])
	username=StringField('username', validators=[DataRequired()])
	password=PasswordField('password',validators=[DataRequired()])

class GharAdd(FlaskForm):
	location = StringField('location',validators=[DataRequired()])
	price = IntegerField('price')
	available = DateField('available' , format='%Y-%m-%d')
	username = StringField('username')
	photo = FileField('photo')


	# 	<form action="" method="POST" enctype="multipart/form-data">
	# 	<div class = "form-group">

	# 	<input type="text" placeholder="Location" name="location" value="{{request.form.location}}">
	# 	<input type="text" placeholder="Price" name="price" value="{{request.form.price}}">
	# 	<input type="text" placeholder="Username" name="username" value="{{request.form.username}}">
	# 	<input type="date" placeholder="Available" name="available" value="{{request.form.available}}">
	# 	<input type = "file" name="file">
	# </div>
	# 	<input class="btn btn-default" type="submit" value="Login">

	# </form>