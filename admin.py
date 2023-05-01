import json
from flask import *
from database import *
from  datetime import *
admin = Blueprint('admin', __name__)


@admin.route('/adminhome', methods=['get', 'post'],)
def adminhome():
    return render_template('adminhome.html')


@admin.route('/managerooms', methods=['get', 'post'],)
def managerooms():
    if 'submit' in request.form:
        rname = request.form['rname']
        status = request.form['status']
        q = "select * from rooms where room_name='%s' and room_status='%s'" % (
            rname, status)
        res = select(q)
        if len(res) > 0:
            flash("Already Exists")
        else:
            q = "insert into rooms values(null,'%s','%s')" % (rname, status)
            insert(q)
            flash("Room added")
    return render_template('admanage_rooms.html')


@admin.route('/viewdoctors', methods=['get', 'post'])
def viewdoctors():
    data = {}
    if 'action' in request.args:
        action = request.args['action']
        id = request.args['id']
        id1 = request.args['id1']
    else:
        action = None
    if action == "delete":
        q = "delete from login where login_id='%s'" % (id1)
        delete(q)
        q = "delete from doctors where doctor_id='%s'" % (id)
        delete(q)
        flash("Account Deleted")
        return redirect(url_for('admin.viewdoctors'))
    q = "SELECT *,CONCAT(first_name,' ',last_name)AS NAME FROM `doctors` inner join login using(login_id)"
    res = select(q)
    data['doc'] = res
    if 'id1' in request.args:
        id1 = request.args['id1']
        q = "UPDATE login SET usertype='Doctor' WHERE login_id='%s' AND usertype='Pending'" % id1
        update(q)
        return redirect(url_for('admin.viewdoctors'))
    elif 'id2' in request.args:
        id2 = request.args['id2']
        q = "UPDATE login SET usertype='Request Reject' WHERE login_id='%s' AND usertype='Pending'" % id2
        update(q)
        return redirect(url_for('admin.viewdoctors'))
    elif 'id3' in request.args:
        id3 = request.args['id3']
        q = "UPDATE login SET usertype='Pending' WHERE login_id='%s' AND usertype='Request Reject'" % id3
        update(q)
        return redirect(url_for('admin.viewdoctors'))
    return render_template('adview_doctors.html', data=data)


@admin.route('/manage_patients', methods=['get', 'post'])
def manage_patients():
    data = {}
    q = "select * from rooms"
    res = select(q)
    data['ro'] = res
    if 'submit' in request.form:
        rname = request.form['rname']
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        uname = request.form['uname']
        password = request.form['password']
        q = "select * from  rooms where room_name='%s'" % (rname)
        res = select(q)
        if len(res) > 0:
            flash("Already Reserved")
        else:
            q = "insert into login values(null,'%s','%s','patients')" % (
                uname, password)
            res = insert(q)
            q = "insert into patients values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                res, rname, fname, lname, age, gender, phone, email, address)
            insert(q)
            flash("Registered Successfully")
    return render_template('adminmanage_patients.html', data=data)


@admin.route('/viewpatients', methods=['get', 'post'])
def viewpatients():
    data = {}
    q = "select *,concat(first_name,' ',last_name)as NAME from patients inner join rooms using(room_id)"
    res = select(q)
    data['pa'] = res
    if 'action' in request.args:
        action = request.args['action']
        id = request.args['id']
        id1 = request.args['id1']
    else:
        action = None
    if action == "delete":
        q = "delete from login where login_id='%s'" % (id1)
        delete(q)
        q = "delete from patients where patient_id='%s'" % (id)
        delete(q)
        flash("Account Deleted")
        return redirect(url_for('admin.viewpatients'))
    return render_template('adview_patients.html', data=data)


@admin.route('/manage_pharmacy', methods=['get', 'post'])
def manage_pharmacy():
    if 'submit' in request.form:
        pname = request.form['pname']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        q = "select * from pharmacy where phar_name='%s'" % (pname)
        res = select(q)
        if len(res) > 0:
            flash("Already Exists")
        else:
            q = "insert into pharmacy values(null,'%s','%s','%s','%s')" % (
                pname, phone, email, address)
            insert(q)
            flash("Pharmacy Details Added")
    return render_template('admanage_pharmacy.html')


@admin.route('/view_pharmacy', methods=['get', 'post'])
def view_pharmacy():
    data = {}
    q = "select * from pharmacy"
    res = select(q)
    data['phar'] = res
    if 'action' in request.args:
        action = request.args['action']
        id = request.args['id']
    else:
        action = None
    if action == "delete":
        q = "delete from pharmacy where pharmacy_id='%s'" % (id)
        delete(q)
        flash("Details Deleted")
    return render_template('adview_pharmacy.html', data=data)


@admin.route('/view_feedbacks', methods=['get', 'post'])
def view_feedbacks():
    data = {}
    q="SELECT fm.*, CONCAT(IFNULL(p.first_name, d.first_name), ' ', IFNULL(p.last_name, d.last_name)) AS name, l.usertype FROM feed_mess fm LEFT JOIN patients p ON fm.fromid = p.login_id LEFT JOIN doctors d ON fm.fromid = d.login_id LEFT JOIN login l ON fm.fromid = l.login_id WHERE fm.toid = 1 ORDER BY fm.mess_id DESC"
    res = select(q)
    data['feed'] = res
    return render_template('adview_feedbacks.html', data=data)

@admin.route('/view_message',methods=['get','post'])
def view_message():
    data={}
    # ids=session['login_id']
    ids=request.args.get('from_id')
    name=request.args.get('n')
    user=request.args.get('u')
    data['name']=name
    data['user']=user
    # q="SELECT * FROM `feed_mess` WHERE 'toid' = '1' AND 'fromid' = '%s' or SELECT * FROM `feed_mess` WHERE 'toid' = '%s' AND 'fromid' = '1'"%(ids,ids)
    q="SELECT * FROM feed_mess WHERE (toid = '%s' AND fromid = 1) OR (toid = 1 AND fromid = '%s') ORDER BY mess_id ASC"%(ids,ids)
    res=select(q)
    data['fed_mes']=res
    if 'submit' in request.form:
        feed=request.form['feed']
        timenow = datetime.now()
        current_date = timenow.strftime("%Y-%m-%d")
        current_time = timenow.strftime("%H:%M:%S")
        q="INSERT INTO `feed_mess` (`mess_id`, `toid`, `fromid`, `date`, `time`, `message`, `flag`) VALUES (NULL, '%s', '1', '%s', '%s', '%s', NULL)"%(ids,current_date,current_time,feed)
        # # q="insert into feedback values(null,(select patient_id from patients where login_id='%s'),'%s',Curdate(),'pending')"%(ids,feed)
        insert(q)
        flash("Feedback added")
        
        return redirect('view_feedbacks')
    return render_template('adfeedbackView.html', data=data)

@admin.route('/add_medicine', methods=['get', 'post'])
def add_medicine():
    data = {}
    id = request.args['id']
    if 'submit' in request.form:
        mname = request.form['mname']
        des = request.form['des']
        aval = request.form['aval']
        cost = request.form['cost']
        q = "insert into medicines values(null,'%s','%s','%s','%s','%s')" % (
            id, mname, des, aval, cost)
        insert(q)
        flash("Medicines Added")
        return redirect(url_for('admin.view_pharmacy'))
    return render_template('admanage_medicine.html', data=data)


@admin.route('/view_orderedmedicine', methods=['get', 'post'])
def view_orderedmedicine():
    data = {}
    q = "SELECT *,CONCAT(first_name,' ',last_name)AS NAME FROM `prescription_details` INNER JOIN `prescription_master` USING(pm_id)INNER JOIN `medicines` USING(medicine_id)INNER JOIN patients USING(patient_id)"
    res = select(q)
    data['order'] = res
    if 'id' in request.args:
        id = request.args['id']
        q = "update prescription_master set  delivery_status='Order Accept'  where pm_id='%s' and delivery_status='pending'" % (
            id)
        update(q)
        return redirect(url_for('admin.view_orderedmedicine'))
    elif 'id1' in request.args:
        id1 = request.args['id1']
        q = "update prescription_master set  delivery_status='Order Reject'  where pm_id='%s' and delivery_status='pending'" % (
            id1)
        update(q)
        return redirect(url_for('admin.view_orderedmedicine'))
    return render_template('adminview_orderedmedicine.html', data=data)


@admin.route('/view_rooms', methods=['get', 'post'])
def view_rooms():
    data = {}
    q = "select * from rooms"
    res = select(q)
    data['ro'] = res
    if 'action' in request.args:
        action = request.args['action']
        id = request.args['id']
    else:
        action = None
    if action == "update":
        q = "select * from rooms where room_id='%s'" % (id)
        res = select(q)
        data['updateprt'] = res
    if 'update' in request.form:
        room_status = request.form['room_status']
        q = "update rooms set room_status='%s' where room_id='%s'" % (
            room_status, id)
        update(q)
        return redirect(url_for('admin.view_rooms'))
    return render_template("adminview_rooms.html", data=data)


@admin.route('/assign_doc', methods=['get', 'post'])
def assign_doc():
    data = {}
    q = "SELECT * FROM doctors"
    # assume that the `select()` function is defined elsewhere
    res = select(q)
    data['doc'] = res

    # if 'submit' in request.form:
    #     doc = int(request.form['doctor-name'])
    #     date = request.form['date-value']
    #     time = int(request.form['time-value'])
    #     q = "select * from assign_doc where doctor_id = '%s' and date = '%s' and time_slot = '%s' " % (
    #         doc, date, time)
    #     res = select(q)
    #     if res:
    #         flash("Already Added")
    #     else:
    #         q = "insert into assign_doc (doctor_id, date, time_slot) values ('%s','%s','%s')" % (
    #             doc, date, time)
    #         insert(q)
    #         flash("values are inserted")
    return render_template('adassign_doctors.html', data=data)

# assign_doc ajax urls are below
# first function date checking using doc_id


@admin.route('/admin_assign_doc_check_date', methods=['get', 'post'])
def admin_assign_doc_check_date():
    docId = request.form['doctor_id']
    date = request.form['date']
#  q="SELECT DISTINCT DATE(date) AS date FROM assign_doc WHERE doctor_id = '%s' AND DATE_FORMAT(date, '%i') DIV 3 = 0" %(docId)
    q = "select time_slot from assign_doc where doctor_id = '%s' and date = '%s' " % (
        docId, date)
    res = select(q)
    return (res)
@admin.route('/assignsave_doc', methods=['GET', 'POST'])
def assignsave_doc():
    try:
        docId = request.form['doctor_id']
        date = request.form['date']
        sel = request.form['select']
        q = "INSERT INTO assign_doc (doctor_id, date, time_slot) VALUES ('%s', '%s', '%s')" % (docId, date, sel)
        insert(q)
        return '1'
    except KeyError as e:
        return f'Error: {e}'


        # @admin.route('/save', methods=['get', 'post'])
        # def save():
        #     data = {}
        #     text = request.form['text']
        #     docId = request.form['docid']
        #     if request.files['file']:
        #      picfile = request.files['file']
        #      filename = 'static/images/dB_Images/dbImg'+picfile.filename
        #      picfile.save(filename)
        #      q="UPDATE `doctors` SET `profile_pic` = '%s' WHERE `doctors`.`doctor_id` = %s;" % (
        #         filename, docId)
        #      insert(q)
        #      q = "UPDATE `doctors` SET `specialization` = '%s' WHERE `doctors`.`doctor_id` = %s;" % (
        #         text, docId)
        #      insert (q)
        #      return "bothSuccess"
        #     else:
        #      q = "UPDATE `doctors` SET `specialization` = '%s' WHERE `doctors`.`doctor_id` = %s;" % (
        #         text, docId)
        #      insert (q)
        #      return "text"

        # in below save routing is the profile image save in doctor view section ajax code


@admin.route('/save', methods=['GET', 'POST'])
def save():
    data = {}
    text = request.form['text']
    docId = request.form['docid']

    if 'file' in request.files:
        picfile = request.files['file']
        filename = 'static/images/dB_Images/dbImg' + picfile.filename
        picfile.save(filename)

        q = "UPDATE `doctors` SET `profile_pic` = '%s' WHERE `doctors`.`doctor_id` = %s;" % (
            filename, docId)
        insert(q)

    q = "UPDATE `doctors` SET `specialization` = '%s' WHERE `doctors`.`doctor_id` = %s;" % (
        text, docId)
    insert(q)

    if 'file' in request.files:
        return "bothSuccess"
    else:
        return "text"

    # text=request.files['text']
    # docId=request.files['docId']
