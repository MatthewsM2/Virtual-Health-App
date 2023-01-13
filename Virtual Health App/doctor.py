from flask import *
from database import *
doctor=Blueprint('doctor',__name__)

@doctor.route('/doctorhome',methods=['get','post'],)
def doctorhome():
	return render_template('doctor_home.html')

@doctor.route('/updatebooking_status',methods=['get','post'])
def updatebooking_status():
	data={}
	ids=session['login_id']
	q="SELECT *,CONCAT(`patients`.first_name,' ',patients.`last_name`)AS NAME,CONCAT(doctors.`first_name`,' ',doctors.`last_name`)AS DNAME FROM `booking` INNER JOIN patients USING(patient_id)INNER JOIN `doctors` USING(doctor_id) where doctors.login_id='%s'"%(ids)
	res=select(q)
	data['book']=res
	if 'id' in request.args:
		id=request.args['id']
		q="update booking set  status='Appoinment Accept'  where booking_id='%s' and status='Booked'"%(id)
		update(q)
		return redirect(url_for('doctor.updatebooking_status'))
	elif 'id1' in request.args:
		id1=request.args['id1']
		q="update booking set  status='Appoinment Reject'  where booking_id='%s' and status='Booked'"%(id1)
		update(q)
		return redirect(url_for('doctor.updatebooking_status'))
	return render_template('doctorview_booking.html',data=data,ids=ids)

@doctor.route('/view_progress',methods=['get','post'])
def view_progress():
	data={}
	ids=session['login_id']
	q="SELECT *,CONCAT(`patients`.`first_name`,patients.`last_name`)AS PNAME,CONCAT(`doctors`.`first_name`,doctors.`last_name`)AS DNAME FROM `share_progress` INNER JOIN `patients` USING(patient_id)INNER JOIN `doctors` USING(doctor_id) WHERE doctors.login_id='%s'"%(ids)
	res=select(q)
	data['view']=res
	return render_template('doctorview_progress.html',data=data)

@doctor.route('/add_prescription',methods=['get','post'])
def add_prescription():
	data={}
	ids=session['login_id']
	id=request.args['id']
	q="select * from medicines"
	res=select(q)
	data['me']=res
	if 'submit' in request.form:
		mname=request.form['mname']
		quantity=request.form['quan']
		q="insert into prescription values(null,'%s',(select doctor_id from doctors where login_id='%s'),'%s','%s',Curdate())"%(id,ids,mname,quantity)
		insert(q)
		flash("Prescription Added")
		return redirect(url_for('doctor.view_progress'))
	return render_template('doctoradd_prescription.html',data=data)

@doctor.route('/video',methods=['get','post'])
def video():
	return render_template('doctorjoin_video.html')

@doctor.route('/close',methods=['get','post'])
def close():
	ids=session['login_id']
	session.clear()
	return redirect(url_for('doctor.doctorhome',ids=ids))