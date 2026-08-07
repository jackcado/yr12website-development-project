from flask import Flask, render_template, request, flash, session, redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.config['SECRET_KEY'] = "password123"

DATABASE = "please.db"

def query_db(sql,args=(),one=False):
    '''connect and query- will retun one item if one=true and can accept arguments as tuple'''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results


#routes
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        username = request.form['username']

        password = request.form['password']

        hashed_password = generate_password_hash(password)

        sql = "INSERT INTO users (username, password) VALUES (?, ?);"
        query_db(sql,(username, hashed_password))
        flash("Sign up Succsessful")

    return render_template('signup.html')

@app.route('/login')
def login():
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


@app.post('/add_item')
def add_item():
    item = request.form['item_name']
    sql = "INSERT INTO item (item) VALUES (?);"
    query_db(sql,(item,))
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)