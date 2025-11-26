"""
Flask Web Application for Fake Message and Link Detection
Modern web interface for the AI detection system
"""

import base64
import io
from functools import wraps

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from fake_detector import FakeDetector
from fake_detection_db import FakeDetectionDB
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fake-detection-secret-key-2024'

# Simple user credentials (in production, use a database with hashed passwords)
USERS = {
    'admin': 'admin123',  # username: password
    'user': 'user123',
    'demo': 'demo123'
}

# Initialize detector and database
detector = FakeDetector()
db = FakeDetectionDB()

FILTER_MAP = {
    "fake_link": ("link", "FAKE"),
    "legit_link": ("link", "LEGITIMATE"),
    "fake_message": ("message", "FAKE"),
    "legit_message": ("message", "LEGITIMATE"),
}

CHART_TYPES = {"bar", "histogram", "scatter", "box", "line"}


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def _generate_chart_image(df: pd.DataFrame, chart_type: str, title: str) -> str:
    plt.clf()
    sns.set_theme(style="darkgrid")
    fig, ax = plt.subplots(figsize=(8, 4))

    if chart_type == "bar":
        sns.barplot(data=df, x="index", y="percent", ax=ax, color="#6366f1")
        ax.set_xlabel("Detection #")
        ax.set_ylabel("Confidence (%)")
    elif chart_type == "histogram":
        sns.histplot(x=df["percent"], bins=10, ax=ax, color="#8b5cf6")
        ax.set_xlabel("Confidence (%)")
        ax.set_ylabel("Frequency")
    elif chart_type == "scatter":
        ax.scatter(df["index"], df["percent"], color="#10b981")
        ax.set_xlabel("Detection #")
        ax.set_ylabel("Confidence (%)")
    elif chart_type == "box":
        sns.boxplot(y=df["percent"], ax=ax, color="#fbbf24")
        ax.set_ylabel("Confidence (%)")
    elif chart_type == "line":
        ax.plot(df["index"], df["percent"], color="#3b82f6", marker="o")
        ax.set_xlabel("Detection #")
        ax.set_ylabel("Confidence (%)")

    ax.set_title(title)
    ax.set_ylim(0, 100)
    plt.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    # If already logged in, redirect to main page
    if session.get('logged_in'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        # Check credentials
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return jsonify({
                'success': True,
                'message': 'Login successful'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid username or password'
            }), 401
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout route"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    """Main page"""
    return render_template('index.html', username=session.get('username', 'User'))

@app.route('/detect/url', methods=['POST'])
@login_required
def detect_url():
    """API endpoint for URL detection"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        result = detector.detect_url(url)
        prediction = "FAKE" if result["is_fake"] else "LEGITIMATE"
        db.insert_detection(url, prediction, float(result.get("confidence", 0.0)), detection_type="link")
        
        return jsonify({
            'success': True,
            'is_fake': result['is_fake'],
            'confidence': round(result['confidence'] * 100, 2),
            'reasons': result['reasons'],
            'url': url
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/detect/message', methods=['POST'])
@login_required
def detect_message():
    """API endpoint for message detection"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        result = detector.detect_message(message)
        prediction = "FAKE" if result["is_fake"] else "LEGITIMATE"
        db.insert_detection(message, prediction, float(result.get("confidence", 0.0)), detection_type="message")
        
        return jsonify({
            'success': True,
            'is_fake': result['is_fake'],
            'confidence': round(result['confidence'] * 100, 2),
            'reasons': result['reasons'],
            'message': message
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/analytics', methods=['POST'])
@login_required
def analytics():
    data = request.get_json(silent=True) or {}
    filter_key = data.get("filter_type")
    chart_type = data.get("chart_type")

    if filter_key not in FILTER_MAP:
        return jsonify({"success": False, "error": "Invalid dataset selection."}), 400

    if chart_type not in CHART_TYPES:
        return jsonify({"success": False, "error": "Invalid chart type."}), 400

    detection_type, prediction_label = FILTER_MAP[filter_key]
    rows = db.fetch_by_filter(detection_type=detection_type, prediction_label=prediction_label, limit=200)

    if not rows:
        return jsonify({"success": False, "error": "No data available for this selection."}), 404

    df = pd.DataFrame(rows)
    df["percent"] = df["detection_percent"] * 100
    df["index"] = range(1, len(df) + 1)

    title = f"{prediction_label.title()} {detection_type.title()}s ({chart_type.title()} Chart)"
    image_data = _generate_chart_image(df, chart_type, title)

    return jsonify({"success": True, "image": image_data})


if __name__ == '__main__':
    # Check if models exist
    if not os.path.exists('models/url_model.pkl'):
        print("Warning: Models not found. Please run 'python train_models.py' first.")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
