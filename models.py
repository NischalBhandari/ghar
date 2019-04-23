from app import db
from sqlalchemy.sql import func
from datetime import date

ramroho = db.Table('ramroho',
	db.Column('user_id', db.Integer, db.ForeignKey('kaskoghar.id')),
	db.Column('post_id', db.Integer,db.ForeignKey('perception.id'))
	)


class KaskoGhar(db.Model):
	__tablename__="kaskoghar"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50),nullable=False)
	password = db.Column(db.String(100),nullable=False)
	name = db.Column(db.String(100),nullable=False)
	email = db.Column(db.String(100),nullable=True)
	ghar = db.relationship('GharBare', backref='owner')
	ramro_lagyo = db.relationship('Perception', secondary=ramroho, backref=db.backref('fanharu'))


class GharBare(db.Model):
	__tablename__="gharbare"

	id = db.Column(db.Integer, primary_key=True)
	location = db.Column(db.String(50),nullable=False)
	price = db.Column(db.Integer,nullable=False)
	username = db.Column(db.String(50), unique= True ,nullable=False)
	available = db.Column(db.Date,default=date.today(),nullable=False)
	ghar_image = db.Column(db.String(100),nullable=False,unique=False,default='default.jpg')
	storey = db.Column(db.Integer, nullable=True)
	owner_id = db.Column(db.Integer, db.ForeignKey('kaskoghar.id'))
	ramro = db.relationship('Perception',backref='likes',uselist=False)

	def __init__(self,location,price,username,available,owner_id,ghar_image,storey):
		self.location = location
		self.price = price
		self.username = username
		self.available = available
		self.owner_id=owner_id
		self.ghar_image=ghar_image
		self.storey = storey
	#	self.owner=owner

	def __repr__(self):
		return '{}--{}--{}--{}'.format(self.location,self.price,self.username,self.storey)



class Perception(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	Likes = db.Column(db.Integer,nullable=True)
	Views = db.Column(db.Integer,nullable=True)
	ghar_ko = db.Column(db.Integer,db.ForeignKey('gharbare.id'))



### many to many #######

#### create a association table ######

