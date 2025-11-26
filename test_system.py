"""
Quick Test Script
Tests the fake detection system with sample inputs
"""

from fake_detector import FakeDetector
import os

def test_system():
    """Test the detection system"""
    print("Testing Fake Detection System...")
    print("=" * 60)
    
    # Check if models exist
    if not os.path.exists('models/url_model.pkl') or not os.path.exists('models/message_model.pkl'):
        print("⚠️  Models not found. Please run 'python train_models.py' first.")
        return False
    
    detector = FakeDetector()
    
    # Test URL detection
    print("\n1. Testing URL Detection:")
    print("-" * 60)
    
    test_urls = [
        ('https://www.google.com', False),  # Should be legitimate
        ('http://bit.ly/verify-now', True),  # Should be fake
    ]
    
    for url, expected_fake in test_urls:
        result = detector.detect_url(url)
        status = "✓" if result['is_fake'] == expected_fake else "✗"
        print(f"{status} URL: {url[:50]}")
        print(f"   Expected: {'Fake' if expected_fake else 'Legitimate'}, Got: {'Fake' if result['is_fake'] else 'Legitimate'} ({result['confidence']:.1%})")
    
    # Test message detection
    print("\n2. Testing Message Detection:")
    print("-" * 60)
    
    test_messages = [
        ('Hello, how are you?', False),  # Should be legitimate
        ('URGENT! Click here NOW to verify!', True),  # Should be fake
    ]
    
    for message, expected_fake in test_messages:
        result = detector.detect_message(message)
        status = "✓" if result['is_fake'] == expected_fake else "✗"
        print(f"{status} Message: {message[:50]}")
        print(f"   Expected: {'Fake' if expected_fake else 'Legitimate'}, Got: {'Fake' if result['is_fake'] else 'Legitimate'} ({result['confidence']:.1%})")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    return True

if __name__ == "__main__":
    test_system()

