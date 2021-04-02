"""Routes for user authentication."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash

from . import login_manager
from .forms import FormLogin, FormSignup
from .models import User
from Predilectura import mongo

# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.
    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = FormSignup()
    if form.validate_on_submit():
        existing_user = mongo.db.users.find_one({"email": form.email.data})
        if existing_user is None:
            user = User(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data,
                is_admin=form.is_admin.data
            )

            user_id = mongo.db.users.insert(user.get_json())
            user.set_id(user_id)
            login_user(user)  # Log in as newly created user
            return redirect(url_for('/dashapp/'))
        flash('A user already exists with that email address.')
    return render_template(
        'signup.jinja2',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('/dashapp/'))

    form = FormLogin()
    # Validate login attempt
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"email": form.email.data})

        if user and check_password_hash(user["password"], form.password.data):
            loginuser = User(user["name"], user["email"], form.password.data, user["is_admin"])
            login_user(loginuser)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('/dashapp/'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login'))
    return render_template(
        'login.jinja2',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with your User account."
    )


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return mongo.db.users.find_one({"_id": user_id})

    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))
