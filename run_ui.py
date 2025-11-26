"""
Run the Web UI for Fake Detection System
"""

import os
import sys

def check_models():
    """Check if models exist"""
    if not os.path.exists('models/url_model.pkl') or not os.path.exists('models/message_model.pkl'):
        print("=" * 70)
        print("WARNING: Models not found!")
        print("=" * 70)
        print("\nPlease train the models first:")
        print("  python train_models.py")
        print("\nThen run this script again.")
        print("=" * 70)
        return False
    return True

def main():
    """Main function"""
    print("=" * 70)
    print("AI Fake Detection System - Web Interface")
    print("=" * 70)
    
    if not check_models():
        sys.exit(1)
    
    print("\nStarting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)
    
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()


