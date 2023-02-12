import traceback

from flask import *
import psycopg2
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
CORS(app)
app.secret_key = "lmzfsildfxi78dfzydusy7dyf78dyfzs8odfmyos"

def db_connection():
    conn = psycopg2.connect(host='127.0.0.1', database='quiz_app', user='postgres', password='Shalish1998@')
    return conn

@app.route("/")
def index():
    try:
        if session['current_user']:
            return render_template("quiz.html", current_user=session['current_user'])
    except:
        return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    con=db_connection()
    cur= con.cursor()
    query='INSERT INTO public."user" (name,password,email) VALUES (%s,%s,%s)'
    try:
        cur.execute(query, (name,generate_password_hash(password),email))
        con.commit()
    except:
        return render_template("index.html",status=0,msg="Email Exist")

    return render_template("index.html", status=1,msg="Registered please Login:)")


@app.route("/login", methods=["POST"])
def log_in():
    email = request.form['email']
    password = request.form['pass_me']
    con = db_connection()
    cur = con.cursor()
    # query='select * from "user" where email=email'
    cur.execute('select * from "user" where "email"='+"'"+email+"'")
    data=cur.fetchall()
    if len(data)==0:
        return render_template("index.html", status=2, msg="Email Not Registered:(")
    else:
        if check_password_hash(data[0][3],password):
            session['current_user'] = current_user=data[0][2]
            return redirect(url_for('quiz_home',current_user=data[0][2]))
        else:
            return render_template("index.html", status=3, msg="Password InCorrect")

@app.route("/quiz_home")
def quiz_home():
    try:
        if session['current_user']:
            return render_template("quiz.html", current_user=session['current_user'])
    except:
        return redirect(url_for('index'))
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

