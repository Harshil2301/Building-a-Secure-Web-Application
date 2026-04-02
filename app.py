import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth

from models import db, User

load_dotenv()

app = Flask(__name__)
# Security configuration
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-fallback-secret-key')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-fallback-jwt-key')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False # For simplicity; use True in strict production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize security plugins
db.init_app(app)
jwt = JWTManager(app)
csrf = CSRFProtect(app)
# Talisman secures HTTP headers (force_https=False for local dev otherwise it loops)
Talisman(app, content_security_policy=None, force_https=False) 

# OAuth Setup
oauth = OAuth(app)
github_client_id = os.environ.get('GITHUB_CLIENT_ID')
github_client_secret = os.environ.get('GITHUB_CLIENT_SECRET')

# Only register GitHub OAuth if valid credentials are provided
if github_client_id and github_client_id != 'your_github_client_id_here':
    github = oauth.register(
        name='github',
        client_id=github_client_id,
        client_secret=github_client_secret,
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )
else:
    github = None

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check against database securely
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            resp = redirect(url_for('dashboard'))
            set_access_cookies(resp, access_token) # Secure HttpOnly cookie
            return resp
        else:
            flash("Invalid credentials", "error")
            
    return render_template("login.html", github_enabled=github is not None)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "error")
        else:
            new_user = User(username=username)
            new_user.set_password(password) # Secure hash
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully. Please login.", "success")
            return redirect(url_for('login'))
            
    return render_template("signup.html")

@app.route('/login/github')
def login_github():
    if not github:
        flash("GitHub OAuth is not configured in .env", "error")
        return redirect(url_for('login'))
    redirect_uri = url_for('auth_github', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/auth/github')
def auth_github():
    if not github:
        return redirect(url_for('login'))
        
    token = github.authorize_access_token()
    resp = github.get('user')
    profile = resp.json()
    
    github_id = str(profile['id'])
    username = profile.get('login', f"github_user_{github_id}")
    
    user = User.query.filter_by(github_id=github_id).first()
    if not user:
        if User.query.filter_by(username=username).first():
            username = f"{username}_{github_id}"
        
        user = User(username=username, github_id=github_id)
        db.session.add(user)
        db.session.commit()
        
    access_token = create_access_token(identity=str(user.id))
    resp_redir = redirect(url_for('dashboard'))
    set_access_cookies(resp_redir, access_token)
    return resp_redir

@app.route("/dashboard")
@jwt_required()
def dashboard():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    return render_template("dashboard.html", user=user)

@app.route("/logout")
def logout():
    resp = redirect(url_for('login'))
    unset_jwt_cookies(resp)
    return resp

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)