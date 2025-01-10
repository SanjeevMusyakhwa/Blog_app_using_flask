from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Flask app and extensions setup
app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SECRET_KEY'] = 'mysecretkey'  # To secure sessions

db = SQLAlchemy(app)  # link flask app to database
bcrypt = Bcrypt(app)  # For hashing passwords
login_manager = LoginManager(app)  # For user session management
login_manager.login_view = 'login'  # Redirect to login if not authenticated


# Database Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('BlogPost', backref='author', lazy=True)
    
    def __repr__(self):
        return f"Author: {self.username}"

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return 'Blog Post' + str(self.title)


# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Url and Views

@app.route('/', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']  # This should be the username of the user

        # Fetch the User by username
        user = User.query.filter_by(username=post_author).first()
        if not user:
            return "User not found", 404  # Handle case when user is not found

        # Create the post, assign the user_id
        create_post = BlogPost(title=post_title, content=post_content, user_id=user.id)
        db.session.add(create_post)
        db.session.commit()

        return redirect('/')
    else:
        page = request.args.get('page', 1, type=int)
        posts_per_page = 4
        all_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).paginate(page=page, per_page=posts_per_page)
        return render_template('posts.html', posts=all_posts)


@app.route('/posts/new', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']  # Username of the user

        # Fetch the User by username
        user = User.query.filter_by(username=post_author).first()
        if not user:
            return "User not found", 404  # Handle case when user doesn't exist

        # Create the post, assign the user_id
        create_post = BlogPost(title=post_title, content=post_content, user_id=user.id)
        db.session.add(create_post)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('create_post.html')

@app.route('/posts/delete/<int:post_id>', methods=['POST'])
@login_required
def delete(post_id):
    try:
        # Fetch the post by ID or return a 404 if not found
        post = BlogPost.query.get_or_404(post_id)

        # Check if the current user is the owner of the post
        if post.user_id != current_user.id:
            return jsonify({"error": "You do not have permission to delete this post"}), 403

        # Delete the post
        db.session.delete(post)
        db.session.commit()

        return redirect('/')

    except Exception as e:
        # Log the exception for debugging
        app.logger.error(f"Error deleting post: {e}")
        return jsonify({"error": "An error occurred while trying to delete the post"}), 500



@app.route('/posts/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit.html', post=post)


@app.route('/posts/detail/<int:id>', methods=['GET'])
def post_detail(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('post_detail.html', post=post)


# User Registration Route
@app.route('/accounts/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # Hash password

        # Check if the user already exists
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username already exists', 'danger')
            return redirect('/accounts/register')

        # Create a new user
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful, you can now log in!', 'success')
        return redirect('/accounts/login')

    return render_template('accounts/register.html')


# User Login Route
@app.route('/accounts/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Find the user by username
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect('/')
        else:
            flash('Login failed. Check your username and/or password', 'danger')

    return render_template('accounts/login.html')


# User Logout Route
@app.route('/accounts/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect('/')


# End of Url and Views

if __name__ == "__main__":
    app.run(debug=True)
