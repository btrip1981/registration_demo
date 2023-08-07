from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

#config db
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'demo_registration'

mysql = MySQL(app)

# create app route for index
@app.route('/')
def index():
    return render_template('index.html')

# create app route for signup, submit data to database and redirect to dashboard
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (fname VARCHAR(255), lname VARCHAR(255), email VARCHAR(255), phone VARCHAR(255))")
        cur.execute("INSERT INTO users(fname, lname, email, phone) VALUES (%s,%s,%s,%s)", (fname, lname, email, phone))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('dashboard', fname=fname))

    return render_template('signup.html')

# create app route for dashboard and def user first name for personalized greeting
@app.route('/dashboard')
def dashboard():
    fname = request.args.get('fname', '')
    return render_template('dashboard.html', fname=fname)

if __name__ == "__main__":
    app.run()
