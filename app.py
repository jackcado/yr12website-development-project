from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DATABASE = "please.db"

def query_db(sql,args=(),one=False):
    '''connect and query- will retun one item if one=true and can accept arguments as tuple'''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    #return None if there is no result from the query
    #return the first item only if one=True
    #return the list of tuples if one=False
    return (results[0] if results else None) if one else results


#routes
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home')
def home():
    return render_template('index.html')

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

if __name__ == "__main__":
    app.run(debug=True)