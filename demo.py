"""
Demo Script
Demonstrates the fake message and link detection system
"""

from fake_detector import FakeDetector
import os

def print_result(result, item_type="URL"):
    """Pretty print detection result"""
    print("\n" + "=" * 70)
    print(f"{item_type} Analysis Result")
    print("=" * 70)
    
    if item_type == "URL":
        print(f"URL: {result.get('url', 'N/A')}")
    else:
        print(f"Message: {result.get('message', 'N/A')[:100]}...")
    
    print(f"\nStatus: {'[FAKE]' if result['is_fake'] else '[LEGITIMATE]'}")
    print(f"Confidence: {result['confidence']:.1%}")
    
    print("\nReasons:")
    for i, reason in enumerate(result['reasons'], 1):
        print(f"  {i}. {reason}")
    
    print("=" * 70)

def main():
    print("=" * 70)
    print("Fake Message and Link Detection System")
    print("=" * 70)
    
    # Check if models exist
    if not os.path.exists('models/url_model.pkl') or not os.path.exists('models/message_model.pkl'):
        print("\n⚠️  Models not found. Training models first...")
        print("This may take a few moments.\n")
        import train_models
        detector_instance = train_models.detector
    else:
        detector_instance = FakeDetector()
    
    print("\n" + "=" * 70)
    print("URL Detection Examples")
    print("=" * 70)
    
    # Test URLs
    test_urls = [
        'https://www.google.com',
        'https://github.com/user/repo',
        'http://bit.ly/verify-account-now',
        'https://verify-payment.tk/urgent',
        'http://192.168.1.100/login',
        'https://www.amazon.com/product/123',
        'https://update-account.ml/secure',
        'https://stackoverflow.com/questions/12345'
    ]
    
    for url in test_urls:
        result = detector_instance.detect_url(url)
        print_result(result, "URL")
    
    print("\n" + "=" * 70)
    print("Message Detection Examples")
    print("=" * 70)
    
    # Test messages
    test_messages = [
        'Hello, how are you doing today?',
        'URGENT! Your account has been SUSPENDED! Click here NOW to verify: http://bit.ly/verify-now',
        'Thank you for your email. I will get back to you soon.',
        'CONGRATULATIONS! You won $1,000,000! Claim your prize NOW!',
        'The meeting is scheduled for tomorrow at 3 PM.',
        'Your payment has EXPIRED! Update immediately or your account will be LOCKED!',
        'Your package has been delivered to your address.',
        'VERIFY your account NOW or it will be DELETED! Click below!'
    ]
    
    for message in test_messages:
        result = detector_instance.detect_message(message)
        print_result(result, "Message")
    
    print("\n" + "=" * 70)
    print("Interactive Mode")
    print("=" * 70)
    print("\nYou can now test your own URLs and messages.")
    print("Type 'quit' to exit.\n")
    
    while True:
        print("\nWhat would you like to check?")
        print("1. URL")
        print("2. Message")
        print("3. Quit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '3' or choice.lower() == 'quit':
            print("\nThank you for using the Fake Detection System!")
            break
        elif choice == '1':
            url = input("\nEnter URL to check: ").strip()
            if url:
                result = detector_instance.detect_url(url)
                print_result(result, "URL")
        elif choice == '2':
            message = input("\nEnter message to check: ").strip()
            if message:
                result = detector_instance.detect_message(message)
                print_result(result, "Message")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

