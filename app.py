from flask import Flask, render_template
import sqlite3   #for the database stuff

app = Flask(__name__)

#the path and filename for the database
DATABASE = "database.db"

#cool function to automatcally connect and query
def query_db(sql,args=(),one=False):
    '''connect and query- will retun one item if one=true and can accept arguments as tuple'''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    #return None if ther is no result from the query
    #return the first item only if one=True
    #return the list of tuples if one=False
    return (results[0] if results else None) if one else results


#routes go here
@app.route('/')
def index():
    results = query_db("SELECT * FROM item")  
    return render_template('index.html',results=results)

#this bit of code runs the app that we just made with debug on
if __name__ == "__main__":
    app.run(debug=True)