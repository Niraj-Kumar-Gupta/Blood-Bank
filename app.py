
# import flast module
from flask import Flask, render_template, Response,request,redirect,url_for
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from flask import jsonify
from sqlalchemy import not_
 
# instance of flask application
app = Flask(__name__)


# database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'BJHGTY%$#%$Y%^&YIHUGTY^&*((*)(&*^%FTYGUHJIKO))'

db=SQLAlchemy(app)

login = LoginManager(app)
login.init_app(app)
@login.user_loader
def load_user(sno):
    return user.query.get(sno)


#database initilize
class user(UserMixin,db.Model):
        sno = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)
        age = db.Column(db.Integer(),nullable=False)
        location = db.Column(db.String(300), nullable=False)
        email = db.Column(db.String(100), nullable=False,unique=True)
        phone_number = db.Column(db.Integer(),nullable=False)
        address = db.Column(db.String(1000), nullable=False)
        username = db.Column(db.String(50), nullable=False,unique=True)
        password = db.Column(db.String(50),nullable=False)
        gender = db.Column(db.String(100),nullable=False)
        blood = db.Column(db.String(100),nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.now)

        def get_id(self):
         return self.sno
        

class newsletter(db.Model):
        sno = db.Column(db.Integer,primary_key=True)
        newsletter_email = db.Column(db.String(100),nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.now)
     
     

class blood_donate(db.Model):
        sno = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)
        blood = db.Column(db.String(100),nullable=False)
        dob = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), nullable=False)
        number = db.Column(db.Integer(),nullable=False)
        location = db.Column(db.String(50), nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.now)
        flag = db.Column(db.Integer,default="0")
        address_details = db.Column(db.Integer, nullable=False)


        def get_id(self):
         return self.sno


class blood_request(db.Model): 
    sno = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    blood = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer(),nullable=False)
    location = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    flag = db.Column(db.Integer,default="0")
    address_details = db.Column(db.Integer, nullable=False)

    def get_id(self):
         return self.sno   

class contact_form(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(100),nullable=False , unique=True)
    subject= db.Column(db.String(200),nullable=False)
    message = db.Column(db.String(500),nullable=False)

    def get_id(self):
         return self.sno 


@app.route('/check-email', methods=['POST'])
def checkemail():
    email = request.form.get('email')
    existing_user = user.query.filter_by(email=email).first()
    if existing_user:
        response = {'exists': True}
    else:
          response = {'exists': False}    
    return jsonify(response)


@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == "POST": 
        first_name = request.form['first_name']
        last_name =  request.form['last_name']
        age = request.form['age']
        location = request.form['location']
        email = request.form['email']
        phone_number = request.form['phone_number']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        gender = request.form['gender'] 
        blood = request.form['blood']
         
         # checking if username already exists
        usr = user.query.filter_by(username=username).first()
        if usr:
            return render_template("login.html", message="username already exists")
        else:
            eml = user.query.filter_by(email = email).first()
            if eml:
                return render_template("register.html", message="Email address Already exist")
            else:
                if password == confirm_password:
                    if len(password) > 5:
                        usr = user(first_name=first_name,last_name=last_name, age=age,location=location,
                                    email=email,phone_number=phone_number,address=address,username=username,password=password
                                ,gender=gender,blood=blood)
                        db.session.add(usr)  # adding user if not exists
                        db.session.commit()
                    #    user_object = user.query.filter_by( username=username).first()
                        # login new user
                        return render_template("login.html", message="Registration succesfull !")
                    else:
                        return render_template("register.html", message="password length is too short")
                else:
                    return render_template("register.html", message="password and confirm password are not same")      
   
    return render_template("register.html")




@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # checking if username already exists
        usr = user.query.filter_by(username=username,password=password).first()
        if usr:
            # user_object = user.query.filter_by( username=username).first()
            # return render_template("profile.html",message=user_object)
            login_user(usr)  # login that user
            return redirect("/")
        else:
            usr = user.query.filter_by(username=username).first()
            if usr:
              return render_template("login.html", message="Password Wrong!!")
            else:  
              return render_template("login.html", message="No such user exists !!")    
    return render_template("login.html")


#profile section ##

@app.route("/profile")
def profile(message=None):
    user= load_user(current_user.get_id())
    return render_template('profile.html',usr=user)
   

#profile section ##


#logout section
@login_required
@app.route("/logout")
def logout():
     logout_user()  # logout current user
     return redirect("/")
#logout section 
 

   # Admin
    # Admin
admin = Admin(app, name="data base", template_mode='bootstrap3')
admin.add_view(ModelView(user, db.session))
admin.add_view(ModelView(blood_donate, db.session))
admin.add_view(ModelView(blood_request, db.session))
admin.add_view(ModelView(newsletter, db.session))
admin.add_view(ModelView(contact_form, db.session))

    # Admin
    # Admin

# home route with no custom message
from collections import defaultdict
@app.route('/')
def home(message=None):
    user= load_user(current_user.get_id())
    if user:
        return render_template('index.html',usr=user)
    else:
        return render_template('index.html',usr=False)

# home page with custom message
@app.route('/new/<message>')
def home1(message):
    user= load_user(current_user.get_id())
    if user:
        return render_template('index.html',usr=user)
    else:
        return render_template('index.html',usr=False)
    
 

@app.route('/about')
def about():
    user= load_user(current_user.get_id())
    if user:
        return render_template('about.html',usr=user)
    else:
        return render_template('about.html',usr=False)

### Contact section start##
@app.route('/contact',methods=['GET','POST'])
def contact_section():
    if request.method=="POST":
        name = request.form['name']
        email=request.form['email']
        subject=request.form['subject']
        message=request.form['message']
        
        cont=contact_form(name=name,email=email,subject=subject,message=message)
        db.session.add(cont)
        db.session.commit()
        return render_template("contact.html",message="sucessfully sent !!!")

    return render_template("contact.html")   


    
    

# smtp mail protocol to send message #

@login_required
@app.route('/newsletter', methods=['GET','POST'])
def news_letter():
     if request.method == "POST":
         newsletter_email = request.form['newsletter_email']
         news=newsletter(newsletter_email=newsletter_email)
         db.session.add(news)  # adding user if not exists
         db.session.commit()
         return render_template("index.html",message=("congratulation !!" +" "+newsletter_email + " " +" is sucessfully Registered"))
     return render_template("index.html",message="Login Required")

###request blood
@app.route('/request')
def request_b():
    user= load_user(current_user.get_id())
    if user:
        req = blood_request.query.filter_by( first_name=user.first_name,email=user.email ).first()
        if req:
            flag = req.flag
            det=req.address_details
            details=blood_donate.query.filter_by(sno=det).first()
            return render_template("request_blood.html",exist=True,accept=flag,usr=user,details=details)
        else:
            return render_template("request_blood.html",exist=False,usr=user)
    else:
      return render_template("login.html",message="login required !!")


@login_required
@app.route("/request", methods=['GET','POST'])
def blood_request1():
     
   user= load_user(current_user.get_id())
   if user:
        if request.method == "POST": 
                first_name = request.form['first_name']
                last_name =  request.form['last_name']
                blood = request.form['blood']
                email = request.form['email']
                number = request.form['number']
                location = request.form['location']
                address_details=0
                req = blood_request(first_name=first_name,last_name=last_name,blood=blood,
                        email=email,number=number,location=location,address_details=address_details)
                db.session.add(req)  # adding user if not exists
                db.session.commit()
                req = blood_request.query.filter_by( first_name=first_name,email=email).first()
                if req:
                 return redirect("/request")
    
        


#### donate blood 
@app.route('/donate')
def donate():
   user= load_user(current_user.get_id())
   if user:
        req = blood_donate.query.filter_by( first_name=user.first_name,email=user.email ).first()
        if req:
            flag = req.flag
            det=req.address_details
            details=blood_request.query.filter_by(sno=det).first()
            return render_template("donate.html",exist=True,accept=flag,usr=user,details=details)
        else:
            return render_template("donate.html",exist=False,usr=user)
   else:
      return render_template("login.html",message="login required !!")

@login_required
@app.route("/donate", methods=['GET','POST'])
def donate_blood():
   user= load_user(current_user.get_id())
   if user:
        if request.method == "POST": 
                first_name = request.form['first_name']
                last_name =  request.form['last_name']
                blood = request.form['blood']
                dob = request.form['dob']
                email = request.form['email']
                number = request.form['number']
                location = request.form['location']
                address_details=0

                donate = blood_donate(first_name=first_name,last_name=last_name,blood=blood,dob=dob,
                        email=email,number=number,location=location,address_details=address_details)
                db.session.add(donate)  # adding user if not exists
                db.session.commit()
                req = blood_donate.query.filter_by( first_name=first_name,email=email).first()
                if req:
                 return redirect("/donate")
        
 
@login_required
@app.route('/notification')
def notify():
    return render_template("notification.html",users=blood_donate)
  

@app.route('/adminl')
def admin_login():
      # Fetch all blood donation records from the database
    return render_template("admin.html")

@app.route('/display_donar')
def display_donar():
    blood_donate_records = blood_donate.query.filter(not_(blood_donate.flag == 2)).all()
    return render_template("display_donar.html", blood_donate_records=blood_donate_records)

@app.route('/display_request')
def display_request():
    blood_request_records = blood_request.query.filter(not_(blood_request.flag == 2)).all()
    return render_template("display_request.html", blood_request_records=blood_request_records)

@app.route('/display_donar/<string:blood>', methods=['GET'])
def display_donar1(blood):
     request_list = blood_request.query.filter_by(blood=blood,flag=1).all()
     # Convert the request_list to a list of dictionaries
     request_list_data = [{'sno':request.sno,'first_name': request.first_name,'last_name': request.last_name, 'blood': request.blood, 'location': request.location,'email':request.email,'number':request.number} for request in request_list]
     return jsonify(request_list_data)

@app.route('/display_request/<string:blood>', methods=['GET'])
def display_request1(blood):
     request_list = blood_donate.query.filter_by(blood=blood,flag=1).all()
     # Convert the request_list to a list of dictionaries
     request_list_data = [{'sno':request.sno,'first_name': request.first_name,'last_name': request.last_name, 'blood': request.blood, 'location': request.location,'email':request.email,'number':request.number} for request in request_list]
     return jsonify(request_list_data)
    
### display_donar start ##
@app.route('/delete_request/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    record = blood_donate.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()
    return redirect('/display_donar')


@app.route('/accept_request/<int:record_id>', methods=['POST'])
def accept_request(record_id):
    record = blood_donate.query.get(record_id)
    if record:
        record.flag = True  # Assuming 'flag' is a boolean field indicating acceptance
        db.session.commit()
    return redirect('/display_donar')

@app.route('/details_send/<int:donar_id>', methods=['GET','POST'])
def details_send(donar_id):
    if request.method == "POST": 
       donar_id = donar_id
       select_request_1 = request.form['select_request_1']
       if donar_id and select_request_1:
         donar_database = blood_donate.query.get(donar_id)
         receiver_database= blood_request.query.get(select_request_1)
         donar_database.address_details=select_request_1
         receiver_database.address_details=donar_id
         donar_database.flag=2
         receiver_database.flag=2
         db.session.commit()
       print("Donor ID:", donar_id)
       print("Selected Request:", select_request_1)
    return redirect('/display_donar')
       
    


# request start ##
@app.route('/delete_request_receiver/<int:record_id>', methods=['POST'])
def delete_record_request(record_id):
    record = blood_request.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()
    return redirect('/display_request')


@app.route('/accept_request_receiver/<int:record_id>', methods=['POST'])
def accept_request_receiver(record_id):
    record = blood_request.query.get(record_id)
    if record:
        record.flag = True  # Assuming 'flag' is a boolean field indicating acceptance
        db.session.commit()
    return redirect('/display_request')

@app.route('/details_send1/<int:request_id>', methods=['GET','POST'])
def details_send1(request_id):
    if request.method == "POST": 
       request_id = request_id
       select_request_1 = request.form['select_request_1']
       if request_id and select_request_1:
         donar_database = blood_donate.query.get(select_request_1)
         receiver_database= blood_request.query.get(request_id)
         donar_database.address_details=request_id
         receiver_database.address_details=select_request_1
         donar_database.flag=2
         receiver_database.flag=2
         db.session.commit()
       print("Request ID:", request_id)
       print("Donar Request:", select_request_1)
    return redirect('/display_request')

if __name__ == '__main__': 
   app.run(debug=False,host="0.0.0.0",port="8000")
