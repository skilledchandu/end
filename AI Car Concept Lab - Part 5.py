from flask import Flask, render_template_string, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'ai_car_concept_lab_part5_secret'

LAYOUT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Car Concept Lab - Part 5</title>
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
        .placeholder-render { background: #18181b; border-radius: 8px; overflow: hidden; margin-bottom: 1rem; border: 1px solid #27272a; }
        .colorway-container { display: flex; gap: 0.8rem; margin-bottom: 1rem; }
        .color-tab { padding: 0.5rem 1rem; border-radius: 4px; border: 1px solid #3f3f46; cursor: pointer; font-size: 0.9rem; background: #18181b; color: #fff; transition: all 0.2s; }
        .color-tab.active { border-color: #38bdf8; background: #1e293b; color: #38bdf8; font-weight: bold; }
        .info-box { background: #18181b; padding: 1rem; border-radius: 6px; border: 1px solid #27272a; color: #a1a1aa; font-size: 0.95rem; }
        .grid-history { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
        .history-card { background: #121214; padding: 1.5rem; border-radius: 8px; border: 1px solid #27272a; }
        .history-card h3 { color: #38bdf8; margin-bottom: 0.5rem; }
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
            <h1 style="font-size: 3rem; margin-bottom: 1rem;">AI Car Concept Lab - Part 5</h1>
            <p style="color: #a1a1aa; font-size: 1.2rem; margin-bottom: 2rem;">Interactive SVG Car Preview & Instant Colorway Switching[cite: 23].</p>
            <a href="/studio" class="btn-primary" style="width: auto;">Launch Design Studio</a>
        </div>
    """)

@app.route('/studio', methods=['GET', 'POST'])
def studio():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        data = request.json or request.form
        car_model = data.get('car_model', 'Apex Hyper-V')
        style = data.get('style', 'Futuristic Cyberpunk')
        features = data.get('features', 'Autonomous AI, Solar Skin')
        
        # Returns three unique colorways with specific color codes for the SVG and info panel
        colorways = [
            {
                "name": "Neon Midnight", 
                "primary": "#0f172a", 
                "accent": "#38bdf8", 
                "description": "Deep obsidian finish with vibrant cyan lighting accents for nighttime aerodynamic efficiency."
            },
            {
                "name": "Cyber Crimson", 
                "primary": "#18181b", 
                "accent": "#f43f5e", 
                "description": "Aggressive track-spec styling featuring high-contrast crimson lines and carbon-fiber trimming."
            },
            {
                "name": "Quantum Gold", 
                "primary": "#09090b", 
                "accent": "#fbbf24", 
                "description": "Exclusive luxury edition utilizing gold-infused quantum paneling and solar-reactive skin."
            }
        ]
        
        concept = {
            "id": len(session['history']) + 1,
            "model": car_model,
            "style": style,
            "features": features,
            "colorways": colorways,
            "description": f"Advanced {style} vehicle concept built for {car_model}."
        }
        
        session['history'].insert(0, concept)
        session.modified = True
        
        return jsonify({"status": "success", "concept": concept})

    return render_template_string(LAYOUT_TEMPLATE + """
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

                    <button type="submit" class="btn-primary">Generate Concept & Colorways</button>
                </form>
            </div>

            <div class="preview-panel">
                <h2>Interactive SVG Render Preview</h2>
                <div class="placeholder-render">
                    <svg id="car-svg" viewBox="0 0 600 300" width="100%" height="100%">
                        <rect width="600" height="300" fill="#111" rx="12"/>
                        <!-- Dynamic SVG Car Body -->
                        <path id="car-body" d="M80,210 L150,140 C200,130 350,130 420,140 L520,210 Z" fill="#38bdf8" style="transition: fill 0.4s ease;"/>
                        <path id="car-roof" d="M190,140 L230,90 L370,90 L410,140 Z" fill="#27272a" style="transition: fill 0.4s ease;"/>
                        <!-- Wheels -->
                        <circle cx="170" cy="210" r="28" fill="#18181b" stroke="#3f3f46" stroke-width="6"/>
                        <circle cx="430" cy="210" r="28" fill="#18181b" stroke="#3f3f46" stroke-width="6"/>
                        <text id="svg-label" x="300" y="50" fill="#a1a1aa" font-size="14" text-anchor="middle">Configure brief to render active SVG model</text>
                    </svg>
                </div>
                
                <!-- Colorway Tabs Container -->
                <div id="colorway-tabs" class="colorway-container"></div>
                
                <!-- Color Information Panel -->
                <div id="info-panel" class="info-box">Select or generate a design brief to view interactive colorways[cite: 23].</div>
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
                const carRoof = document.getElementById('car-roof');
                const svgLabel = document.getElementById('svg-label');
                const tabsContainer = document.getElementById('colorway-tabs');
                const infoPanel = document.getElementById('info-panel');

                svgLabel.textContent = `${concept.model} — Live Interactive Preview`;
                tabsContainer.innerHTML = '';

                // Dynamically build colorway tabs and wire single-click synchronization[cite: 23]
                concept.colorways.forEach((cw, index) => {
                    const btn = document.createElement('button');
                    btn.className = `color-tab ${index === 0 ? 'active' : ''}`;
                    btn.innerText = cw.name;
                    
                    btn.onclick = () => {
                        // Update active tab styling
                        document.querySelectorAll('.color-tab').forEach(b => b.classList.remove('active'));
                        btn.classList.add('active');
                        
                        // Update SVG element colors instantly[cite: 23]
                        carBody.setAttribute('fill', cw.accent);
                        carRoof.setAttribute('fill', cw.primary);
                        
                        // Update color information panel together[cite: 23]
                        infoPanel.innerHTML = `<strong>Colorway:</strong> ${cw.name} <br>` +
                                              `<strong>Primary Finish:</strong> ${cw.primary} | <strong>Accent Glow:</strong> ${cw.accent}<br>` +
                                              `<em style="color:#d4d4d8; display:block; margin-top:4px;">${cw.description}</em>`;
                    };
                    tabsContainer.appendChild(btn);
                });

                // Initialize default selection with the first colorway
                if(concept.colorways.length > 0) {
                    const defaultCw = concept.colorways[0];
                    carBody.setAttribute('fill', defaultCw.accent);
                    carRoof.setAttribute('fill', defaultCw.primary);
                    infoPanel.innerHTML = `<strong>Colorway:</strong> ${defaultCw.name} <br>` +
                                          `<strong>Primary Finish:</strong> ${defaultCw.primary} | <strong>Accent Glow:</strong> ${defaultCw.accent}<br>` +
                                          `<em style="color:#d4d4d8; display:block; margin-top:4px;">${defaultCw.description}</em>`;
                }
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
            <p style="color: #a1a1aa; margin-top: 0.5rem;">Review previously configured vehicle concepts and variations.</p>
            {% if history %}
                <div class="grid-history">
                    {% for item in history %}
                    <div class="history-card">
                        <h3>{{ item.model }}</h3>
                        <p><strong>Style:</strong> {{ item.style }}</p>
                        <p><strong>Features:</strong> {{ item.features }}</p>
                        <p style="margin-top:6px; color:#a1a1aa; font-size:0.9rem;">{{ item.description }}</p>
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <p style="margin-top: 1.5rem; color: #a1a1aa;">No concepts generated yet. Head over to the <a href="/studio" style="color: #38bdf8;">Studio</a>!</p>
            {% endif %}
        </div>
    """, history=user_history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)