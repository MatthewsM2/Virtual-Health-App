from flask import Flask
from public import public
from admin import admin
from user import user
from doctor import doctor
app=Flask(__name__)
app.secret_key="hai"
app.register_blueprint(public)
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(user,url_prefix='/user')
app.register_blueprint(doctor,url_prefix='/doctor')
app.run(debug=True,port=5000)
# app.run(host="0.0.0.0")