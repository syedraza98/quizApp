import traceback

from flask import *
import psycopg2
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
CORS(app)
app.secret_key = "lmzfsildfxi78dfzydusy7dyf78dyfzs8odfmyos"
# postgres://shalish:bwROkhzjHVRU0JHZHGVIRGQUSvS8HaXu@dpg-cfke1o5a49903fnhlj30-a.oregon-postgres.render.com/quiz_app_095d

def db_connection():
    # conn = psycopg2.connect(host='127.0.0.1', database='quiz_app', user='postgres', password='Shalish1998@')
    conn = psycopg2.connect(host="dpg-cfke1o5a49903fnhlj30-a.oregon-postgres.render.com", database="quiz_app_095d", user="shalish", password="bwROkhzjHVRU0JHZHGVIRGQUSvS8HaXu")
    return conn

@app.route("/")
def index():
    try:
        if session['current_user']:
            return render_template("dashboard.html", current_user=session['current_user'])
    except:
        return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    con=db_connection()
    cur= con.cursor()
    query=f'INSERT INTO public."user" (email, "name", "password") VALUES (%s,%s,%s)'
    try:
        cur.execute(query, (email, name,generate_password_hash(password)))
        con.commit()
    except Exception as e:
        return render_template("index.html",status=0,msg="Email Exist")
        # return traceback.format_exc()

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
            session['email'] = current_user = data[0][1]
            session['current_user'] = current_user=data[0][2]
            return redirect(url_for('dashboard',current_user=data[0][2]))
        else:
            return render_template("index.html", status=3, msg="Password InCorrect")

@app.route("/dashboard")
def dashboard():
    try:
        if session['current_user']:
            return render_template("dashboard.html", current_user=session['current_user'])
    except:
        return redirect(url_for('index'))
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

@app.route("/save_result/<score>")
def save_result(score):
    try:
        if session['current_user']:
            email = session['email']
            # score = request.form['score']
            con = db_connection()
            cur = con.cursor()
            query = f'INSERT INTO public."result" (email, "score") VALUES (%s,%s)'
            try:
                cur.execute(query, (email, score))
                con.commit()
                return {"msg":"Score Saved"}
            except Exception as e:
                return traceback.format_exc()
    except:
        return redirect(url_for('index'))

@app.route("/show_result")
def show_result():
    try:
        if session['current_user']:
            email = session['email']

            con = db_connection()
            cur = con.cursor()
            query = f'SELECT * FROM public."result" WHERE email ='+"'"+email+"'"
            try:
                cur.execute(query)
                data = cur.fetchall()
                return render_template("result.html", current_user=session['current_user'], data=data)
            except Exception as e:
                return traceback.format_exc()
    except:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

