from flask import *
from database import *
public = Blueprint('public', __name__)


@public.route(
    "/",
    methods=["get", "post"],
)
def index():
    data = {}
    q = "SELECT * FROM doctors"
    res = select(q)
    data["doc"] = res
    q = "SELECT DISTINCT date FROM assign_doc WHERE date >= CURDATE()"
    res = select(q)
    data["days"] = res
    q = "SELECT DISTINCT time_slot FROM assign_doc WHERE date >= CURDATE()"
    res = select(q)
    data['time'] = res

    time = {"tim": []}
    for row in res:
        if row['time_slot'] == 809:  # replace with your condition
            time['tim'].append({'real': "08:00 Am - 09:00 Am", 'val': 809})
        elif row['time_slot'] == 1011:
            time['tim'].append({'real': "10:00 Am - 11:00 Am", 'val': 1011})
        elif row['time_slot'] == 1201:
            time['tim'].append({'real': "12:00 Pm - 01:00 Pm", 'val': 1201})
        elif row['time_slot'] == 203:
            time['tim'].append({'real': "02:00 Pm - 03:00 Pm", 'val': 203})
        elif row['time_slot'] == 405:
            time['tim'].append({'real': "04:00 Pm - 05:00 Pm", 'val': 405})
    # time_ranges = {
    # 809: "08:00 Am - 09:00 Am",
    # 1011: "10:00 Am - 11:00 Am",
    # 1201: "12:00 Pm - 01:00 Pm",
    # 203: "02:00 Pm - 03:00 Pm",
    # 405: "04:00 Pm - 05:00 Pm",
    # }

    # data = {"name_time": {}, "time": []}

    # q = "SELECT DISTINCT time_slot FROM assign_doc WHERE date >= CURDATE()"
    # res = select(q)

    # for row in res:
    #  if row["time_slot"] in time_ranges:
    #     real_time = time_ranges[row["time_slot"]]
    #     data["time"].append(real_time)

    return render_template("index.html", data=data, time=time)


@public.route('/login', methods=['get', 'post'])
def login():
    if 'submit' in request.form:
        uname = request.form['uname']
        password = request.form['password']
        q = "select * from login where username='%s' and password='%s'" % (
            uname, password)
        result = select(q)
        if result:
            session['login_id'] = result[0]['login_id']
            if result[0]['usertype'] == "admin":
                flash("Login successfully")
                return redirect(url_for('admin.adminhome'))
            if result[0]['usertype'] == "patients":
                flash("Login successfully")
                return redirect(url_for('user.userhome'))
            if result[0]['usertype'] == "Doctor":
                flash("Login successfully")
                return redirect(url_for('doctor.doctorhome'))
            else:
                flash("Invalid Login Data")
        else:
            flash("invalid username and password")
    return render_template('login.html')


@public.route('/doctors_register', methods=['get', 'post'])
def doctors_register():
    if 'submit' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
        qual = request.form['qual']
        phone = request.form['phone']
        email = request.form['email']
        gender = request.form['gender']
        uname = request.form['uname']
        password = request.form['password']
        q = "select * from doctors where first_name='%s'" % (fname)
        res = select(q)
        if len(res) > 0:
            flash("Already Exists")
        else:
            q = "insert into login values(null,'%s','%s','Pending')" % (
                uname, password)
            res = insert(q)
            q = "insert into doctors values(null,'%s','%s','%s','%s','%s','%s','%s')" % (
                res, fname, lname, qual, phone, email, gender)
            insert(q)
            flash("Registered successfully")
            return redirect(url_for('public.login'))
    return render_template('doctors_register.html')


@public.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    doctor = request.form.get('doctor')
    date = request.form.get('appointmentfor')
    time = request.form.get('time')
    q = "select * from `appo_booking` where date='%s' and time='%s' and doc_id='%s'" % (
        date, time, doctor)
    res = select(q)
    if len(res) > 5:
        flash("Appointment to this date and time is Over")
    else:
        q = "INSERT INTO appo_booking (name, email, doc_id, date, time) VALUES ( '%s', '%s', '%s', '%s', '%s' )" % (
            name, email, doctor, date, time)
        insert(q)
        flash("Appointment Approved")
    return redirect(url_for('public.index'))


@public.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('contact-name')
    email = request.form.get('contact-email')
    mobile_num = request.form.get('contact-number')
    message = request.form.get('contact-message')
    q = "INSERT INTO `messages` (`id`, `name`, `email`, `mob`, `message`) VALUES (NULL, '%s', '%s', '%s', '%s')" % (
        name, email, mobile_num, message)
    if (insert(q)):
     mes = "success"
    else:
     mes = "fail"
    return (mes)
