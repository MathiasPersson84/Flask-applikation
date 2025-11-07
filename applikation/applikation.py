import os
import sqlite3
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import jwt

# === Ladda miljövariabler ===
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# === Initiera Flask ===
app = Flask(__name__)
app.secret_key = SECRET_KEY

# === Databas-funktioner ===
def get_db():
    conn = sqlite3.connect("database.db")
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        db.commit()

init_db()

# === Startsida (skyddad) ===
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', user=session['user'])

# === Registrering ===
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_pw = generate_password_hash(password)
        db = get_db()

        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            db.commit()
            flash("Registreringen lyckades! Du kan nu logga in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Användarnamnet finns redan.", "danger")

    return render_template('register.html')

# === Inloggning ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user[2], password):
            # Skapa JWT-token
            token = jwt.encode({
                "user": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, SECRET_KEY, algorithm="HS256")

            if isinstance(token, bytes):
                token = token.decode('utf-8')

            session['user'] = username
            session['token'] = token
            flash("Du är nu inloggad!", "success")
            return redirect(url_for('home'))
        else:
            flash("Fel användarnamn eller lösenord", "danger")

    return render_template('login.html')

# === Utloggning ===
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('token', None)
    flash("Du har loggat ut.", "info")
    return redirect(url_for('login'))

# === JWT-verifiering (test-endpoint) ===
@app.route('/verify')
def verify():
    token = session.get('token')
    if not token:
        return jsonify({"error": "Ingen token"}), 401

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"valid": True, "payload": payload})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token har gått ut"}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({"error": str(e)}), 401

# === Återställ lösenord (begäran) ===
@app.route('/reset', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        username = request.form['username']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user:
            return redirect(url_for('reset_password', username=username))
        else:
            flash("Användaren finns inte.", "warning")
            return redirect(url_for('reset_request'))

    return render_template("reset_request.html")

# === Återställ lösenord (nytt lösen) ===
@app.route('/reset/<username>', methods=['GET', 'POST'])
def reset_password(username):
    if request.method == 'POST':
        new_password = request.form['password']
        hashed_pw = generate_password_hash(new_password)
        db = get_db()
        db.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_pw, username))
        db.commit()
        flash("Lösenordet har uppdaterats! Du kan nu logga in.", "success")
        return redirect(url_for('login'))

    return render_template("reset_password.html", username=username)

# === Starta appen ===
if __name__ == "__main__":
    app.run(debug=True)
