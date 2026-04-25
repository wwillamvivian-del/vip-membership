from flask import Flask, render_template_string, request, send_from_directory, session
import os

app = Flask(__name__)
app.secret_key = "vip_secret_key" # Needed to remember the address

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.getcwd(), filename)

# OFFICIAL TRACKING CODE
VALID_CODE = "1066652772"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #f4f7f9; color: #333; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; margin: 0; padding: 0; }
        
        /* 1. LANDING & SETUP PAGES */
        .page-wrap { background: #050505; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding-top: 40px; text-align: center; color: white; }
        .gold-card {
            background: linear-gradient(135deg, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
            width: 90%; max-width: 400px; height: 230px; border-radius: 15px; padding: 20px; color: #1a1a1a; position: relative; text-align: left;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #91792e; box-sizing: border-box; margin-bottom: 30px;
        }
        .main-photo { width: 120px; height: 155px; border: 2px solid #1a1a1a; position: absolute; top: 45px; left: 20px; overflow: hidden; }
        .main-photo img { width: 100%; height: 100%; object-fit: cover; }
        .card-info { margin-left: 150px; margin-top: 40px; }
        .btn-gold { background: #bf953f; color: #fff; border: 1px solid #fcf6ba; padding: 18px; width: 90%; max-width: 400px; border-radius: 8px; font-weight: bold; cursor: pointer; text-transform: uppercase; border: none; font-size: 1.1rem; }
        .address-input { width: 85%; max-width: 380px; padding: 15px; margin: 10px 0; border-radius: 8px; border: 1px solid #bf953f; background: #222; color: white; font-size: 1rem; }

        /* 2. TRACKING INPUT (Package Info) */
        .shipping-input-container { background: white; min-height: 100vh; padding: 40px 25px; box-sizing: border-box; max-width: 500px; margin: 0 auto; color: #333; }
        .barcode-section { text-align: center; margin-bottom: 50px; }
        .main-title { font-size: 2.8rem; margin-bottom: 30px; font-weight: normal; text-align: left; }
        .info-row { border-top: 1px solid #eee; padding: 25px 0; display: flex; align-items: center; }
        .label { font-size: 1.4rem; font-weight: bold; width: 45%; text-align: left; }
        .value-input { width: 55%; font-size: 1.4rem; border: 2px solid #333; padding: 10px; border-radius: 4px; }

        /* 3. FINAL TRACKING STATUS */
        .track-header { background: #0071ce; color: white; padding: 18px; display: flex; align-items: center; font-size: 1.2rem; font-weight: bold; }
        .status-card { background: white; padding: 20px; margin-bottom: 10px; border-bottom: 1px solid #eee; }
        .transit-row { display: flex; align-items: center; margin-bottom: 15px; }
        .truck-icon { background: #e7f3ff; width: 55px; height: 55px; border-radius: 50%; margin-right: 15px; display: flex; align-items: center; justify-content: center; font-size: 1.6rem; }
        .progress-bar { display: flex; justify-content: space-between; margin: 25px 10px; position: relative; }
        .line { position: absolute; top: 10px; left: 0; right: 0; height: 4px; background: #ddd; z-index: 1; }
        .fill { position: absolute; top: 10px; left: 0; width: 66%; height: 4px; background: #0071ce; z-index: 2; }
        .dot { width: 20px; height: 20px; background: #0071ce; border-radius: 50%; z-index: 3; border: 4px solid white; box-shadow: 0 0 0 1px #0071ce; }
        .dot.pending { background: #ddd; box-shadow: none; }
        .alert-orange { background: #fff8f0; border: 1px solid #ffcc99; color: #663300; padding: 12px; border-radius: 4px; font-weight: bold; display: flex; align-items: center; font-size: 0.9rem; }
    </style>
</head>
<body>

    {% if step == 'landing' %}
    <div class="page-wrap">
        <div class="gold-card">
            <div style="font-weight:bold; font-size: 0.8rem;">MEMBERSHIP CARD</div>
            <div class="main-photo"><img src="nicole_portrait.png"></div>
            <div class="card-info">
                <span style="font-weight:bold; font-size:1.4rem;">Nicole Kidman</span><br>
                <span style="font-weight:bold; font-size:0.7rem;">OFFICIAL VIP GUEST</span>
            </div>
        </div>
        <form method="POST" action="/setup"><button class="btn-gold">ENTER</button></form>
    </div>

    {% elif step == 'setup' %}
    <div class="page-wrap">
        <h2 style="color: #bf953f;">Shipping Details</h2>
        <p>Please enter the delivery address for your card:</p>
        <form method="POST" action="/dashboard">
            <input type="text" name="full_name" class="address-input" placeholder="Full Name" required><br>
            <input type="text" name="address" class="address-input" placeholder="Street Address" required><br>
            <input type="text" name="city_state" class="address-input" placeholder="City, State, Zip" required><br>
            <button class="btn-gold" style="margin-top:20px;">SAVE & CONTINUE</button>
        </form>
    </div>

    {% elif step == 'dashboard' %}
    <div class="shipping-input-container">
        <div class="barcode-section">
            <img src="https://bwipjs-api.metafloor.com/?bcid=code128&text=102431141920&scale=3&rotate=N&includetext" style="width:280px;">
        </div>
        <h1 class="main-title">Package information</h1>
        <form method="POST" action="/track">
            <div class="info-row">
                <div class="label">Tracking<br>number</div>
                <input type="text" name="code" class="value-input" placeholder="Enter number" required>
            </div>
            <button class="btn-gold" style="width:100%; background:#c1943d;">CHECK STATUS</button>
        </form>
        {% if error %}<p style="color:red; text-align:center; font-weight:bold; margin-top:15px;">Invalid tracking number.</p>{% endif %}
    </div>

    {% elif step == 'status' %}
    <div class="track-header"><span style="margin-right:20px;">&#10094;</span> Track shipment</div>
    <div class="status-card">
        <div class="transit-row">
            <div class="truck-icon">&#128666;</div>
            <div>
                <b style="font-size:1.1rem;">In transit, arriving late</b><br>
                <span style="color:#666; font-size:0.9rem;">Estimated arrival Tue, Oct 07</span>
            </div>
        </div>
        <div class="progress-bar">
            <div class="line"></div><div class="fill"></div>
            <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot pending"></div>
        </div>
        <div class="alert-orange">
            <span style="background:#d9534f; color:white; border-radius:50%; width:18px; height:18px; display:inline-block; text-align:center; margin-right:10px;">!</span>
            Your order's running late!
        </div>
    </div>

    <div class="status-card">
        <div style="font-weight:bold; margin-bottom:8px;">Shipping address</div>
        <div style="line-height:1.4;">
            <b>{{ address_data['name'] }}</b><br>
            {{ address_data['street'] }}<br>
            {{ address_data['city'] }}
        </div>
    </div>

    <div class="status-card">
        <div style="font-weight:bold; display:flex; justify-content:space-between;">Order details <span style="color:#0071ce; font-weight:normal; text-decoration:underline; font-size:0.8rem;">See details</span></div>
        <div style="color:#666; font-size:0.8rem; margin-top:4px;">Order #10353133259</div>
        <div style="display:flex; align-items:center; margin-top:12px;">
            <div style="width:45px; height:45px; background:#eee; border-radius:4px; margin-right:12px; border:1px solid #ddd; overflow:hidden;">
                <img src="nicole_portrait.png" style="width:100%; height:100%; object-fit:cover;">
            </div>
            <b style="font-size:0.9rem;">1 VIP Gold Membership Card</b>
        </div>
    </div>
    {% endif %}

</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, step='landing')

@app.route('/setup', methods=['POST'])
def setup():
    return render_template_string(HTML_TEMPLATE, step='setup')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    # Save address to session so we can show it later
    session['address_data'] = {
        'name': request.form.get('full_name'),
        'street': request.form.get('address'),
        'city': request.form.get('city_state')
    }
    return render_template_string(HTML_TEMPLATE, step='dashboard')

@app.route('/track', methods=['POST'])
def track():
    if request.form.get("code") == VALID_CODE:
        return render_template_string(HTML_TEMPLATE, step='status', address_data=session.get('address_data'))
    return render_template_string(HTML_TEMPLATE, step='dashboard', error=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
