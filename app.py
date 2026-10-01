from flask import Flask, render_template, request, flash, session, redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

#secret key for sessions and flash
app.config['SECRET_KEY'] = "password123"

#path and filename for database
DATABASE = "please.db"

#connects and query database
def query_db(sql,args=(),one=False):
    '''connect and query- will retun one item if one=true and can accept arguments as tuple'''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results


#index routes
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home')
def home():
    return render_template('index.html')

#signup route and inserts user info into database while hashing password so it isn't stored in the database directly
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == "POST":

        username = request.form['username']

        password = request.form['password']

        hashed_password = generate_password_hash(password)

        sql = "INSERT INTO user (username, password) VALUES (?, ?);"
        query_db(sql,(username, hashed_password))
        flash("Sign up Succsessful")

    return render_template('signup.html')

#login route. checks if username and password hash match for a successful login
@app.route('/login', methods=["GET","POST"])
def login():
    print(request.form)
    if request.method == "POST":
        #getting username
        username = request.form['username']
        password = request.form['password']

        #checking here
        sql = "SELECT * from user WHERE username = ?"
        user = query_db(sql=sql,args=(username,),one=True)
        if user:
            if check_password_hash(user[2],password):
                #stores in session
                session['user'] = user
                flash("Logged in successfully")
            else:
                flash("Incorrect password")
        else:
            flash("User does not exist")
    return render_template('login.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/searchreports')
def searchreports():
    return render_template('searchreports.html')

@app.route('/speciesfinder')
def speciesfinder():
    return render_template('speciesfinder.html')

#inserts items into database
@app.post('/add_item')
def add_item():
    item = request.form['item_name']
    sql = "INSERT INTO item (item) VALUES (?);"
    query_db(sql,(item,))
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)