from flask import Flask,url_for,request,render_template,redirect,session,flash,g,escape,jsonify,Response
from functools import wraps
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO , send , emit
#import sql alchemy for python3.6
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import *
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from forms import MyForm, GharAdd
from flask_pymongo import PyMongo
## for matplot lib ########
import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
##################################
import sqlite3
import json


def create_connection(db_file):
	conn = sqlite3.connect(db_file)
	print(sqlite3.version)
	return conn


UPLOAD_FOLDER = os.path.basename('static')




# to be able to import resources 
#if many modules are used then other than __name__ needs to be implemented
app = Flask(__name__)
app.secret_key="gharbar123"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



#define a database and the use of the database type
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ghardata.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:fiberoptics12@localhost/gharkhoj'
db = SQLAlchemy(app)
#app.config['SQLALCHEMY_ECHO'] = True
from models import *

#############For adding py mongo ################################
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo=PyMongo(app)
#############################################################



#from models import KaskoGhar,GharBare
#for getting api 
CORS(app)
socketio = SocketIO(app, manage_session=False)


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to Login First')
			return redirect(url_for('login'))
	return wrap


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def createhashedfile(filename):
	x=filename.rsplit('.',1)[0].lower()
	y=filename.rsplit('.',1)[1].lower()
	z=generate_password_hash(x)
	w=z+'.'+y
	print(w)
	return w
#create a route for the root page
@app.route('/')
def home():
	d=GharBare.query.all()
	print(d)
	return render_template('index.html',data=d)
# create route for the login page
#login page needs to be connected to the template folder 
@app.route('/login', methods=['GET','POST'])
def login():
	error=None
	data=[1,2,3,4]
	# data=db.session.query(GharBare).all()
	# db.session.flush()

	if request.method == 'POST':
### This is the original login without database ###
			POST_USERNAME= request.form['username']
			POST_PASSWORD = request.form['password']
			print(db.session)
			#Close the session so the old cache is removed of the database 
			db.session.close()
			c=db.session.query(KaskoGhar).filter_by(username=POST_USERNAME).first()
			print(db.session)
			# c = connection.execute("SELECT * FROM 'kaskoghar' WHERE username= val"),({'val' : POST_USERNAME})
			
			print(c)
			#connection.close()

			if(c):
				if (check_password_hash(c.password,POST_PASSWORD)):
			#print(c)
			# checks if query returns any value if it returns a valid value then the user is logged in else cannot login
				# to make the session logged in true

					session['logged_in'] = True
					session['username'] = c.username
					session['id']= c.id
					POST_PASSWORD=""
					POST_USERNAME=""

					return redirect(url_for('ghar'))
					# return redirect(url_for('ghar',user=request.form['username']))
	

				session.clear()
				error = 'Invalid password, Please try again'
				flash('Invalid password')
				POST_USERNAME=""
				POST_PASSWORD=""
				return redirect(url_for('login', error=error , data=data))
			return redirect(url_for('incorrect'))	
#	return "Welcome to Login Page for Ghar Khoj"
	return render_template('login.html',error=error,data=data)

#ROute to ghar page where username is a must
@app.route('/ghar')
@login_required
def ghar(user="default"):
	gharharu=db.session.query(GharBare).all()
	return render_template('ghar.html',user=session['username'],gharharu=gharharu)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	flash('you were just logged out')
	return redirect(url_for('home'))

@app.route('/timroghar')
@login_required
def timroghar():
	timrogharharu=db.session.query(GharBare).filter_by(username=session['username']).all()
	return render_template('myhome.html',timrogharharu=timrogharharu)


@app.route('/register',methods=['GET','POST'])
def register():
	form = MyForm()
	if form.validate_on_submit():
		# cur  = mysql.connection.cursor()
		# cur.execute("INSERT INTO kaskoghar(username,email,password,name) VALUES(%s,%s,%s,%s)",(form.username.data,form.email.data,form.password.data,form.name.data))
		# mysql.connection.commit()
		# cur.close()
		db.session.close()
		x = db.session.query(KaskoGhar).filter_by(username=form.username.data).first()
		if(x):
			flash('choose a different username ')
			return render_template('registration.html' , form=form)	
		formdata=KaskoGhar(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data), name=form.name.data)
		print(type(formdata))
		db.session.add(formdata)

		db.session.commit()
		print(db.session)
		return redirect(url_for('home'))
	return render_template	('registration.html', form=form)




@app.route('/gharjod',methods=['GET','POST'])
@login_required
def gharjod():
	form = GharAdd()
	if form.validate_on_submit():
		home_data= mongo.db.home
		f= form.photo.data
		username=form.username.data
		filename = secure_filename(f.filename)
		hashed_name=createhashedfile(filename)
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], hashed_name))
		db.session.add(GharBare(location=form.location.data, price=form.price.data, available=form.available.data, username=form.username.data ,ghar_image=hashed_name,owner_id=session['id'], storey=form.floor.data))
		db.session.commit()
		x=GharBare.query.filter_by(username=username).first()
		db.session.add(Perception(Likes=0,Views=0,ghar_ko=x.id))
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('add.html', form=form)


# @app.route('/gharjod',methods=['GET','POST'])
# @login_required
# def gharjod():
# 	form = GharAdd()
# 	if form.validate_on_submit():
# 		f= form.photo.data
# 		username=form.username.data
# 		filename = secure_filename(f.filename)
# 		hashed_name=createhashedfile(filename)
# 		f.save(os.path.join(app.config['UPLOAD_FOLDER'], hashed_name))
# 		db.session.add(GharBare(location=form.location.data, price=form.price.data, available=form.available.data, username=form.username.data ,ghar_image=hashed_name,owner_id=session['id']))
# 		db.session.commit()
# 		x=GharBare.query.filter_by(username=username).first()
# 		db.session.add(Perception(Likes=0,Views=0,ghar_ko=x.id))
# 		db.session.commit()
# 		return redirect(url_for('home'))
# 	return render_template('add.html', form=form)



@app.route('/start')
def start():
	d=GharBare.query.all()
	print(d)
	return render_template('start.html',data=d)


@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/show/<int:show_id>')
def show(show_id):
	n=GharBare.query.filter_by(id=show_id).first()
	return render_template('show.html' ,data=n)

@app.route('/detail/<int:ghar_id>', methods=['GET','POST'])
def detail(ghar_id):

	# if (request.method == 'POST' ):
	# 	if(request.form['LikeButton']==1):
	# 		db.session.close()
	# 		z = GharBare.query.filter_by(id=ghar_id).first()
	# 		w= KaskoGhar.query.filter_by(id=session['id']).first()
	# 		z.ramro.fanharu.append(w)
	# 		z.ramro.Likes+=1
	# 		db.session.commit()
	# 		return redirect(url_for('detail', ghar_id=ghar_id))
	if(request.method == 'POST' ):
		if(request.form['opinions'] != "0" and request.form['mydata'] == "0"):
			print(type(request.form['opinions']))
			comment_it = mongo.db.users

			findusers = comment_it.find_one({'post_id': ghar_id})
			print(type(findusers))
			if(findusers):
				comment_it.update({'_id':findusers['_id']},{ '$addToSet':
					{'comments':
					{'user': session['username'], 
					'comment': request.form['opinions']
					}
					}
					}
					)
			
			comment_it.insert({'post_id': ghar_id,  
				'comments': 
							[ {'user': session['username'], 
				'comment':request.form['opinions']
				
				}
				]
				}
				)
		#return redirect(url_for('detail', ghar_id=ghar_id))
		elif(request.form['opinions'] == "0" and request.form['mydata'] == "1"):
		#	print(request.form['mydata'])

			db.session.close()
			z = GharBare.query.filter_by(id=ghar_id).first()
			w= KaskoGhar.query.filter_by(id=session['id']).first()
			z.ramro.fanharu.append(w)
			z.ramro.Likes+=1
			db.session.commit()
			return redirect(url_for('detail', ghar_id=ghar_id))
		return redirect(url_for('detail', ghar_id=ghar_id))

	o = 0
	comments_query = mongo.db.users
	find_home = mongo.db.home
	these_homes = find_home.find_one({'ghar_id': 2 })
	these_home = these_homes['floor']
	m=KaskoGhar.query.filter_by(id=session['id']).first()

	n=GharBare.query.filter_by(id=ghar_id).first()
	found = comments_query.find_one({"post_id": ghar_id})
	print(found)
	print("found : "  ,these_homes)
	try:
		if(n.ramro in m.ramro_lagyo):
			o = 1
		else:
			o = 0
	except AttributeError:
		return redirect(url_for('detail', ghar_id=ghar_id))
	if(found):
		what=found['comments']
		print(what)
		return render_template('detail.html',data=n, person=m , ramrolagyokinai = o, what=what, home= these_home)
	return render_template('detail.html',data=n, person=m , ramrolagyokinai = o)


# @socketio.on('connected',namespace='/private')	
# def handledetails(ghar_id):
# 	o=0
# 	y=db.session.query(GharBare).filter_by(id=ghar_id).first()	
# 	y.ramro.Views+=1
# 	db.session.commit()
# 	emit('like_result',{'like1': y.ramro.Likes, 'like2' : y.ramro.Views},broadcast=True)

# 	# 	print("Here is the session id " ,request.sid)
# 	# 	x.ramro.Views+=1
# 	# 	db.session.commit()
# 	# print(test)
	
# @socketio.on('testlike', namespace='/private')
# def handleliked(test,ghar_id,person_id):
# 	o = 0
# 	z=db.session.query(GharBare).filter_by(id=ghar_id).first()
# 	#w=db.session.query(KaskoGhar).filter_by(id=person_id).first()
# 	z.ramro.fanharu.append(w)
# 	z.ramro.Likes+=1
	
# 	emit('like_result',{'like1': z.ramro.Likes, 'like2' : z.ramro.Views },broadcast=True)

# 	db.session.commit()



@app.route('/ghar/json/<int:ghar_id>')
def jsondata(ghar_id):
	x=GharBare.query.filter_by(id=ghar_id).first()
	return jsonify({'data': x.price})

#giving json data for the page ghar/id/detail.html #######
@app.route('/testjson')
def  testjson():
	return render_template('test.html')

#testing the ajax data which returns date and name ulto
@app.route('/process',methods=['GET','POST'])
def process():
	email = request.form['email']
	name = request.form['name']
	if (name and email):
		newName = name[::-1]
		return jsonify({'name': newName,'date': datetime.now()})
	return jsonify({'error': 'MIssing data!'})

#testing the json data from the page learn.html

@app.route('/jsonshow/<x>', methods=['GET','POST'])
def jsonshow(x):
	xes={}
	ras={}
	conn = create_connection("/home/nischal/Documents/search/tutorial/market.db")
	cur = conn.cursor()
	cur.execute("SELECT * FROM market WHERE sn=?",(x))
	rows = cur.fetchall()
	for count,i in enumerate(rows) :
		xes[count]={'id':i[0] ,'S.N':i[1], 'Traded_Companies':i[2], 'No_Of_Transaction':i[3], 'Max_Price':i[4],'Min_Price':i[5],'Closing_Price':i[6],'Traded_Shares':i[7],'Amount':i[8],'Previous_Closing':i[9],'Date_Time':i[10], 'rising':True }

	print(type(xes))
	print(xes)
	#return json.dumps(rows)

	return jsonify(xes)
@app.route('/datas/<ids>', methods=['GET'])
def datas(ids):
	conn = create_connection("/home/nischal/Documents/search/tutorial/market.db")
	cur = conn.cursor()
	cur.execute("SELECT * FROM market WHERE sn=?",(ids))
	i = cur.fetchone()
	temp=0
	temp = i[10].split('.')
	dates=str(temp[:1])
	return jsonify({'date': dates, 'closing' : i[5]})

#this is used to render learn.html
@app.route('/page')
def page():
	return render_template("learn.html")

@app.route('/lump')
def jump():
	error=None
	data=GharBare.query.all()
	try:
	#get the session id from flask as socketio has different session and they conflict with each other .
		x=session['id']
		@socketio.on('Like')
		def handleLike(ballot):
			Like = Perception(Likes=ballot,ghar_ko=x)
			db.session.add(Like)
			db.session.commit()
			result1=Perception.query.filter_by(Likes=2).count()
			result2=Perception.query.filter_by(Views=3).count()
			emit('like_results',{'like1': result1, 'like2' : result2},broadcast=True)
	#messages = ['Message one ', 'Message two ', 'MESSAGE THree']
		messages = History.query.all()
#	print("hello",escape(session['id']))
		return render_template("sockettest.html",messages=messages)
	except:
		return redirect(url_for('login'))
#handles the message on the message event
@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	message = History(message=msg)
	db.session.add(message)
	db.session.commit()
	send(msg, broadcast=True)


@app.route('/incorrect')
def incorrect():
	return render_template('incorrect.html')

@app.route('/mongotest', methods=['GET', 'POST'])
def mongotest():
	if request.method == 'POST':

		user = mongo.db.users
		findusers = user.find_one({'name': request.form['name']})
		print(type(findusers))
		if(findusers):
			user.update({'_id':findusers['_id']},{ '$addToSet':
				{'comments':
				{'user': session['username'], 
				'comment': request.form['opinions']
				}
				}
				}
				)
		user.insert({'name': request.form['name'], 
			'language': request.form['language'], 
			'ghar': request.form['ghar'] , 
			'comments': 
						[ {'user': session['username'], 
			'comment':request.form['opinions']
			
			}
			]
			}
			)
		return 'Added user'
	return render_template("mongoadd.html")

@app.route('/mongoget', methods=['GET', 'POST'])
def mongoget():
	if request.method == 'POST':
		x = request.form['search']
		user=mongo.db.users
		x = user.find_one({'comments': {'name': x} })
		y = x['comments']
		for f in y :
			print(f['user'])
			print(f['comment'])
		return render_template('comments.html', comment= y)
	return render_template('search.html')		

@app.route('/plot.png')
def plot_png():
	fig = create_figure()
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')

def create_figure():
	conn = create_connection("/home/nischal/Documents/search/tutorial/market.db")
	cur = conn.cursor()
	cur.execute("SELECT * FROM market WHERE sn=?",('2'))
	rows = cur.fetchall()
	dates = []
	closing =[]
	fig=Figure()
	axis = fig.add_subplot(1,1,1,facecolor="#AAAAAA")
	
	x = db.session.query(GharBare).all()

	for i in rows :
		temp=0
		print(i)
		temp = i[10].split('.')
		dates.append(str(temp[:1]))

		closing.append(i[5])
	print(type(dates))
	print(closing)
	ys = closing
	xs = dates
	# xs = range(len(price_list))
	#ys = [random.randint(1,50) for x in xs]
	axis.set_ylabel("min_price")

	axis.set_xlabel("dates")
	axis.tick_params(axis='x', labelrotation=10)
	axis.plot(xs,ys)
	axis.grid(b=True, which='minor', color='w',linewidth=0.75)
	axis.set_title("Market of xyz")
	return fig

@app.route('/vuetest')
def vuetest():
	return render_template('vuetest.html')

if __name__=='__main__':
	app.run(debug=True,host='0.0.0.0')
	#socketio.run(app,host='0.0.0.0', debug=True)
