"""
AI-Based Fake Detection - Detects FAKE or LEGITIMATE for any link or message
Uses machine learning to analyze URL/message characteristics
Works for all links, not just known domains
"""

from fake_detector import FakeDetector

def detect_link(url):
    """Detect if a link is fake - returns simple result"""
    detector = FakeDetector()
    result = detector.detect_url(url)
    
    if result['is_fake']:
        return "FAKE"
    else:
        return "LEGITIMATE"

def detect_message(message):
    """Detect if a message is fake - returns simple result"""
    detector = FakeDetector()
    result = detector.detect_message(message)
    
    if result['is_fake']:
        return "FAKE"
    else:
        return "LEGITIMATE"

def main():
    """Main function"""
    print("=" * 70)
    print("Simple Fake Detection - Messages and Links")
    print("=" * 70)
    
    detector = FakeDetector()
    
    while True:
        print("\nWhat do you want to check?")
        print("1. Check a Link/URL")
        print("2. Check a Message")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            url = input("\nEnter the link/URL: ").strip()
            if url:
                result = detector.detect_url(url)
                status = "FAKE" if result['is_fake'] else "LEGITIMATE"
                print(f"\n{'=' * 70}")
                print(f"RESULT: {status}")
                print(f"{'=' * 70}")
            else:
                print("No URL provided.")
        
        elif choice == '2':
            message = input("\nEnter the message: ").strip()
            if message:
                result = detector.detect_message(message)
                status = "FAKE" if result['is_fake'] else "LEGITIMATE"
                print(f"\n{'=' * 70}")
                print(f"RESULT: {status}")
                print(f"{'=' * 70}")
            else:
                print("No message provided.")
        
        elif choice == '3':
            print("\nThank you for using Simple Fake Detection!")
            break
        
        else:
            print("Invalid choice. Please enter 1-3.")

if __name__ == "__main__":
    main()

