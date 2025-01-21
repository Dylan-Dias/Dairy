# In app.py
from DBConnection import Cow, db
import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
mail = Mail(app)

# PostgreSQL connection setup
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="Authentication",
        user="root",
        password="root"
    )
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Check if username already exists
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cur.fetchone()
        if existing_user:
            flash("Username already exists!", "danger")
            cur.close()
            conn.close()
            return redirect(url_for('register'))

        # Insert new user into the database
        hashed_password = generate_password_hash(password)
        cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        conn.commit()
        cur.close()
        conn.close()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM users WHERE username = %s', (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user:
            flash("No account found with that email address.", "danger")
            return redirect(url_for('forgot_password'))

        # Generate a secure token
        token = secrets.token_urlsafe(32)

        # Store the token in the database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE users SET reset_token = %s WHERE username = %s', (token, email))
        conn.commit()
        cur.close()
        conn.close()

        # Send the email
        reset_url = url_for('reset_password', token=token, _external=True)
        msg = Message('Password Reset Request', sender='your_email@gmail.com', recipients=[email])
        msg.body = f'Click the following link to reset your password: {reset_url}'
        mail.send(msg)

        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))

    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('reset_password', token=token))

        # Validate the token and update the password
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM users WHERE reset_token = %s', (token,))
        user = cur.fetchone()

        if not user:
            flash("Invalid or expired token.", "danger")
            cur.close()
            conn.close()
            return redirect(url_for('forgot_password'))

        hashed_password = generate_password_hash(password)
        cur.execute('UPDATE users SET password = %s, reset_token = NULL WHERE id = %s', (hashed_password, user['id']))
        conn.commit()
        cur.close()
        conn.close()

        flash("Your password has been reset successfully. You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('reset_password.html', token=token)

@app.route('/index')
def index():
    return app.send_static_file('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/homescreen')
def homescreen():
    return render_template('Homescreen.html')


@app.route('/insights')
def insights():
    return render_template('Insights.html')

@app.route('/schedules')
def schedules():
    return render_template('Schedules.html')

@app.route('/api/data')
def get_data():
    data = [
        {"id": 1, "name": "Cow 1"},
        {"id": 2, "name": "Cow 2"},
        {"id": 3, "name": "Cow 3"},
    ]
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)
