from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///cmu_student_hub.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Handle PostgreSQL URL format for newer SQLAlchemy versions
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    andrew_id = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text)
    research_interests = db.Column(db.Text)
    contact_info = db.Column(db.Text)
    profile_image = db.Column(db.String(200))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    demo_url = db.Column(db.String(200))
    technologies = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_featured = db.Column(db.Boolean, default=False)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_featured = db.Column(db.Boolean, default=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'CMU Africa Hub is running'}, 200

@app.route('/')
def home():
    try:
        featured_projects = Project.query.filter_by(is_featured=True).order_by(Project.date_created.desc()).limit(6).all()
        featured_blogs = BlogPost.query.filter_by(is_featured=True).order_by(BlogPost.date_created.desc()).limit(3).all()
        return render_template('home.html', projects=featured_projects, blogs=featured_blogs)
    except Exception as e:
        # Fallback if database isn't ready
        return render_template('home.html', projects=[], blogs=[])

@app.route('/projects')
def projects():
    page = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.date_created.desc()).paginate(
        page=page, per_page=9, error_out=False)
    return render_template('projects.html', projects=projects)

@app.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.date_created.desc()).paginate(
        page=page, per_page=6, error_out=False)
    return render_template('blog.html', posts=posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    comments = Comment.query.filter_by(blog_post_id=post_id).order_by(Comment.date_created.desc()).all()
    return render_template('blog_post.html', post=post, comments=comments)

@app.route('/student/<int:user_id>')
def student_profile(user_id):
    user = User.query.get_or_404(user_id)
    projects = Project.query.filter_by(user_id=user_id).order_by(Project.date_created.desc()).all()
    return render_template('student_profile.html', student=user, projects=projects)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        andrew_id = request.form['andrew_id']
        password = request.form['password']
        user = User.query.filter_by(andrew_id=andrew_id).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Andrew ID or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        andrew_id = request.form['andrew_id']
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(andrew_id=andrew_id).first():
            flash('Andrew ID already exists', 'error')
            return render_template('register.html')
        
        user = User(andrew_id=andrew_id, full_name=full_name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.date_created.desc()).all()
    user_posts = BlogPost.query.filter_by(user_id=current_user.id).order_by(BlogPost.date_created.desc()).all()
    return render_template('dashboard.html', projects=user_projects, posts=user_posts)

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        project = Project(
            title=request.form['title'],
            description=request.form['description'],
            image_url=request.form['image_url'],
            github_url=request.form['github_url'],
            demo_url=request.form['demo_url'],
            technologies=request.form['technologies'],
            user_id=current_user.id
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_project.html')

@app.route('/add_blog', methods=['GET', 'POST'])
@login_required
def add_blog():
    if request.method == 'POST':
        post = BlogPost(
            title=request.form['title'],
            content=request.form['content'],
            excerpt=request.form['excerpt'],
            image_url=request.form['image_url'],
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Blog post added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_blog.html')

@app.route('/add_comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    comment = Comment(
        content=request.form['content'],
        user_id=current_user.id,
        blog_post_id=post_id
    )
    db.session.add(comment)
    db.session.commit()
    flash('Comment added successfully!', 'success')
    return redirect(url_for('blog_post', post_id=post_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    """Proxy endpoint to handle chat requests and avoid CORS issues"""
    try:
        # Get the question from the request
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'Question is required'}), 400
        
        # Make request to the external API
        external_api_url = 'https://tartan-qa-system.onrender.com/chat'
        response = requests.post(
            external_api_url,
            json={'question': data['question']},
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        # Return the response from the external API
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'External API error'}), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout. Please try again.'}), 408
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to connect to chat service'}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

# Initialize database
def init_db():
    try:
        with app.app_context():
            db.create_all()
            print("Database tables created successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')
else:
    # For production deployment
    init_db()
