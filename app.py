
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "change-this-key-before-deployment"


@app.route("/", methods=["GET", "POST"])
def register_student():

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            flash("Please enter name and email.", "error")
        else:
            flash(f"Form received for {name}!", "success")

        return redirect(url_for("register_student"))

    return render_template("index.html")


@app.route("/students", methods=["GET"])
def view_students():
    return "<h1>Student records will be displayed here.</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
