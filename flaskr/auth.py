import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# If not created, create file "sign_up_code" with signup code 
# as only text
try:
    with open("flaskr/static/sign_up_code") as f:
        code = f.readline()
        print(code)
except IOError:
    print("No signup code set: Please create a file called 'sign_up_code' in static/")
    code = "passcode"


@bp.route('/register', methods=('GET', 'POST'))
def register()->render_template:
    """Register user
    
    Form request arguments:
    username -- User's name. Must be unique
    password -- User's password
    reg_code -- Hidden code to limit registering users
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        reg_code = request.form['regcode']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not reg_code:
            error = 'Registration code is required.'
        elif not(reg_code == code):
            error = 'Registration code is incorrect.'
        elif check_user(username):
            error = 'Username is already taken.'


        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login()->render_template:
    """Login user
    
    Form request arguments:
    username -- User's name
    password -- User's password
    """
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user()->None:
    """Load user

    Return: None
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_user(user_id)
        

def get_user(user_id:int)->str:
    """Return user given user ID
    
    Keyword arguments:
    user_id -- integer number representing user in DB
    Return: str username for corresponding user_id. 
    None if no matches
    """
    return get_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()


def check_user(username:str)->bool:
    """Check if username exists. Returns false if not found
    
    Keyword arguments:
    username -- username to search database with
    Return: False is query is empty, True if found
    """
    if (get_db().execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone() is None):
        return False
    return True


@bp.route('/logout')
def logout():
    """Log user out
    """
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """Wrapper decorator to require login for pages
    
    Keyword arguments:
    view -- Flask View
    Return: Wrapped flask view
    """
    
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view