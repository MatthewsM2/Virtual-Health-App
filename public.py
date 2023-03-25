from flask import *
from database import *
public=Blueprint('public',__name__)

@public.route('/',methods=['get','post'],)
def index():
	return render_template('index.html')

@public.route('/login',methods=['get','post'])
def login():
	if 'submit' in request.form:
		uname=request.form['uname']
		password=request.form['password']
		q="select * from login where username='%s' and password='%s'" %(uname,password)
		result=select(q)
		if result:
			session['login_id']=result[0]['login_id']
			if result[0]['usertype']=="admin":
				flash("Login successfully")
				return redirect(url_for('admin.adminhome'))
			if result[0]['usertype']=="patients":
				flash("Login successfully")
				return redirect(url_for('user.userhome'))
			if result[0]['usertype']=="Doctor":
				flash("Login successfully")
				return redirect(url_for('doctor.doctorhome'))
			else:
				flash("Invalid Login Data")
		else:
			flash("invalid username and password")
	return render_template('login.html')


@public.route('/doctors_register',methods=['get','post'])
def doctors_register():
	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		qual=request.form['qual']
		phone=request.form['phone']
		email=request.form['email']
		gender=request.form['gender']
		uname=request.form['uname']
		password=request.form['password']
		q="select * from doctors where first_name='%s'"%(fname)
		res=select(q)
		if len(res)>0:
			flash("Already Exists")
		else:
			q="insert into login values(null,'%s','%s','Pending')"%(uname,password)
			res=insert(q)
			q="insert into doctors values(null,'%s','%s','%s','%s','%s','%s','%s')"%(res,fname,lname,qual,phone,email,gender)
			insert(q)
			flash("Registered successfully")
			return redirect(url_for('public.login'))
	return render_template('doctors_register.html')