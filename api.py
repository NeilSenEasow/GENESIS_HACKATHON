from flask import Flask, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os, random


key = -1
if os.path.exists('secret.key'):
    f = open('secret.key')
    key = int(f.read())
    f.close()
else:
    key = int.from_bytes(random.randbytes(128))
    with open('secret_key', 'w') as f:
        f.write(str(key))
key = str(key)


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=key
)


def get_db():
    # Get an instance of the database
    con = sqlite3.connect('auth.db')
    con.row_factory = sqlite3.Row
    return con


def close_db(con):
    # Close the database
    con.close()


def is_valid_login_donor(email, password):
    # Check if the login is valid.
    if email is None:
        # If email is not provided, return 1
        return 1
    elif password is None:
        # If password is not provided, return 2
        return 2
    else:
        conn = get_db() # Get connection
        # Get user by email
        usr = conn.execute('SELECT * FROM donors WHERE email = ?', (email,)).fetchone()
        # Close the connection
        close_db(conn)
        if usr is None:
            # No user found
            return 3
        elif not check_password_hash(usr['password'], password):
            # Password mismatch
            return 4
        else:
            # Success
            return 0
        

def is_valid_login_volunteer(email, password):
    # Check if the login is valid.
    if email is None:
        # If email is not provided, return 1
        return 1
    elif password is None:
        # If password is not provided, return 2
        return 2
    else:
        conn = get_db() # Get connection
        # Get user by email
        usr = conn.execute('SELECT * FROM volunteers WHERE email = ?', (email,)).fetchone()
        # Close the connection
        close_db(conn)
        if usr is None:
            # No user found
            return 3
        elif not check_password_hash(usr['password'], password):
            # Password mismatch
            return 4
        else:
            # Success
            return 0
        

def create_donor(email, password, phone):
    # Create a user
    if email is None:
        # If no email is provided
        return 1
    elif password is None:
        # No password provided
        return 2
    
    conn = get_db() # Get connection
    try:
        # Try inserting a new record
        # The record is of the new user
        # If it fails, email-acc_type combination exists in database
        conn.execute("INSERT INTO donors (email, password, phone) VALUES (?, ?, ?)", (email, generate_password_hash(password), phone))
        conn.commit() # Save the change
    except conn.IntegrityError:
        # Violated uniqueness of email
        return 3
    # Close database
    close_db(conn)
    return 0 # Success


def create_volunteer(email, password, phone):
    # Create a user
    if email is None:
        # If no email is provided
        return 1
    elif password is None:
        # No password provided
        return 2
    
    conn = get_db() # Get connection
    try:
        # Try inserting a new record
        # The record is of the new user
        # If it fails, email-acc_type combination exists in database
        conn.execute("INSERT INTO volunteers (email, password, phone) VALUES (?, ?, ?)", (email, generate_password_hash(password), phone))
        conn.commit() # Save the change
    except conn.IntegrityError:
        # Violated uniqueness of email
        return 3
    # Close database
    close_db(conn)
    return 0 # Success


@app.route('/signup/donors', methods=["POST"])
def sign_up_donors():
    email = request.form['email'] # Get email from form action
    password = request.form['password'] # Get password from form action
    phone = request.form['phone'] # Get phone from form action
    ret_code = create_donor(email, password, phone) # Create user

    if ret_code == 0:
        # Success
        login_donor(email)
        return redirect(url_for('donor_index'))
    elif ret_code == 1:
        return "No username was provided", 403
    elif ret_code == 2:
        return "No password was provided", 403
    else:
        return "Email address exists in database", 403


@app.route('/signup/volunteers', methods=["POST"])
def sign_up_volunteers():
    email = request.form['email'] # Get email from form action
    password = request.form['password'] # Get password from form action
    phone = request.form['phone'] # Get phone from form action
    ret_code = create_volunteer(email, password, phone) # Create user

    if ret_code == 0:
        # Success
        login_volunteer(email)
        return redirect(url_for('volunteer_index'))
    elif ret_code == 1:
        return "No username was provided", 403
    elif ret_code == 2:
        return "No password was provided", 403
    else:
        return "Email address exists in database", 403


@app.route('/login/donor', methods=["POST"])
def login_call_donor():
    email = request.form['email'] # Get email from form action
    password = request.form['password'] # Get password from form action
    ret_code = is_valid_login_donor(email, password) # Validate

    if ret_code == 0:
        # Success
        login_donor(email)
        return redirect(url_for('donor_index'))
    elif ret_code == 1:
        return "No email provided", 403
    elif ret_code == 2:
        return "No password provided", 403
    elif ret_code == 3:
        return "No user with provided email found", 403
    else:
        return "Inorrect password", 403


@app.route('/login/volunteer', methods=["POST"])
def login_call_volunteer():
    email = request.form['email'] # Get email from form action
    password = request.form['password'] # Get password from form action
    ret_code = is_valid_login_volunteer(email, password) # Validate

    if ret_code == 0:
        # Success
        login_volunteer(email)
        return redirect(url_for('volunteer_index'))
    elif ret_code == 1:
        return "No email provided", 403
    elif ret_code == 2:
        return "No password provided", 403
    elif ret_code == 3:
        return "No user with provided email found", 403
    else:
        return "Inorrect password", 403
    

def login_volunteer(email):
    session.clear()
    session['user_id'] = email
    session['acc_type'] = 'volunteer'


def login_donor(email):
    session.clear()
    session['user_id'] = email
    session['acc_type'] = 'donor'


@app.route('/volunteer')
def volunteer_index():
    # Go to volunteer page
    return app.send_static_file('volunteer.html')


@app.route('/donor')
def donor_index():
    # Go to donor page
    return app.send_static_file('donor.html')


@app.route('/')
def index():
    return app.send_static_file('index.html')

# @app.route('/test/create')
# def tester():
#     create_volunteer('test@example.com', 'password')
#     return "Created login test@example.com with password password"

@app.route('/auth/signup/donor')
def donor_sign_up_ui():
    return app.send_static_file('signupd.html')


@app.route('/auth/signup/volunteer')
def volunteer_sign_up_ui():
    return app.send_static_file('signupv.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
