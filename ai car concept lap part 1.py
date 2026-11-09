from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'car_lab_part1_secret'

LAYOUT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Car Concept Lab - Part 1</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: #09090b; color: #f4f4f5; min-height: 100vh; }
        .navbar { display: flex; justify-content: space-between; align-items: center; padding: 1.2rem 2rem; background: #18181b; border-bottom: 1px solid #27272a; }
        .logo { font-weight: bold; font-size: 1.2rem; color: #38bdf8; }
        .navbar nav a { color: #a1a1aa; text-decoration: none; margin-left: 1.5rem; transition: color 0.2s; }
        .navbar nav a:hover { color: #38bdf8; }
        .container { max-width: 1000px; margin: 2rem auto; padding: 0 1rem; }
        .card { background: #121214; padding: 2rem; border-radius: 12px; border: 1px solid #27272a; margin-top: 1.5rem; }
        h1, h2 { color: #fff; margin-bottom: 1rem; }
        p { color: #a1a1aa; line-height: 1.6; margin-bottom: 1.5rem; }
        label { display: block; margin: 1rem 0 0.5rem; color: #d4d4d8; }
        input, select, textarea { width: 100%; padding: 0.8rem; background: #18181b; border: 1px solid #27272a; color: #fff; border-radius: 6px; margin-bottom: 1rem; }
        .btn-primary { background: #38bdf8; color: #09090b; padding: 0.8rem 1.5rem; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn-primary:hover { background: #0ea5e9; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
        .history-card { background: #18181b; padding: 1.2rem; border-radius: 8px; border: 1px solid #27272a; }
        .history-card h3 { color: #38bdf8; margin-bottom: 0.5rem; }
    </style>
</head>
<body>
    <header class="navbar">
        <div class="logo">⚡ AI Car Studio</div>
        <nav>
            <a href="/">Home</a>
            <a href="/studio">Studio</a>
            <a href="/history">History</a>
        </nav>
    </header>
    <main class="container">
        {% block content %}{% endblock %}
    </main>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(LAYOUT_TEMPLATE + """
        <div class="card" style="text-align: center; padding: 4rem 2rem;">
            <h1>AI Car Concept Lab - Part 1</h1>
            <p>Welcome to the futuristic AI Car Concept Lab. Structure your interface, submit design briefs, and track your vehicle generation history seamlessly[cite: 3].</p>
            <a href="/studio" class="btn-primary">Go to Studio Page</a>
        </div>
    """)

@app.route('/studio', methods=['GET', 'POST'])
def studio():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        car_model = request.form.get('car_model')
        style = request.form.get('style')
        features = request.form.get('features')
        
        concept = {
            "model": car_model,
            "style": style,
            "features": features,
            "image_url": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=600&q=80"
        }
        
        session['history'].insert(0, concept)
        session.modified = True
        return redirect(url_for('history'))

    return render_template_string(LAYOUT_TEMPLATE + """
        <div class="card">
            <h2>Design Studio Interface</h2>
            <p>Fill out the structured car-design brief below[cite: 3]. Flask will process the brief, generate a concept, and save it to your session history[cite: 3].</p>
            <form method="POST">
                <label>Car Model Name:</label>
                <input type="text" name="car_model" required placeholder="e.g. Apex Hyper-V">

                <label>Design Style:</label>
                <select name="style">
                    <option value="Futuristic Cyberpunk">Futuristic Cyberpunk</option>
                    <option value="Minimalist Electric">Minimalist Electric</option>
                    <option value="Aggressive Track Spec">Aggressive Track Spec</option>
                </select>

                <label>Advanced Features:</label>
                <input type="text" name="features" placeholder="e.g. Holographic HUD, Solid-state battery">

                <button type="submit" class="btn-primary">Generate Concept & Save</button>
            </form>
        </div>
    """)

@app.route('/history')
def history():
    user_history = session.get('history', [])
    return render_template_string(LAYOUT_TEMPLATE + """
        <h2>Concept History Page</h2>
        <p>Review all previously generated vehicle concepts stored in your session[cite: 3].</p>
        {% if history %}
            <div class="grid">
                {% for item in history %}
                <div class="history-card">
                    <h3>{{ item.model }}</h3>
                    <p><strong>Style:</strong> {{ item.style }}</p>
                    <p><strong>Features:</strong> {{ item.features }}</p>
                    <img src="{{ item.image_url }}" alt="Car Render" style="width:100%; border-radius: 4px; margin-top: 10px;">
                </div>
                {% endfor %}
            </div>
        {% else %}
            <p>No concepts saved yet. Head over to the <a href="/studio" style="color: #38bdf8;">Studio</a> to create one!</p>
        {% endif %}
    """, history=user_history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)