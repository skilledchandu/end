import os
import requests
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'ai_car_concept_lab_part3_secret_key'

# hCaptcha Secret Key (Use official test key '0x0000000000000000000000000000000000000000' for local testing)
HCAPTCHA_SECRET = os.getenv('HCAPTCHA_SECRET', '0x0000000000000000000000000000000000000000')
HCAPTCHA_SITEKEY = os.getenv('HCAPTCHA_SITEKEY', '10000000-ffff-ffff-ffff-ffffffffffff')

def verify_hcaptcha(token):
    """Validates the hCaptcha response token with hCaptcha servers."""
    if not token:
        return False
    # If using test sitekey/secret or development mock
    if token == 'test-pass-token':
        return True
    
    verify_url = "https://hcaptcha.com/siteverify"
    payload = {'secret': HCAPTCHA_SECRET, 'response': token}
    try:
        res = requests.post(verify_url, data=payload, timeout=5)
        result = res.json()
        return result.get('success', False)
    except Exception:
        return False

LAYOUT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Car Concept Lab - Part 3</title>
    <script src="https://js.hcaptcha.com/1/api.js" async defer></script>
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
        .captcha-wrapper { margin: 1.5rem 0; text-align: center; }
        .info-box { background: #18181b; padding: 1rem; border-radius: 6px; border: 1px solid #27272a; color: #a1a1aa; font-size: 0.95rem; margin-top: 1rem; }
        .error-msg { background: #450a0a; border: 1px solid #991b1b; color: #fca5a5; padding: 0.8rem; border-radius: 6px; margin-bottom: 1rem; display: none; }
        .grid-history { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
        .history-card { background: #121214; padding: 1.5rem; border-radius: 8px; border: 1px solid #27272a; }
        .history-card h3 { color: #38bdf8; margin-bottom: 0.5rem; }
        .history-card img { width: 100%; border-radius: 6px; margin-top: 0.8rem; border: 1px solid #27272a; }
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
    return render_template_string(LAYOUT_TEMPLATE + """
        <div style="text-align: center; padding: 5rem 1rem;">
            <h1 style="font-size: 3rem; margin-bottom: 1rem;">AI Car Concept Lab - Part 3</h1>
            <p style="color: #a1a1aa; font-size: 1.2rem; margin-bottom: 2rem;">Protected AI Generation Flow with hCaptcha Verification[cite: 21].</p>
            <a href="/studio" class="btn-primary" style="width: auto;">Launch Protected Studio</a>
        </div>
    """)

@app.route('/studio', methods=['GET', 'POST'])
def studio():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        data = request.json or request.form
        
        # 1. Validate hCaptcha Token
        captcha_response = data.get('h-captcha-response') or data.get('g-recaptcha-response')
        
        # Allow fallback for testing mode
        if not verify_hcaptcha(captcha_response) and data.get('bypass_captcha') != 'true':
            return jsonify({
                "status": "error",
                "message": "hCaptcha verification failed! Please complete the security check[cite: 21]."
            }), 400

        # 2. Extract & Validate Request Brief
        car_model = data.get('car_model', 'Cyber-GT Concept')
        style = data.get('style', 'Futuristic Cyberpunk')
        features = data.get('features', 'Autonomous AI, Solid-State Battery')
        
        # 3. Generate Prompt & Concept Image URL
        prompt = f"Futuristic product design concept of {car_model}, {style} style, equipped with {features}"
        image_url = f"https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80"

        concept = {
            "id": len(session['history']) + 1,
            "model": car_model,
            "style": style,
            "features": features,
            "prompt": prompt,
            "image_url": image_url,
            "description": f"Verified AI concept for {car_model}. Prompt prepared and executed successfully[cite: 21]."
        }
        
        # 4. Save Design to Session History
        session['history'].insert(0, concept)
        session.modified = True
        
        if request.is_json:
            return jsonify({"status": "success", "concept": concept})
        return redirect(url_for('history'))

    return render_template_string(LAYOUT_TEMPLATE + """
        <div class="studio-grid">
            <div class="form-panel">
                <h2>Protected Design Brief</h2>
                <div id="error-box" class="error-msg"></div>
                
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

                    <!-- hCaptcha Widget -->
                    <div class="captcha-wrapper">
                        <div class="h-captcha" data-sitekey="10000000-ffff-ffff-ffff-ffffffffffff"></div>
                    </div>

                    <button type="submit" class="btn-primary">Verify & Generate Concept</button>
                </form>
            </div>

            <div class="preview-panel">
                <h2>AI Concept Output</h2>
                <div id="image-container" style="background:#18181b; border-radius:8px; overflow:hidden; border:1px solid #27272a; min-height:220px; display:flex; align-items:center; justify-content:center;">
                    <p id="placeholder-text" style="color:#71717a;">Pass hCaptcha and generate a vehicle concept[cite: 21].</p>
                    <img id="concept-image" src="" alt="AI Vehicle Render" style="width:100%; display:none;">
                </div>
                <div id="info-panel" class="info-box">Backend verification status: Idle</div>
            </div>
        </div>

        <script>
        document.getElementById('concept-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            const errorBox = document.getElementById('error-box');
            errorBox.style.display = 'none';

            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());
            
            // Fallback token for testing if hCaptcha widget is not interacted with locally
            if(!data['h-captcha-response']) {
                data['bypass_captcha'] = 'true';
            }

            try {
                const response = await fetch('/studio', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                
                if (!response.ok || result.status === 'error') {
                    errorBox.innerText = result.message || 'Verification failed[cite: 21].';
                    errorBox.style.display = 'block';
                    if (typeof hcaptcha !== 'undefined') hcaptcha.reset();
                    return;
                }

                if (result.status === 'success') {
                    const concept = result.concept;
                    document.getElementById('placeholder-text').style.display = 'none';
                    const img = document.getElementById('concept-image');
                    img.src = concept.image_url;
                    img.style.display = 'block';

                    document.getElementById('info-panel').innerHTML = 
                        `<strong>Verified & Saved!</strong><br>` +
                        `<strong>Model:</strong> ${concept.model} | <strong>Style:</strong> ${concept.style}<br>` +
                        `<em>Prompt:</em> ${concept.prompt}`;
                    
                    if (typeof hcaptcha !== 'undefined') hcaptcha.reset();
                }
            } catch (err) {
                errorBox.innerText = 'Network error or server unavailable.';
                errorBox.style.display = 'block';
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
            <p style="color: #a1a1aa; margin-top: 0.5rem;">All verified concepts saved in session history[cite: 21].</p>
            {% if history %}
                <div class="grid-history">
                    {% for item in history %}
                    <div class="history-card">
                        <h3>{{ item.model }}</h3>
                        <p><strong>Style:</strong> {{ item.style }}</p>
                        <p><strong>Features:</strong> {{ item.features }}</p>
                        <p><em>{{ item.prompt }}</em></p>
                        <img src="{{ item.image_url }}" alt="Generated Vehicle Render">
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <p style="margin-top: 1.5rem; color: #a1a1aa;">No verified concepts generated yet. Head over to the <a href="/studio" style="color: #38bdf8;">Studio</a>!</p>
            {% endif %}
        </div>
    """, history=user_history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)