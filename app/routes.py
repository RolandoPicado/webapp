
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from .models import db, User, Sponsor
from .forms import LoginForm, CreateUserForm

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    print(current_app.jinja_loader.searchpath)
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        sponsors = Sponsor.query.all()
    else:
        sponsors = [current_user.sponsor]
    return render_template('dashboard.html', sponsors=sponsors)

@main.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    #Überprüfen ob User ein Admin ist
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.dashboard'))

    form = CreateUserForm()
    if form.validate_on_submit():
        #Erstelle neuer User verbinde mit Sponsor
        user = User(username=form.username.data, is_admin=False)
        user.set_password(form.password.data)
        Sponsor = Sponsor(company_name=form.company_name.data, sponsorship_level=form.sponsorship_level.data)
        user.sponsor = sponsor
        db.session.add(user)
        db.session.commit()
        flash('New sponsor created successfully')
        return redirect(url_for('main.dashboard'))
    return render_template('create_user.html', form=form)

@main.route('/admin_dashboard')
@login_required
def admin_dashboard():
        if not current_user.is_admin:
            flash('You do not have permission to access this page.')
            return redirect(url_for('main.dashboard'))
        sponsors = Sponsor.query.all()
        return render_template('admin_dashboard.html', sponsors=sponsors)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
