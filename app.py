from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)
DATABASE = "feedback.db"


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute(
        "CREATE TABLE IF NOT EXISTS feedback "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, message TEXT)"
    )
    db.commit()
    db.close()


@app.route("/", methods=["GET", "POST"])
def home():
    db = get_db()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()
        if name and message:
            db.execute(
                "INSERT INTO feedback (name, message) VALUES (?, ?)",
                (name, message),
            )
            db.commit()
            db.close()
            return redirect("/")

    feedback = db.execute(
        "SELECT id, name, message FROM feedback ORDER BY id DESC"
    ).fetchall()
    db.close()
    return render_template("index.html", feedback=feedback)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
