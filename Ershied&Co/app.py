from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyB9nMFheLwSZh4IQjAQl-lvdM9leyp4gS0",
  "authDomain": "ershiedco.firebaseapp.com",
  "databaseURL": "https://ershiedco-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "ershiedco",
  "storageBucket": "ershiedco.appspot.com",
  "messagingSenderId": "446550114941",
  "appId": "1:446550114941:web:6f6fa82512e63780a12714",
  "measurementId": "G-T0Y53Y12HG"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'




@app.route('/', methods=['GET', 'POST'])
def signin():
  if request.method == 'POST':
    print('post')
    email = request.form['email']
    password = request.form['password']
    try:
      login_session['user'] = auth.sign_in_with_email_and_password(email, password)
      return redirect(url_for('home'))
    except:
      print('error')
  return render_template('signin.htm')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == "POST":
        login_session['email']= request.form['email']
        login_session['password'] = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(login_session["email"], login_session["password"])
            user= {"email": request.form['email'],"password": request.form['password']}
            user = db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('home'))
        except:
            return render_template("signup.htm", error="problem")
    else:
        return render_template("signup.htm")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/about')
def about():
    return render_template("about.htm")




@app.route('/home')
def home():
    return render_template("home.htm")



@app.route('/contact')
def contact():
    return render_template("contact.htm")





if __name__ == '__main__':
    app.run(debug=True, port="5001")
