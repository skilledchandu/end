from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'resume_login_secret_key'

# In-memory user database simulation
USERS = {}

BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Create Resume & User Login App</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 40px; }
        .container { max-width: 500px; margin: auto; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        h2 { color: #38bdf8; margin-top: 0; text-align: center; }
        input, textarea, button { width: 100%; padding: 12px; margin: 10px 0; box-sizing: border-box; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 6px; }
        button { background: #38bdf8; color: #0f172a; font-weight: bold; cursor: pointer; border: none; transition: background 0.2s; }
        button:hover { background: #0ea5e9; }
        .btn-alt { background: #475569; color: white; }
        .btn-alt:hover { background: #334155; }
        .msg { color: #f43f5e; text-align: center; font-size: 0.9rem; }
        .nav { text-align: center; margin-bottom: 20px; }
        .nav a { color: #38bdf8; text-decoration: none; margin: 0 10px; font-weight: 500; }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/login">Login / Register</a> | 
            <a href="/resume">Resume Backend</a>
        </div>
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return redirect(url_for('login_route'))

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    msg = ""
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if action == 'register':
            if username in USERS:
                msg = "Username already exists!"
            else:
                USERS[username] = password
                msg = "Registration successful! You can now log in."
        elif action == 'login':
            if USERS.get(username) == password:
                session['user'] = username
                return redirect(url_for('resume_route'))
            else:
                msg = "Invalid username or password!"
                
    return render_template_string(BASE_TEMPLATE + """
        <h2>User Authentication</h2>
        {% if msg %}<p class="msg">{{ msg }}</p>{% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit" name="action" value="login">Login</button>
            <button type="submit" name="action" value="register" class="btn-alt">Register</button>
        </form>
    """, msg=msg)

@app.route('/resume', methods=['GET', 'POST'])
def resume_route():
    if 'user' not in session:
        return redirect(url_for('login_route'))
    
    user = session['user']
    resume_data = session.get('resume_data', {})
    
    if request.method == 'POST':
        resume_data = {
            'fullname': request.form.get('fullname'),
            'job_title': request.form.get('job_title'),
            'email': request.form.get('email'),
            'skills': request.form.get('skills'),
            'experience': request.form.get('experience')
        }
        session['resume_data'] = resume_data
        
    return render_template_string(BASE_TEMPLATE + """
        <h2>Resume Backend Studio</h2>
        <p style="text-align: center; color: #94a3b8;">Logged in as: <strong>{{ user }}</strong></p>
        <form method="POST">
            <input type="text" name="fullname" placeholder="Full Name" value="{{ resume_data.get('fullname', '') }}" required>
            <input type="text" name="job_title" placeholder="Professional Title (e.g. Python Developer)" value="{{ resume_data.get('job_title', '') }}" required>
            <input type="email" name="email" placeholder="Email Address" value="{{ resume_data.get('email', '') }}" required>
            <input type="text" name="skills" placeholder="Skills (comma separated)" value="{{ resume_data.get('skills', '') }}">
            <textarea name="experience" placeholder="Work Experience Summary" rows="3">{{ resume_data.get('experience', '') }}</textarea>
            <button type="submit">Save Resume Data</button>
        </form>
        
        {% if resume_data %}
            <hr style="border-color: #334155; margin: 20px 0;">
            <h3 style="color: #38bdf8; font-size: 1.1rem;">Saved Backend Data:</h3>
            <p><strong>Name:</strong> {{ resume_data.fullname }}</p>
            <p><strong>Title:</strong> {{ resume_data.job_title }}</p>
            <p><strong>Email:</strong> {{ resume_data.email }}</p>
            <p><strong>Skills:</strong> {{ resume_data.skills }}</p>
            <p><strong>Experience:</strong> {{ resume_data.experience }}</p>
        {% endif %}
    """, user=user, resume_data=resume_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)