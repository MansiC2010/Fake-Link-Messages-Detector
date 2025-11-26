"""
AI-Based Fake Detection System
Detects fake links and messages using machine learning
Analyzes URL/message characteristics - works for all links, not just known domains
"""

from fake_detector import FakeDetector

def check_url(url, simple=False):
    """Check if a URL is fake"""
    detector = FakeDetector()
    result = detector.detect_url(url)
    
    if simple:
        # Simple mode - just show FAKE or LEGITIMATE
        status = "FAKE" if result['is_fake'] else "LEGITIMATE"
        print(f"\n{'=' * 70}")
        print(f"RESULT: {status}")
        print(f"{'=' * 70}")
    else:
        # Detailed mode
        print("\n" + "=" * 70)
        print("URL DETECTION RESULT")
        print("=" * 70)
        print(f"URL: {url}")
        print(f"\nStatus: {'[FAKE]' if result['is_fake'] else '[LEGITIMATE]'}")
        print(f"Confidence: {result['confidence']:.1%}")
        
        print("\nReasons:")
        for i, reason in enumerate(result['reasons'], 1):
            print(f"  {i}. {reason}")
        print("=" * 70)
    
    return result

def check_message(message, simple=False):
    """Check if a message is fake"""
    detector = FakeDetector()
    result = detector.detect_message(message)
    
    if simple:
        # Simple mode - just show FAKE or LEGITIMATE
        status = "FAKE" if result['is_fake'] else "LEGITIMATE"
        print(f"\n{'=' * 70}")
        print(f"RESULT: {status}")
        print(f"{'=' * 70}")
    else:
        # Detailed mode
        print("\n" + "=" * 70)
        print("MESSAGE DETECTION RESULT")
        print("=" * 70)
        print(f"Message: {message}")
        print(f"\nStatus: {'[FAKE]' if result['is_fake'] else '[LEGITIMATE]'}")
        print(f"Confidence: {result['confidence']:.1%}")
        
        print("\nReasons:")
        for i, reason in enumerate(result['reasons'], 1):
            print(f"  {i}. {reason}")
        print("=" * 70)
    
    return result

def main():
    """Main interactive function"""
    print("=" * 70)
    print("Fake Link and Message Detector")
    print("Check your own URLs and messages for fake/spam content")
    print("=" * 70)
    
    detector = FakeDetector()
    
    # Ask for simple or detailed mode
    print("\nChoose display mode:")
    print("1. Simple mode (just shows FAKE or LEGITIMATE)")
    print("2. Detailed mode (shows reasons and confidence)")
    mode_choice = input("\nEnter mode (1 or 2, default=1): ").strip()
    simple_mode = (mode_choice != '2')
    
    while True:
        print("\nWhat would you like to check?")
        print("1. Check a URL/Link")
        print("2. Check a Message/Text")
        print("3. Check multiple URLs (paste one per line, empty line to finish)")
        print("4. Check multiple Messages (paste one per line, empty line to finish)")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            url = input("\nEnter the URL to check: ").strip()
            if url:
                check_url(url, simple=simple_mode)
            else:
                print("No URL provided.")
        
        elif choice == '2':
            message = input("\nEnter the message to check: ").strip()
            if message:
                check_message(message, simple=simple_mode)
            else:
                print("No message provided.")
        
        elif choice == '3':
            print("\nEnter URLs (one per line). Press Enter twice when done:")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)
            
            if urls:
                print(f"\nChecking {len(urls)} URL(s)...")
                for url in urls:
                    check_url(url, simple=simple_mode)
            else:
                print("No URLs provided.")
        
        elif choice == '4':
            print("\nEnter messages (one per line). Press Enter twice when done:")
            messages = []
            while True:
                message = input().strip()
                if not message:
                    break
                messages.append(message)
            
            if messages:
                print(f"\nChecking {len(messages)} message(s)...")
                for message in messages:
                    check_message(message, simple=simple_mode)
            else:
                print("No messages provided.")
        
        elif choice == '5':
            print("\nThank you for using the Fake Detection System!")
            break
        
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()

