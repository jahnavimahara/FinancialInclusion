from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
# import pickle
# import numpy as np
import MySQLdb.cursors
import re
    
app = Flask(__name__)
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('user.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)

# model = pickle.load(open('model.pkl', 'rb'))

# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     if request.method ==  'POST':
#         gender = request.form['gender']
#         married = request.form['married']
#         dependents = request.form['dependents']
#         education = request.form['education']
#         employed = request.form['employed']
#         credit = float(request.form['credit'])
#         area = request.form['area']
#         ApplicantIncome = float(request.form['ApplicantIncome'])
#         CoapplicantIncome = float(request.form['CoapplicantIncome'])
#         LoanAmount = float(request.form['LoanAmount'])
#         Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

#         # gender
#         if (gender == "Male"):
#             male=1
#         else:
#             male=0
        
#         # married
#         if(married=="Yes"):
#             married_yes = 1
#         else:
#             married_yes=0

#         # dependents
#         if(dependents=='1'):
#             dependents_1 = 1
#             dependents_2 = 0
#             dependents_3 = 0
#         elif(dependents == '2'):
#             dependents_1 = 0
#             dependents_2 = 1
#             dependents_3 = 0
#         elif(dependents=="3+"):
#             dependents_1 = 0
#             dependents_2 = 0
#             dependents_3 = 1
#         else:
#             dependents_1 = 0
#             dependents_2 = 0
#             dependents_3 = 0  

#         # education
#         if (education=="Not Graduate"):
#             not_graduate=1
#         else:
#             not_graduate=0

#         # employed
#         if (employed == "Yes"):
#             employed_yes=1
#         else:
#             employed_yes=0

#         # property area

#         if(area=="Semiurban"):
#             semiurban=1
#             urban=0
#         elif(area=="Urban"):
#             semiurban=0
#             urban=1
#         else:
#             semiurban=0
#             urban=0


#         ApplicantIncomelog = np.log(ApplicantIncome)
#         totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
#         LoanAmountlog = np.log(LoanAmount)
#         Loan_Amount_Termlog = np.log(Loan_Amount_Term)

#         prediction = model.predict([[credit, ApplicantIncomelog,LoanAmountlog, Loan_Amount_Termlog, totalincomelog, male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate, employed_yes,semiurban, urban ]])

#         # print(prediction)

#         if(prediction=="N"):
#             prediction="Not Approved"
#         else:
#             prediction="Approved"


#         return render_template("prediction.html", prediction_text="Your Loan is  {}".format(prediction))

#     else:
#         return render_template("prediction.html")

if __name__ == "__main__":
    app.run()
