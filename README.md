# CMU African Student Project Hub

A modern, responsive web application built with Flask that connects African students at Carnegie Mellon University through innovative projects and collaborative learning.

## Features

### 🏠 Home Page
- Hero section with CMU Africa branding
- Latest 6 featured projects in a responsive grid
- Latest 3 blog posts preview
- Statistics section
- Floating chat icon

### 📁 Projects Section
- Paginated project listings
- Technology filtering
- Student profile integration
- GitHub and demo links

### 📝 Blog Section
- Blog post listings with pagination
- Detailed blog post view with commenting system
- Author profiles and contact information

### 👤 User Authentication
- Andrew ID and password login
- User registration
- Secure password hashing

### 🎛️ Dashboard
- User dashboard for managing projects and blog posts
- Add new projects with technology tags
- Write and publish blog posts
- View personal statistics

### 💬 Interactive Chat
- Floating chat button
- Real-time chat simulation
- Community engagement features

## Technology Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-Bcrypt
- **Frontend**: Bootstrap 5, Font Awesome, Custom CSS/JS
- **Database**: SQLite (development)
- **Styling**: CMU Africa color scheme with modern responsive design

## Installation & Setup

1. **Activate your virtual environment** (already created as mentioned)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:5000`

## Project Structure

```
cmu_student_project/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── home.html         # Homepage
│   ├── projects.html     # Projects listing
│   ├── blog.html         # Blog listing
│   ├── blog_post.html    # Individual blog post
│   ├── student_profile.html # Student profile page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── add_project.html  # Add project form
│   └── add_blog.html     # Add blog post form
└── static/              # Static assets
    ├── css/
    │   └── style.css     # Custom styles with CMU colors
    └── js/
        └── main.js       # Interactive JavaScript
```

## Key Features Implemented

### ✅ Responsive Design
- Mobile-first approach with Bootstrap 5
- CMU Africa color scheme (red, gold, blue)
- Modern, slick UI with smooth animations

### ✅ Navigation
- Home, Projects, Blog, Login/Register
- User authentication with Andrew ID
- Dashboard for authenticated users

### ✅ Project Management
- Add projects with descriptions, images, GitHub links
- Technology tagging system
- Student profile integration
- Pagination for large project lists

### ✅ Blog System
- Write and publish blog posts
- Commenting system
- Author profiles and contact information
- Featured posts on homepage

### ✅ User Profiles
- Student profiles with bio and research interests
- Project portfolios
- Contact information
- Professional presentation

### ✅ Interactive Features
- Floating chat with simulated responses
- Technology filtering
- Smooth scrolling and animations
- Form validation and loading states

## Database Models

- **User**: Student information with Andrew ID authentication
- **Project**: Student projects with metadata
- **BlogPost**: Blog posts with content and metadata
- **Comment**: Blog post comments

## Color Scheme

The application uses CMU Africa's official colors:
- **Primary Red**: #C41E3A
- **Dark Red**: #8B0000
- **Gold**: #FFD700
- **Blue**: #1E3A8A
- **Light Blue**: #3B82F6

## Getting Started

1. Register a new account with your Andrew ID
2. Add your first project to showcase your work
3. Write a blog post about your experiences
4. Explore other students' projects and connect with the community

## Future Enhancements

- Real-time chat integration
- File upload for project images
- Advanced search functionality
- Email notifications
- Social media integration
- Mobile app development

---

**Built with ❤️ for the CMU African Student Community**
