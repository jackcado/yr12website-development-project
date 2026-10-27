"""Lizard Locator, to report sightings to DOC."""
from flask import Flask, render_template, request, flash, session, redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)


# Secret key for sessions and flash.
app.config['SECRET_KEY'] = "password123"


# Path and filename for database and upload folder.
DATABASE = "please.db"
UPLOAD_FOLDER = "yr12website-development-project/static/imageupload"


# Connects and query database.
def query_db(sql, args=(), one=False):
    """Connect and query.

    will retun one item if
    one=true and can accept
    arguments as tuple.
    """
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results


USERNAME = "admin"
PASSWORD = "admin"


# Homepage routes.
@app.route('/', methods=["GET", "POST"])
def index():
    """Redirects to homepage."""
    return render_template('index.html')


@app.route('/home')
def home():
    """Redirects to homepage."""
    return render_template('index.html')


# Signup route and inserts user info into database while hashing password.
# So it isn't stored in the database directly.
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign up form."""
    if request.method == "POST":

        username = request.form['username']

        password = request.form['password']

        hashed_password = generate_password_hash(password)

    # Checking here for unique username.
        sql = "SELECT * from user WHERE username = ?"
        user = query_db(sql=sql, args=(username,), one=True)
        if user:
            flash("Username already taken")
        else:
            # Create a query to insert their data.
            sql = "INSERT INTO user (username, password) VALUES (?, ?);"
            query_db(sql, (username, hashed_password))  # Execute the query.
            flash("Sign up successful")

    return render_template('signup.html')


# Login route.
# Checks if username and password hash match for a successful login.
@app.route('/login', methods=["GET", "POST"])
def login():
    """Log in form."""
    print(request.form)
    if request.method == "POST":
        # Getting username.
        username = request.form['username']
        password = request.form['password']

        # Checking here.
        sql = "SELECT * from user WHERE username = ?"
        user = query_db(sql=sql, args=(username,), one=True)
        if user:
            if check_password_hash(user[2], password):
                # Stores in session and redirects.
                session['user'] = user
                flash("Logged in successfully")
                return redirect('/')
            else:
                flash("Incorrect password")
        else:
            flash("User does not exist")

    return render_template('login.html')


# Logs user out, in nav bar.
@app.route('/logout')
def logout():
    """Delete current user from session."""
    session.pop('user', None)
    return redirect('/')


# Route and sql form to insert into database.
@app.route('/report', methods=["GET", "POST"])
def report():
    """Report form."""
    try:
        session['user']
    except KeyError:
        flash("Please login before reporting!")
        return redirect('/login')

    if request.method == "POST":

        username = request.form['username']

        location = request.form['location']

        speciesid = request.form['species']

        date = request.form['date']

        filename = request.files["file"].filename

        # Create a query to insert their data.
        sql = "INSERT INTO reports (location, username, speciesid, date, imagefilename) VALUES (?, ?, ?, ?, ?);"
        query_db(sql, (location, username, speciesid, date, filename))  # Execute the query.
        flash("Thank you for your report!")

    sql = "SELECT speciesid, commonname FROM species"
    results = query_db(sql)

    return render_template('report.html', species=results)


# Route to show all reports made.
# Can each be clicked on to lead to their own unique pages.
@app.route('/searchreports', methods=["GET", "POST"])
def searchreports():
    """Look through reports made."""
    sql = "SELECT species.commonname, reports.username, reports.location, reports.date, reports.reportid FROM reports LEFT JOIN species ON reports.speciesid = species.speciesid"
    results = query_db(sql)

    return render_template('searchreports.html', results=results)


# Dynamic route to show reports.
@app.route('/reports/<int:reportid>')
def reports(reportid):
    """Report form."""
    sql = "SELECT * FROM reports WHERE reportid=?"
    sql = f"SELECT species.commonname, reports.username, reports.location, reports.date, reports.reportid FROM reports LEFT JOIN species ON reports.speciesid = species.speciesid WHERE reportid={reportid}"

    reports = query_db(sql, one=True)
    return render_template('reports.html', reports=reports)


# Route for species finder, no sql as just displays.
@app.route('/speciesfinder')
def speciesfinder():
    """List of species with pictures. Just a redirect."""
    return render_template('speciesfinder.html')


# Inserts items into database.
@app.post('/add_item')
def add_item():
    """To insert into database."""
    # Get the form data from the request object like this.
    item = request.form['item_name']
    # Create a query to insert their data.
    file = request.files["file"]
    if file:
        file.save(UPLOAD_FOLDER+filename)
    sql = "INSERT INTO reports (imagefilename) VALUES (?);"
    query_db(sql, (file,))  # Execute the query.
    return redirect('/')  # Redirect back to the home page.


# 404 route when bad link.
@app.errorhandler(404)
def page_not_found(error):
    return render_template('/404.html', error=error), 404


# Runs with debug enabled.
if __name__ == "__main__":
    app.run(debug=True)
