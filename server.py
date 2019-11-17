from flask import Flask, render_template, url_for, request, redirect, session
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '0047'
app.config['MYSQL_DATABASE_DB'] = 'Test'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.secret_key = 'aks64_hsc'

mysql.init_app(app)
connection = mysql.connect()

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        cursor = get_cursor()
        username = request.form['username']
        password = request.form['password']
        cursor.execute("INSERT INTO Users(username, password)VALUES(%s, %s)",(username, password))
        connection.commit()
        cursor.close()
        return "Account created successfully! Login <a href='/login'>here</a>"
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        cursor = get_cursor()
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * from Users')
        users = cursor.fetchall()
        cursor.close()
        for user in users:
            if user[1]==username and user[2]==password:
                session['id'] = user[0]
                session['username'] = user[1]
                return render_template('home.html', user = user)
        return "<h3>Credentials not found</h3>"
    return render_template('login.html')

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        cursor = get_cursor()
        fullname = request.form['fullname']
        fathersname = request.form['fathersname']
        contactno = request.form['contactno']
        cursor.execute("UPDATE Users SET fullname = %s, fathersname = %s, contactno = %s where username = %s",(fullname, fathersname, contactno, session['username']))
        connection.commit()
        cursor.close()
        return redirect(url_for('data'))
    return render_template('update.html')

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('login'))

@app.route('/data')
def data():
    cursor = get_cursor()
    cursor.execute("SELECT * from Users where username = %s", (session['username']))
    userdata = cursor.fetchone()
    return render_template('data.html', userdata = userdata)

def get_cursor():
    global connection 
    return connection.cursor()


if __name__ == '__main__':
    app.run(debug=True)