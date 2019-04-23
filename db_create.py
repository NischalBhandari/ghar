from app import db
from models import GharBare, KaskoGhar,Perception
from datetime import date
from werkzeug.security import *
from werkzeug.utils import secure_filename
#create database and db tables 
db.drop_all()
db.create_all()

db.session.add(KaskoGhar(username="nischal",password=generate_password_hash("12345"),name="Nischal", email="niscalbhandari12@gmail.com"))
db.session.add(KaskoGhar(username="suman",password=generate_password_hash("12345"),name="suman" , email="suman@suman.com"))
db.session.add(KaskoGhar(username="om",password=generate_password_hash("omram"), name= "om" , email="om@om.com"))

# insert
db.session.add(GharBare("maitighar","3000","nischal",date.today(),1,"default.jpg",2))
db.session.add(GharBare("baneshwor","4000","gharti",date.today(),1,"default.jpg",3))
db.session.add(GharBare("Lalitpur","6000","gandaki",date.today(),3,"lalitpur.jpg",2))
db.session.add(GharBare("Bhaktapur","6000","Newar",date.today(),3,"index.jpg",1))


db.session.add(Perception(Likes=1,Views=1,ghar_ko=1))
db.session.add(Perception(Likes=2,Views=2,ghar_ko=2))
db.session.add(Perception(Likes=3,Views=3,ghar_ko=3))
db.session.add(Perception(Likes=3,Views=4,ghar_ko=4))


# commit changes
db.session.commit()