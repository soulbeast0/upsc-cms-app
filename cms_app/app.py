from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# ---------- DATABASE CONNECTION ----------
def get_db():
    return sqlite3.connect("database.db")


# ---------- CREATE TABLE ----------
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        question TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        answer TEXT
    )
    ''')

    conn.commit()
    conn.close()


# ---------- ADD SAMPLE DATA ----------
def add_sample_data():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM questions")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("""
        INSERT INTO questions (topic, question, option_a, option_b, option_c, option_d, answer)
        VALUES 
        ('Infectious', 'Which is first-line drug for TB?', 'Rifampicin', 'Isoniazid', 'Ethambutol', 'Pyrazinamide', 'B')
        """)

    conn.commit()
    conn.close()


# ---------- INIT DATABASE ON START (IMPORTANT) ----------
init_db()
add_sample_data()


# ---------- ROUTES ----------
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/get_question')
def get_question():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    q = cursor.fetchone()

    conn.close()

    if q is None:
        return "No questions found"

    return render_template("index.html", q=q)


@app.route('/submit', methods=['POST'])
def submit():
    selected = request.form.get('answer')
    correct = request.form.get('correct')

    if selected == correct:
        result = "Correct"
        score = 2
    else:
        result = "Wrong"
        score = -0.66

    return render_template("index.html", result=result, score=score)
