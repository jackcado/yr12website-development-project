if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template
import sqlite3   #for the database stuff

app = Flask(__name__)

DATABASE = "app.db"

@app.route('/')
def index():
    
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = "SELECT * FROM item" 
    cursor.execute(sql)
    results = cursor.fetchall() 
    db.close()    
    return render_template('index.html',results=results) 

if __name__ == "__main__":
    app.run(debug=True)