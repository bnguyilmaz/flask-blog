from flask import *
import sqlite3
from datetime import datetime

app = Flask(__name__)

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

init_db()  # 📍 tabloyu oluşturur

# --------------------------
#   ROUTES
# --------------------------

@app.route('/')
def index():
    return "Database hazır!"

# ✍️ Writings sayfası
@app.route('/writings')
def writings():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    # Veritabanındaki tüm yazıları son eklenene göre getir
    cursor.execute("SELECT * FROM writings ORDER BY id DESC")
    writings = cursor.fetchall()

    conn.close()

    # writing[1] = title, writing[2] = content, writing[3] = date
    return render_template('writings.html', writings=writings)

# 🎵 Songs
@app.route('/songs')
def songs():
    return "Songs page coming soon!"

# 🎬 Movies
@app.route('/movies')
def movies():
    return "Movies page coming soon!"

# 📚 Books
@app.route('/books')
def books():
    return "Books page coming soon!"


# ➕ Add Writing (Form)
@app.route('/add-writing', methods=['GET', 'POST'])
def add_writing():
    password = request.args.get('pass')
    if password != "bengu123":
        return "Unauthorized access", 403

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

        return redirect(url_for('writings'))

    return render_template('add_writing.html')


if __name__ == "__main__":
    app.run(debug=True)
