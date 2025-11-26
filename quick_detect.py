"""
Quick Detect - Command line tool for simple detection
Usage: python quick_detect.py link "url" or python quick_detect.py message "text"
"""

from fake_detector import FakeDetector
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print('  python quick_detect.py link "https://www.example.com"')
        print('  python quick_detect.py message "Your message text"')
        return
    
    detector = FakeDetector()
    check_type = sys.argv[1].lower()
    text = sys.argv[2]
    
    if check_type == 'link' or check_type == 'url':
        result = detector.detect_url(text)
        status = "FAKE" if result['is_fake'] else "LEGITIMATE"
        print(f"\nLink: {text}")
        print(f"Result: {status}")
    
    elif check_type == 'message' or check_type == 'msg':
        result = detector.detect_message(text)
        status = "FAKE" if result['is_fake'] else "LEGITIMATE"
        print(f"\nMessage: {text}")
        print(f"Result: {status}")
    
    else:
        print("Error: First argument must be 'link' or 'message'")
        print("Usage: python quick_detect.py <link|message> <text>")

if __name__ == "__main__":
    main()


