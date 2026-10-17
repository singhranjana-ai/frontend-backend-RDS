
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "change-this-key-before-deployment"


@app.route("/", methods=["GET", "POST"])
def register_student():

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            flash("Please enter both name and email.", "error")
        else:
            # Database connection will be added in the next step
            print(f"Student received: {name}, {email}")
            flash(f"Form received successfully for {name}!", "success")

        return redirect(url_for("register_student"))

    # GET request displays the frontend
    return render_template("index.html")


@app.route("/students", methods=["GET"])
def view_students():
    return "<h2>Student records will be displayed here.</h2>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
