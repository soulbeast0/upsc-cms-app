from flask import Flask, render_template, request
import sqlite3
import random

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
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
    return render_template("index.html", q=q)

@app.route('/submit', methods=['POST'])
def submit():
    selected = request.form['answer']
    correct = request.form['correct']

    if selected == correct:
        score = 2
        result = "Correct"
    else:
        score = -0.66
        result = "Wrong"

    return render_template("index.html", result=result, score=score)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
