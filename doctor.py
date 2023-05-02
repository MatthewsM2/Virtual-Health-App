from flask import *
from database import *
doctor = Blueprint('doctor', __name__)


@doctor.route('/doctorhome', methods=['get', 'post'],)
def doctorhome():
    return render_template('doctor_home.html')


@doctor.route('/updatebooking_status', methods=['get', 'post'])
def updatebooking_status():
    data = {}
    ids = session['login_id']
    q = "SELECT `doctor_id` FROM `doctors` where login_id = %s" % (ids)
    res = select(q)
    docid = res[0].get('doctor_id')
    q = "SELECT booking.*, CONCAT(doctors.first_name, ' ', doctors.last_name) AS doctor_name, CONCAT(patients.first_name, ' ', patients.last_name) AS patient_name FROM booking INNER JOIN doctors ON booking.doctor_id = doctors.doctor_id INNER JOIN patients ON booking.patient_id = patients.login_id WHERE booking.doctor_id ='%s'" % (docid)
    # '" % (ids)
    res = select(q)
    data['book'] = res
    # if 'id' in request.args:
    #     id = request.args['id']
    #     q = "update booking set  status='Appoinment Accept'  where booking_id='%s' and status='Booked'" % (
    #         id)
    #     update(q)
    #     return redirect(url_for('doctor.updatebooking_status'))
    # elif 'id1' in request.args:
    #     id1 = request.args['id1']
    #     q = "update booking set  status='Appoinment Reject'  where booking_id='%s' and status='Booked'" % (
    #         id1)
    #     update(q)
    #     return redirect(url_for('doctor.updatebooking_status'))
    return render_template('doctorview_booking.html', data=data, ids=ids)


@doctor.route('/doctor_patients', methods=['get', 'post'])
def doctor_patients():
    data = {}
    pid = request.args['P_id']
    did = request.args['D_id']
    q = "SELECT booking.*, doctors.*, patients.*, CONCAT(doctors.first_name, ' ', doctors.last_name) AS doctor_name, CONCAT(patients.first_name, ' ', patients.last_name) AS patient_name FROM booking INNER JOIN doctors ON booking.doctor_id = doctors.doctor_id INNER JOIN patients ON booking.patient_id = patients.login_id WHERE booking.doctor_id = '%s' AND booking.patient_id = '%s'" % (did, pid)
    res = select(q)
    data['detailsBook'] = res
    bid=data['detailsBook'][0]['booking_id']
    q="SELECT * FROM `prescription_uptable` where bid = '%s'" %(bid)
    res=select(q)
    data['pres']=res
    return render_template('doctor_patientsView.html', data=data)


@doctor.route('/view_progress', methods=['get', 'post'])
def view_progress():
    data = {}
    ids = session['login_id']
    q = "SELECT *,CONCAT(`patients`.`first_name`,patients.`last_name`)AS PNAME,CONCAT(`doctors`.`first_name`,doctors.`last_name`)AS DNAME FROM `share_progress` INNER JOIN `patients` USING(patient_id)INNER JOIN `doctors` USING(doctor_id) WHERE doctors.login_id='%s'" % (ids)
    res = select(q)
    data['view'] = res
    return render_template('doctorview_progress.html', data=data)


@doctor.route('/add_prescription', methods=['get', 'post'])
def add_prescription():
    data = {}
    ids = session['login_id']
    id = request.args['id']
    q = "select * from medicines"
    res = select(q)
    data['me'] = res
    if 'submit' in request.form:
        mname = request.form['mname']
        quantity = request.form['quan']
        q = "insert into prescription values(null,'%s',(select doctor_id from doctors where login_id='%s'),'%s','%s',Curdate())" % (
            id, ids, mname, quantity)
        insert(q)
        flash("Prescription Added")
        return redirect(url_for('doctor.view_progress'))
    return render_template('doctoradd_prescription.html', data=data)


@doctor.route('/video', methods=['get', 'post'])
def video():
    return render_template('doctorjoin_video.html')


@doctor.route('/close', methods=['get', 'post'])
def close():
    ids = session['login_id']
    session.clear()
    return redirect(url_for('doctor.doctorhome', ids=ids))

# @doctor.route('/appo_update',methods=['get','post'])
# def appo_update():
#     bid=request.form['b_id']
#     status=request.form['status']
#     aDate=request.form['a_date']
#     link=request.form['link']
#     if status == 'j':
#         q="UPDATE `booking` SET `status` = 'Join' and SET 'a_date' = '%s' WHERE `booking`.`booking_id` = %s"%(aDate,bid)
#         if insert(q):
#             return("Success")
#         else:
#             return("error")
#     elif status == 'n':
#         q="UPDATE `booking` SET `status` = 'Reject' WHERE `booking`.`booking_id` = %s"%(bid)
#         if insert(q):
#             return("Success")
#         else:
#             return("error")
@doctor.route('/pres_save', methods=['POST'])
def pres_save():
        bid = request.form['bid']
        txt = request.form['txt']
        q = "SELECT * FROM `prescription_uptable` WHERE `bid` = '%s'" % bid
        res = select(q)
        if res is None:
            q = "INSERT INTO `prescription_uptable` (`pre_id`, `bid`, `txt`) VALUES (NULL, '%s', '%s')" % (
            bid, txt)
            insert(q)
            return "Success"
        else:
            q = "UPDATE `prescription_uptable` SET `txt` = '%s' WHERE `bid` = '%s'" % (
            txt, bid)
            update(q)
        return "Success"

@doctor.route('/appo_update', methods=['POST'])
def appo_update():
    bid = request.form.get('b_id')
    status = request.form.get('status')
    a_date = request.form.get('a_date')
    link = request.form.get('link')

    if status == 'j':
        q = "UPDATE `booking` SET `status` = 'Join', `a_date` = '%s' WHERE `booking`.`booking_id` = %s" % (
            a_date, bid)
        insert(q)
        return ("Success")
    elif status == 'n':
        q = "UPDATE `booking` SET `status` = 'Reject' WHERE `booking`.`booking_id` = %s" % (
            bid)
        insert(q)
        return ("Success")
    return

    # @doctor.route('/pres_save',methods=['POST'])
    # def pres_save():
    #     bid=request.form['bid']
    #     txt=request.form['txt']
    #     flash(txt)
    #     q="select * from `prescription_uptable` where 'bid' = '%s' "%(bid)
    #     res=select(q)
    #     if res == None:
    #         q="INSERT INTO `prescription_uptable` (`pre_id`, `bid`, `txt`) VALUES (NULL, '%s', '%s')"%(bid,txt)
    #         insert(q)
    #         return("Success")
    #     else:
    #         q="update `prescription_uptable` SET 'txt' = '%s' where bid = '%s'" %(txt,bid)
    #         update(q)
    #         return("Success")
    #     return
