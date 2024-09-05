from flask import Flask, render_template, request, redirect
from pymysql import MySQLError

from mysql import connection, create_tables

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/out")
def show():
    conn = connection()
    cur = conn.cursor()
    contacts = []

    try:
        cur.execute("SELECT * FROM agenda;")
        contacts = cur.fetchall()
    except MySQLError as e:
        print(e)
    finally:
        cur.close()
        conn.close()

    return render_template("out.html", contacts=contacts)

@app.route("/add", methods=["POST"])
def form():
    name = request.form["firstname"]
    lastName = request.form["lastname"]

    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO agenda (firstname, lastname) VALUES (%s, %s)", (name, lastName))
        conn.commit()
    except MySQLError as e:
        print(e)
        return "Error", 400
    finally:
        cursor.close()
        conn.close()

    return redirect("out")
if __name__ == "__main__":
    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS agenda(firstname TEXT, lastname TEXT);")
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


    app.run()
