from flask import *
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key_123"  # session için gerekli anahtar

# Sabit kullanıcı bilgileri (tek kullanıcı için)
USERNAME = "bengu"
PASSWORD = "1234"

# -------------------------------
# DATABASE SETUP
# -------------------------------
def init_db():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS writings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT,
            content TEXT,
            date TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            director TEXT,
            content TEXT,
            date TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            content TEXT,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# -------------------------------
# ROUTES
# -------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/writings')
def writings():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM writings ORDER BY id DESC")
    writings = cursor.fetchall()
    conn.close()
    return render_template('writings.html', writings=writings)


# -------------------------------
# LOGIN & LOGOUT
# -------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            flash("Welcome back, Bengü!", "success")
            return redirect(url_for("writings"))
        else:
            flash("Wrong username or password.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    # geldiğin sayfayı referer'dan al
    previous_page = request.referrer or url_for("index")

    session.clear()
    flash("You have been logged out.", "info")

    # aynı sayfaya geri gönder
    return redirect(previous_page)


# -------------------------------
# ADD WRITING (Korumalı Alan)
# -------------------------------
@app.route('/add-writing', methods=['GET', 'POST'])
def add_writing():
    # 🔒 Giriş yapılmadıysa login sayfasına yönlendir
    if not session.get("logged_in"):
        flash("You must log in to add a new writing.", "warning")
        return redirect(url_for("login"))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO writings (title, content, date) VALUES (?, ?, ?)",
                       (title, content, date))
        conn.commit()
        conn.close()

        flash("Writing added successfully!", "success")
        return redirect(url_for('writings'))

    return render_template('add_writing.html')


# -------------------------------
# PLACEHOLDER PAGES
# -------------------------------
@app.route('/songs')
def songs():
    return "Songs page coming soon!"

@app.route('/movies')
def movies():
    return "Movies page coming soon!"

@app.route('/books')
def books():
    return "Books page coming soon!"


if __name__ == "__main__":
    app.run(debug=True)
