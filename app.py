from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Email settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "kellyawesome061@gmail.com"
app.config['MAIL_PASSWORD'] = "usxe wnzi tqot ppsy"
app.config['MAIL_DEFAULT_SENDER'] = "kellyawesome061@gmail.com"

mail = Mail(app)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("reviews.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  rating INTEGER,
                  message TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- ROUTES ---
@app.route("/")
def home():
    conn = sqlite3.connect("reviews.db")
    c = conn.cursor()
    c.execute("SELECT name, rating, message FROM reviews ORDER BY id DESC")
    reviews = [dict(name=row[0], rating=row[1], message=row[2]) for row in c.fetchall()]
    conn.close()
    return render_template("index.html", reviews=reviews)

@app.route("/send_message", methods=["POST"])
def send_message():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    msg = Message(
        subject=f"📩 New Contact Message from {name}",
        recipients=["kellyawesome061@gmail.com"],
        body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    )
    mail.send(msg)
    flash("✅ Your message was sent successfully!")
    return redirect("/")

@app.route("/add_review", methods=["POST"])
def add_review():
    name = request.form.get("name")
    rating = int(request.form.get("rating"))
    message = request.form.get("message")

    conn = sqlite3.connect("reviews.db")
    c = conn.cursor()
    c.execute("INSERT INTO reviews (name, rating, message) VALUES (?, ?, ?)", 
              (name, rating, message))
    conn.commit()
    conn.close()

    flash("✅ Review submitted successfully!")
    return redirect("/")

if __name__== "__main__":
    app.run(debug=True)