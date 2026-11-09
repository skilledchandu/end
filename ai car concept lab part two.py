from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'ai_car_concept_lab_secret'

LAB_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Car Concept Lab - Part 2</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: #09090b; color: #f4f4f5; min-height: 100vh; }
        .navbar { display: flex; justify-content: space-between; align-items: center; padding: 1.2rem 2rem; background: #18181b; border-bottom: 1px solid #27272a; }
        .logo { font-weight: bold; font-size: 1.2rem; color: #38bdf8; }
        .navbar nav a { color: #a1a1aa; text-decoration: none; margin-left: 1.5rem; transition: color 0.2s; }
        .navbar nav a:hover { color: #38bdf8; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
        .btn-primary { background: #38bdf8; color: #09090b; padding: 0.8rem 1.5rem; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; text-decoration: none; display: inline-block; transition: background 0.2s; }
        .btn-primary:hover { background: #0ea5e9; }
        .studio-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
        .form-panel, .preview-panel { background: #121214; padding: 2rem; border-radius: 12px; border: 1px solid #27272a; }
        .form-panel label { display: block; margin: 1rem 0 0.5rem; color: #d4d4d8; }
        .form-panel input, .form-panel select { width: 100%; padding: 0.8rem; background: #18181b; border: 1px solid #27272a; color: #fff; border-radius: 6px; margin-bottom: 1rem; }
        .placeholder-render { background: #18181b; border-radius: 8px; overflow: hidden; margin-bottom: 1rem; border: 1px solid #27272a; }
        .colorway-container { display: flex; gap: 0.8rem; margin-bottom: 1rem; }
        .color-tab { padding: 0.5rem 1rem; border-radius: 4px; border: 1px solid #3f3f46; cursor: pointer; font-size: 0.9rem; background: #18181b; color: #fff; transition: all 0.2s; }
        .color-tab.active { border-color: #38bdf8; background: #1e293b; }
        .info-box { background: #18181b; padding: 1rem; border-radius: 6px; border: 1px solid #27272a; color: #a1a1aa; font-size: 0.95rem; }
        .grid-history { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
        .history-card { background: #121214; padding: 1.5rem; border-radius: 8px; border: 1px solid #27272a; }
        .history-card h3 { color: #38bdf8; margin-bottom: 0.5rem; }
        .history-card p { margin-bottom: 0.5rem; font-size: 0.95rem; color: #d4d4d8; }
    </style>
</head>
<body>
    <header class="navbar">
        <div class="logo">⚡ AI Car Concept Lab</div>
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
    return render_template_string(LAB_TEMPLATE + """
        {% extends "base" %}
        <div style="text-align: center; padding: 5rem 1rem;">
            <h1 style="font-size: 3rem; margin-bottom: 1rem; color: #fff;">AI Car Concept Lab - Part 2</h1>
            <p style="color: #a1a1aa; font-size: 1.2rem; margin-bottom: 2rem;">Generate AI concept models from user briefs, preview interactive colorways, and track history in session[cite: 2].</p>
            <a href="/studio" class="btn-primary">Launch Studio</a>
        </div>
    """)

@app.route('/studio', methods=['GET', 'POST'])
def studio():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        data = request.json or request.form
        car_model = data.get('car_model', 'Cyber-GT Concept')
        style = data.get('style', 'Futuristic Cyberpunk')
        features = data.get('features', 'Autonomous AI, Solar Skin')
        
        # Colorway variations
        colorways = [
            {"name": "Neon Midnight", "accent": "#38bdf8"},
            {"name": "Cyber Crimson", "accent": "#f43f5e"},
            {"name": "Quantum Gold", "accent": "#fbbf24"}
        ]
        
        concept = {
            "id": len(session['history']) + 1,
            "model": car_model,
            "style": style,
            "features": features,
            "colorways": colorways,
            "description": f"An advanced {style} vehicle concept featuring {features}. Engineered for aerodynamic precision."
        }
        
        session['history'].insert(0, concept)
        session.modified = True
        
        if request.is_json:
            return jsonify({"status": "success", "concept": concept})
        return redirect(url_for('history'))

    return render_template_string(LAB_TEMPLATE + """
        <div class="studio-grid">
            <div class="form-panel">
                <h2>Design Brief</h2>
                <form id="concept-form">
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

                    <button type="submit" class="btn-primary">Generate Concept</button>
                </form>
            </div>

            <div class="preview-panel">
                <h2>Live Render Preview</h2>
                <div class="placeholder-render">
                    <svg viewBox="0 0 600 300" width="100%" height="100%">
                        <rect width="600" height="300" fill="#111" rx="12"/>
                        <path id="car-body" d="M100,200 L180,140 L380,140 L480,200 Z" fill="#38bdf8" style="transition: fill 0.3s;"/>
                        <circle cx="180" cy="210" r="30" fill="#222" stroke="#fff" stroke-width="4"/>
                        <circle cx="420" cy="210" r="30" fill="#222" stroke="#fff" stroke-width="4"/>
                        <text x="300" y="80" fill="#888" font-size="16" text-anchor="middle">Configure brief to render concept</text>
                    </svg>
                </div>
                <div id="colorway-tabs" class="colorway-container"></div>
                <div id="info-panel" class="info-box">Submit design brief to generate concept specs.</div>
            </div>
        </div>

        <script>
        document.getElementById('concept-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());

            const response = await fetch('/studio', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            if(result.status === 'success') {
                const concept = result.concept;
                const carBody = document.getElementById('car-body');
                const tabsContainer = document.getElementById('colorway-tabs');
                const infoPanel = document.getElementById('info-panel');

                tabsContainer.innerHTML = '';
                infoPanel.innerHTML = `<strong>Model:</strong> ${concept.model} | <strong>Style:</strong> ${concept.style}<br>${concept.description}`;

                concept.colorways.forEach((cw, index) => {
                    const btn = document.createElement('button');
                    btn.className = `color-tab ${index === 0 ? 'active' : ''}`;
                    btn.innerText = cw.name;
                    btn.onclick = () => {
                        document.querySelectorAll('.color-tab').forEach(b => b.classList.remove('active'));
                        btn.classList.add('active');
                        carBody.setAttribute('fill', cw.accent);
                    };
                    tabsContainer.appendChild(btn);
                });

                if(concept.colorways.length > 0) {
                    carBody.setAttribute('fill', concept.colorways[0].accent);
                }
            }
        });
        </script>
    """)

@app.route('/history')
def history():
    user_history = session.get('history', [])
    return render_template_string(LAB_TEMPLATE + """
        <div class="history-container">
            <h2>Generated Concepts History</h2>
            {% if history %}
                <div class="grid-history">
                    {% for item in history %}
                    <div class="history-card">
                        <h3>{{ item.model }}</h3>
                        <p><strong>Style:</strong> {{ item.style }}</p>
                        <p><strong>Features:</strong> {{ item.features }}</p>
                        <p>{{ item.description }}</p>
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <p style="margin-top: 1rem; color: #a1a1aa;">No concepts generated in this session yet. Head over to the <a href="/studio" style="color: #38bdf8;">Studio</a>!</p>
            {% endif %}
        </div>
    """, history=user_history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)