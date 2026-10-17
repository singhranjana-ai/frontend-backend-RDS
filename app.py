
import os
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]


# Connect Flask backend to Amazon RDS
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ.get("DB_NAME", "studentdb"),
        port=3306,
        connection_timeout=5
    )


# GET: Show registration page
# POST: Save student details into RDS
@app.route("/", methods=["GET", "POST"])
def register_student():

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            flash("Please enter both name and email.", "error")
            return redirect(url_for("register_student"))

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO students (name, email)
                VALUES (%s, %s)
            """
            cursor.execute(query, (name, email))
            connection.commit()

            flash("Student registered successfully!", "success")

        except mysql.connector.Error:
            app.logger.exception("Failed to save student in RDS")
            flash("Unable to save student. Please check database connectivity.", "error")

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None and connection.is_connected():
                connection.close()

        return redirect(url_for("register_student"))

    return render_template("index.html")


# GET: Fetch student records from RDS
@app.route("/students", methods=["GET"])
def view_students():

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, name, email FROM students ORDER BY id DESC"
        )
        students = cursor.fetchall()

        return render_template("students.html", students=students)

    except mysql.connector.Error:
        app.logger.exception("Failed to fetch students from RDS")
        return "Unable to retrieve student records.", 500

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
