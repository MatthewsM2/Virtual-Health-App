from flask import *
from database import *
user=Blueprint('user',__name__)

@user.route('/userhome',methods=['get','post'],)
def userhome():
	return render_template('userhome.html')

@user.route('/video',methods=['get','post'])
def video():
	return render_template('userjoin_video.html')

@user.route('/close',methods=['get','post'])
def close():
	session.clear()
	return redirect(url_for('user.userhome'))

@user.route('/get_user',methods=['get','post'])
def get_user():
    class_id=request.args['class_id']
    print(class_id)
    q="select *,concat(first_name,' ',last_name)as NAME from users where login_id='%s'"%(class_id)
    result=select(q)
    print (result)
    return demjson.encode(result)


@user.route('/send_feedbacks',methods=['get','post'])
def send_feedbacks():
    ids=session['login_id']
    if 'submit' in request.form:
        feed=request.form['feed']
        q="insert into feedback values(null,(select patient_id from patients where login_id='%s'),'%s',Curdate(),'pending')"%(ids,feed)
        insert(q)
        flash("Send Feedback")
    return render_template('usersend_feedback.html')


@user.route('/view_reply',methods=['get','post'])
def view_reply():
    data={}
    ids=session['login_id']
    q="select *,concat(first_name,' ',last_name)as NAME from feedback inner join patients using(patient_id) where login_id='%s'"%(ids)
    res=select(q)
    data['feed']=res
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    if action=="delete":
        q="delete from feedback where feedback_id='%s'"%(id)
        delete(q)
        flash("Feedback Deleted")
        return redirect(url_for('user.view_reply'))
    return render_template('userview_reply.html',data=data)

@user.route('/view_myprofile',methods=['get','post'])
def view_myprofile():
    data={}
    ids=session['login_id']
    q="select *,concat(first_name,' ',last_name) as NAME from patients inner join rooms using(room_id) where login_id='%s'"%(ids)
    res=select(q)
    data['pa']=res
    return render_template('userview_myprofile.html',data=data)

@user.route('/search_doctors',methods=['get','post'])
def search_doctors():
    data={}
    if 'submit' in request.form:        
        name=request.form['name']
        q="select *,concat(first_name,' ',last_name)as NAME from doctors WHERE  doctors.first_name LIKE '%s'"%(name)
        res=select(q)
        data['viewsearch']=res
    return render_template('usersearch_doctors.html',data=data)

@user.route('/add_appionment',methods=['get','post'])
def add_appoinment():
    id=request.args['id']
    ids=session['login_id']
    if 'submit' in request.form:
        date=request.form['date']
        q="insert into booking values(null,(select patient_id from patients where login_id='%s'),'%s','%s','Booked')"%(ids,id,date)
        insert(q)
        flash("Booked Successfully")
        return redirect(url_for('user.search_doctors'))
    return render_template('userbook_appoinment.html')

@user.route('/share_progress',methods=['get','post'])
def share_progress():
    ids=session['login_id']
    id=request.args['id']
    if 'submit' in request.form:
        des=request.form['des']
        q="insert into share_progress values(null,(select patient_id from patients where login_id='%s'),'%s','%s',Curdate())"%(ids,id,des)
        insert(q)
        flash("Details Shared")
        return redirect(url_for('user.search_doctors'))
    return render_template('usershare_progress.html')

@user.route('/booking_status',methods=['get','post'])
def booking_status():
    data={}
    ids=session['login_id']
    q="SELECT *,CONCAT(`patients`.first_name,' ',patients.`last_name`)AS NAME,CONCAT(doctors.`first_name`,' ',doctors.`last_name`)AS DNAME FROM `booking` INNER JOIN patients USING(patient_id)INNER JOIN `doctors` USING(doctor_id) where patients.login_id='%s'"%(ids)
    res=select(q)
    data['book']=res
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    if action=="delete":
        q="delete from booking where booking_id='%s'"%(id)
        delete(q)
        flash("Booking Canceled")
        return redirect(url_for('user.booking_status'))
    return render_template('userview_bookingstatus.html',data=data)

@user.route('/view_prescription',methods=['get','post'])
def view_prescription():
    data={}
    ids=session['login_id']
    q="SELECT *,CONCAT(patients.`first_name`,' ',patients.`last_name`)AS PNAME,CONCAT(doctors.`first_name`,' ',doctors.`last_name`)AS DNAME FROM `prescription` INNER JOIN `share_progress` USING(progress_id) INNER JOIN patients USING(patient_id)INNER JOIN medicines USING(medicine_id)INNER JOIN doctors ON doctors.doctor_id = doctors.doctor_id where patients.login_id='%s'"%(ids) 
    res=select(q)
    data['pre']=res
    return render_template('userview_prescription.html',data=data)

@user.route('/search_medicine',methods=['get','post'])
def search_medicine():
    data={}
    if 'submit' in request.form:        
        name=request.form['name']
        q="SELECT * FROM `medicines` INNER JOIN `pharmacy` USING(pharmacy_id) WHERE  medicines.medicine_name LIKE '%s'"%(name)
        res=select(q)
        data['viewsearch']=res
    return render_template('usersearch_medicine.html',data=data)

@user.route('/add_cart',methods=['get','post'])
def add_cart():
    ids=session['login_id']
    id=request.args['id']
    if 'submit' in request.form:
        quantity=request.form['quantity']
        q="insert into cart values(null,(select patient_id from patients where login_id='%s'),'%s','%s')"%(ids,id,quantity)
        insert(q)
        flash("Quantity Added")
        return redirect(url_for('user.search_medicine'))
    return render_template('useradd_tocart.html')

@user.route('/buy_now',methods=['get','post'])
def buy_now():
    data={}
    ids=session['login_id']
    if 'submit' in request.form:
        q="select * from cart inner join patients using(patient_id) inner join medicines using(medicine_id) where patient_id=(select patient_id from patients where login_id='%s')"%(ids)
        res=select(q)
        flag=0
        t_amount=0
        quantity=0
        for range in res:
            medicine_id=range['medicine_id']
            quantity=range['quantity']
            costperunit=range['price']
            total_amount=int(quantity)*int(costperunit)
            # t_amount=t_amount+total_amount
            if flag==0:
                q="INSERT INTO `prescription_master` VALUES(NULL,(SELECT patient_id FROM patients WHERE login_id='%s'),CURDATE(),'pending','0')"%(ids)
                ids=insert(q)
                flag=1  
            q="insert into prescription_details values(null,'%s','%s','%s','%s','ordered')"%(ids,medicine_id,quantity,total_amount) 
            insert(q)
            q="update medicines set avilability=avilability-'%s' where medicine_id='%s'"%(quantity,medicine_id)
            update(q)
        q="update `prescription_master` set total_amount='%s' where pm_id='%s'"%(total_amount,ids)
        update(q)
        q="DELETE FROM cart WHERE patient_id=(SELECT patient_id FROM patients WHERE login_id='%s')"%(ids)
        delete(q)
        flash("Medicine Ordered")
        return redirect(url_for('user.search_medicine'))
    q="SELECT *,CONCAT(first_name, ' ',last_name) AS NAME FROM cart INNER JOIN patients USING(patient_id) INNER JOIN medicines USING(medicine_id)"
    res=select(q)
    data['carts']=res
    return render_template('userbuy_medicine.html',data=data)

@user.route('/delivery_status',methods=['get','post'])
def delivery_status():
    data={}
    ids=session['login_id']
    q="SELECT *,CONCAT(first_name,' ',last_name)AS NAME FROM `prescription_details` INNER JOIN `prescription_master` USING(pm_id)INNER JOIN `medicines` USING(medicine_id)INNER JOIN patients USING(patient_id) WHERE login_id='%s'"%(ids)
    res=select(q)
    data['order']=res
    return render_template('userview_deliverystatus.html',data=data)