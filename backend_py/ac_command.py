#!/usr/bin/python3 
from flask import Flask, render_template, request, redirect, url_for, jsonify, session  
from flask_login  import LoginManager, UserMixin,login_user,login_required, current_user
import os
import time
import json

app = Flask(__name__)
app.secret_key ='Binelui'
password = 'Catalin'
tempe = 0
umiditate =0
out_temp=0

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {'admin':{'password':'Catalin'}}

class User(UserMixin):
    def __init__(self, username):
        print('numele este : '+username)
        self.id=username

@login_manager.user_loader
def load_user(user_id):
 if user_id in users:
     return User(user_id)
 return None

@app.route('/')
@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method== 'POST':       
        pwd = request.form['pass']
        session['username'] = request.form['pass']
        if pwd == password:
            user = User('admin')
            login_user(user)
            return redirect(url_for('index'))
    return render_template("login.html")


@app.route('/index')
#@login_required
def index():
    if current_user.is_authenticated:
        with open("/home/pi/work/centrala/temp.json","r") as f2:
            data=json.load(f2)
            tempe = data["temp"]
            umiditate = data["hum"]
            out_temp = data["out_temp"]
            out_hum = data["out_hum"]
            out_cer = data["out_nebulozitate"]
            out_pres = data["out_presiune"]
            return render_template('index.html', temp = tempe, hum = umiditate, temp_out=out_temp, hum_out=out_hum, pres_out=out_pres, cer_out= out_cer)
    return "login failed"


@app.route('/settemp', methods=['POST'])
def setTemp():
    test=0;
    data = request.get_json()
    val = data.get('temp_val')
    print(val)
    temp = int (val)
    print(temp)
    if temp >=15 and  temp <=30:
        #data["setTemp"] = temp
        with open("/home/pi/work/centrala/temp.json", "r") as f:
            test = json.load(f)
        with open ("/home/pi/work/centrala/temp.json", "w") as f:
            print(test["setTemp"])
            test["setTemp"]= temp
            print(test["setTemp"])
            json.dump(test,f)
            
            return jsonify({"message":f"Temp is successfully set to {temp}!"})
    return jsonify({"message":f"Temp out of range be sure that is set between 15C and 30C!"})



@app.route('/get-data')
def get_data():
    with open("/home/pi/work/centrala/temp.json","r") as f4:
        data = json.load(f4);
        print(data["setTemp"])
        return jsonify({"setTemp":data["setTemp"], "setMode":data["modeType"]})

@app.route('/setMode', methods=['POST'])
def setMode():
    test =0
    data = request.get_json()
    mod = data.get('mode_Type')
    print(mod)
    if mod =='AC' or mod == 'CT':
        with open("/home/pi/work/centrala/temp.json", "r") as f:
          test = json.load(f)
          test["modeType"] = mod
        with open("/home/pi/work/centrala/temp.json", "w") as f:
          json.dump(test,f)
    return jsonify({"message":f"setat"})

@app.route('/ac/', methods = ['POST'])
def ac_control():
    data = request.get_json()
    val = data.get('val')
    if val == 'cool_on':
        os.system('irsend SEND_ONCE MY_AC COLD_ON_18')
        print(val)
    if val == 'cool_off':
        os.system('irsend SEND_ONCE MY_AC COLD_OFF_18')
        print(val)
    if val  == 'heat_on':
        os.system('irsend SEND_ONCE MY_AC HEAT_ON_23')
        print(val)
    if val == 'heat_off':
        os.system('irsend SEND_ONCE MY_AC HEAT_OFF_23')
        print(val)
    return jsonify({'message' : f"ac command'{val}' sent."})

if __name__ == '__main__':
    app.run(debug=True,host='192.168.50.247')
