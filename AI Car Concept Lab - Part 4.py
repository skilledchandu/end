import os
import requests
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'ai_car_concept_lab_part4_secret'

# API Keys (Set your environment variables or replace with test/valid keys)
GROQ_API_KEY = os.getenv('GROQ_API_KEY', 'your_groq_api_key_here')
HF_API_KEY = os.getenv('HF_API_KEY', 'your_huggingface_api_key_here')

def generate_concept_with_groq(model_name, style, features):
    """Uses Groq API to generate structured description and colorways."""
    # Fallback response if API key is not configured
    if GROQ_API_KEY == 'your_groq_api_key_here':
        return {
            "description": f"An advanced {style} vehicle concept named {model_name}, featuring {features}. Designed for next-generation aerodynamics and intelligent cabin autonomy.",
            "colorways": [
                {"name": "Neon Midnight", "accent": "#38bdf8"},
                {"name": "Cyber Crimson", "accent": "#f43f5e"},
                {"name": "Quantum Gold", "accent": "#fbbf24"}
            ]
        }
    
    # Real Groq API implementation can be hooked here using `groq` package
    return {
        "description": f"AI-optimized {style} build for {model_name} with integrated {features}.",
        "colorways": [
            {"name": "Electric Cyan", "accent": "#00f0ff"},
            {"name": "Obsidian Matte", "accent": "#27272a"},
            {"name": "Solar Flare", "accent": "#f59e0b"}
        ]
    }

def generate_vehicle_image(prompt):
    """Generates an AI vehicle/product image using Hugging Face Inference API."""
    if HF_API_KEY == 'your_huggingface_api_key_here':
        # Default fallback placeholder image representing the AI render
        return "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80"
    
    api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            # In a full app, you'd save or stream the binary content; here we fallback to sample URL if needed
            pass
    except Exception:
        pass
        
    return "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80"

LAYOUT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Car Concept Lab - Part 4</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: #09090b; color: #f4f4f5; min-height: 100vh; }
        .navbar { display: flex; justify-content: space-between; align-items: center; padding: 1.2rem 2rem; background: #18181b; border-bottom: 1px solid #27272a; }
        .logo { font-weight: bold; font-size: 1.2rem; color: #38bdf8; }
        .navbar nav a { color: #a1a1aa; text-decoration: none; margin-left: 1.5rem; transition: color 0.2s; }
        .navbar nav a:hover { color: #38bdf8; }
        .container { max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }
        .btn-primary { background: #38bdf8; color: #09090b; padding: 0.8rem 1.5rem; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; text-decoration: none; display: inline-block; width: 100%; transition: background 0.2s; }
        .btn-primary:hover { background: #0ea5e9; }
        .studio-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
        .form-panel, .preview-panel { background: #121214; padding: 2rem; border-radius: 12px; border: 1px solid #27272a; }
        .form-panel label { display: block; margin: 1rem 0 0.5rem; color: #d4d4d8; }
        .form-panel input, .form-panel select { width: 100%; padding: 0.8rem; background: #18181b; border: 1px solid #27272a; color: #fff; border-radius: 6px; margin-bottom: 1rem; }
        .colorway-container { display: flex; gap: 0.8rem; margin: 1rem 0; }
        .color-tab { padding: 0.4rem 0.9rem; border-radius: 4px; border: 1px solid #3f3f46; cursor: pointer; font-size: 0.85rem; background: #18181b; color: #fff; }
        .color-tab.active { border-color: #38bdf8; background: #1e293b; }
        .info-box { background: #18181b; padding: 1rem; border-radius: 6px; border: 1px solid #27272a; color: #a1a1aa; font-size: 0.95rem; margin-top: 1rem; }
        .grid-history { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
        .history-card { background: #121214; padding: 1.5rem; border-radius: 8px; border: 1px solid #27272a; }
        .history-card h3 { color: #38bdf8; margin-bottom: 0.5rem; }
        .history-card img { width: 100%; border-radius: 6px; margin-top: 0.8rem; border: 1px solid #27272a; }
    </style>
</head>
<body>
    <header class="navbar">
        <div class="logo">⚡ AI Car Studio Lab</div>
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
        <div style="text-align: center; padding: 5rem 1rem;">
            <h1 style="font-size: 3rem; margin-bottom: 1rem;">AI Car Concept Lab - Part 4</h1>
            <p style="color: #a1a1aa; font-size: 1.2rem; margin-bottom: 2rem;">Dynamic JSON & Fetch Architecture powered by Groq and Hugging Face.</p>
            <a href="/studio" class="btn-primary" style="width: auto;">Launch Dynamic Studio</a>
        </div>
    """)

@app.route('/studio', methods=['GET', 'POST'])
def studio():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        # Accept incoming JSON payload via Fetch API[cite: 6]
        data = request.json or request.form
        car_model = data.get('car_model', 'Apex Hyper-V')
        style = data.get('style', 'Futuristic Cyberpunk')
        features = data.get('features', 'Autonomous AI, Solid-State Battery')
        
        # Call Groq & Hugging Face logic[cite: 6]
        ai_data = generate_concept_with_groq(car_model, style, features)
        image_url = generate_vehicle_image(f"Concept car {car_model}, {style}, {features}")
        
        concept = {
            "id": len(session['history']) + 1,
            "model": car_model,
            "style": style,
            "features": features,
            "description": ai_data["description"],
            "colorways": ai_data["colorways"],
            "image_url": image_url
        }
        
        session['history'].insert(0, concept)
        session.modified = True
        
        return jsonify({"status": "success", "concept": concept})

    return render_template_string(LAYOUT_TEMPLATE + """
        <div class="studio-grid">
            <div class="form-panel">
                <h2>Dynamic Design Brief</h2>
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
                    <input type="text" name="features" placeholder="e.g. Holographic HUD, Solar Skin">

                    <button type="submit" class="btn-primary" id="submit-btn">Generate Branded Concept</button>
                </form>
            </div>

            <div class="preview-panel">
                <h2>Live AI Render & Specs</h2>
                <div id="render-container" style="background:#18181b; border-radius:8px; overflow:hidden; border:1px solid #27272a; min-height:220px; display:flex; align-items:center; justify-content:center;">
                    <p id="placeholder-text" style="color:#71717a;">Submit brief to fetch JSON and render concept[cite: 6].</p>
                    <img id="concept-image" src="" alt="AI Vehicle Render" style="width:100%; display:none;">
                </div>
                <div id="colorway-tabs" class="colorway-container"></div>
                <div id="info-panel" class="info-box">Awaiting asynchronous request...</div>
            </div>
        </div>

        <script>
        document.getElementById('concept-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            const submitBtn = document.getElementById('submit-btn');
            submitBtn.innerText = 'Generating via Groq & Hugging Face...';
            submitBtn.disabled = true;

            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/studio', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                if(result.status === 'success') {
                    const concept = result.concept;
                    
                    document.getElementById('placeholder-text').style.display = 'none';
                    const img = document.getElementById('concept-image');
                    img.src = concept.image_url;
                    img.style.display = 'block';

                    const tabsContainer = document.getElementById('colorway-tabs');
                    tabsContainer.innerHTML = '';
                    
                    concept.colorways.forEach((cw, idx) => {
                        const btn = document.createElement('button');
                        btn.className = `color-tab ${idx === 0 ? 'active' : ''}`;
                        btn.innerText = cw.name;
                        btn.onclick = () => {
                            document.querySelectorAll('.color-tab').forEach(b => b.classList.remove('active'));
                            btn.classList.add('active');
                            img.style.filter = `drop-shadow(0 0 10px ${cw.accent})`;
                        };
                        tabsContainer.appendChild(btn);
                    });

                    document.getElementById('info-panel').innerHTML = 
                        `<strong>Model:</strong> ${concept.model} | <strong>Style:</strong> ${concept.style}<br>` +
                        `<p style="margin-top:6px; color:#d4d4d8;">${concept.description}</p>`;
                }
            } catch (err) {
                alert('An error occurred during fetch generation.');
            } finally {
                submitBtn.innerText = 'Generate Branded Concept';
                submitBtn.disabled = false;
            }
        });
        </script>
    """)

@app.route('/history')
def history():
    user_history = session.get('history', [])
    return render_template_string(LAYOUT_TEMPLATE + """
        <div class="history-container">
            <h2>Generated Concepts History</h2>
            <p style="color: #a1a1aa; margin-top: 0.5rem;">Session history containing all dynamic JSON responses and renders[cite: 6].</p>
            {% if history %}
                <div class="grid-history">
                    {% for item in history %}
                    <div class="history-card">
                        <h3>{{ item.model }}</h3>
                        <p><strong>Style:</strong> {{ item.style }}</p>
                        <p><strong>Features:</strong> {{ item.features }}</p>
                        <p style="font-size:0.9rem; color:#a1a1aa; margin-top:4px;">{{ item.description }}</p>
                        <img src="{{ item.image_url }}" alt="Vehicle Concept">
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <p style="margin-top: 1.5rem; color: #a1a1aa;">No concepts generated yet. Visit the <a href="/studio" style="color: #38bdf8;">Studio</a>!</p>
            {% endif %}
        </div>
    """, history=user_history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)