"""
Training Script
Generates synthetic training data and trains the fake detection models
"""

import numpy as np
from fake_detector import FakeDetector

# Initialize detector
detector = FakeDetector()

# Generate synthetic training data for URLs
print("=" * 60)
print("Generating URL Training Data...")
print("=" * 60)

# Legitimate URLs - diverse examples to train AI to recognize legitimate patterns
legitimate_urls = [
    'https://www.google.com/search?q=python',
    'https://github.com/user/repo',
    'https://stackoverflow.com/questions/12345',
    'https://www.wikipedia.org/wiki/Machine_Learning',
    'https://www.youtube.com/watch?v=abc123',
    'https://www.amazon.com/product/123456',
    'https://www.microsoft.com/en-us',
    'https://www.apple.com/iphone',
    'https://www.linkedin.com/in/profile',
    'https://www.instagram.com/user',
    'https://www.twitter.com/user',
    'https://www.facebook.com/page',
    'https://docs.python.org/3/library',
    'https://pypi.org/project/package',
    'https://www.reddit.com/r/programming',
    'https://www.netflix.com/watch/12345',
    'https://www.spotify.com/album/123',
    'https://www.ebay.com/itm/123456',
    'https://www.paypal.com/us/home',
    'https://example.com/page',
    'https://test-site.org/article/123',
    'https://mywebsite.net/blog/post',
    'https://company.io/products/item',
    'https://service.co.uk/account',
    'https://platform.dev/api/v1',
    'https://app.example.com/dashboard',
    'https://www.news-site.com/article/2024/01/title',
    'https://blog.example.org/2024/01/15/post-name',
    'https://shop.store.com/product/abc-123',
    'https://api.service.io/v2/users/456',
    'https://chatgpt.com/c/6919bf40-06dc-8323-b440-1381b717f112',
    'https://openai.com/api',
    'https://www.discord.com/channels/123',
    'https://zoom.us/j/123456789',
    'https://slack.com/workspace/123',
    'https://custom-domain.com/path/to/resource',
    'https://legitimate-site.org/section/page?id=123'
]

# Fake/Malicious URLs
fake_urls = [
    'http://bit.ly/abc123xyz',
    'https://verify-account.tk/login',
    'http://update-payment.ml/secure',
    'http://192.168.1.100/login',
    'https://click-here-now.ga/claim',
    'http://tinyurl.com/suspicious123',
    'https://account-suspended.cf/verify',
    'http://urgent-update.gq/confirm',
    'https://secure-login.xyz/validate',
    'http://update-now.tk/account',
    'https://verify-payment.ml/urgent',
    'http://click-below.ga/claim-now',
    'https://suspended-account.cf/verify-now',
    'http://update-account.gq/secure-login',
    'https://verify-urgent.xyz/click-here',
    'http://bit.ly/verify-account-now',
    'https://tinyurl.com/update-payment-urgent',
    'http://192.168.0.1:8080/login',
    'https://claim-free-money.tk/click',
    'http://congratulations-winner.ml/verify',
    'https://account-locked.ga/update-now',
    'http://payment-expired.cf/verify-account',
    'https://security-alert.gq/click-below',
    'http://verify-identity.xyz/urgent',
    'https://update-billing.tk/now',
    'http://confirm-payment.ml/verify',
    'https://account-verify.ga/update',
    'http://secure-update.cf/login',
    'https://validate-account.gq/click',
    'http://urgent-verify.xyz/now'
]

# Create labels
url_labels = [0] * len(legitimate_urls) + [1] * len(fake_urls)
all_urls = legitimate_urls + fake_urls

print(f"Total URL samples: {len(all_urls)}")
print(f"Legitimate: {len(legitimate_urls)}, Fake: {len(fake_urls)}")

# Train URL model
print("\n")
detector.train_url_model(all_urls, url_labels)

# Generate synthetic training data for messages
print("\n" + "=" * 60)
print("Generating Message Training Data...")
print("=" * 60)

# Legitimate messages
legitimate_messages = [
    'Hello, how are you doing today?',
    'The meeting is scheduled for tomorrow at 3 PM.',
    'Thank you for your email. I will get back to you soon.',
    'Can you please send me the report by Friday?',
    'I enjoyed reading your article about machine learning.',
    'The weather is nice today. Would you like to go for a walk?',
    'Your package has been delivered to your address.',
    'Your order #12345 has been confirmed and will ship soon.',
    'We received your payment. Thank you for your purchase.',
    'Your subscription will renew automatically next month.',
    'Here is the link to the document: https://docs.google.com/document',
    'The conference will be held on March 15th at the convention center.',
    'Please review the attached file and provide your feedback.',
    'I wanted to follow up on our conversation from yesterday.',
    'The project deadline has been extended to next week.',
    'Your account balance is $1,234.56 as of today.',
    'We have received your application and will review it shortly.',
    'The event registration is now open. Sign up at our website.',
    'Your flight has been confirmed. Check-in opens 24 hours before departure.',
    'Thank you for subscribing to our newsletter.',
    'Your password was successfully changed.',
    'We are pleased to inform you that your request has been approved.',
    'The maintenance window is scheduled for this weekend.',
    'Your invoice #INV-2024-001 is ready for payment.',
    'We have updated our privacy policy. Please review the changes.',
    'Your appointment is confirmed for next Tuesday at 2 PM.',
    'The new feature has been released. Check it out in the app.',
    'Your membership has been renewed for another year.',
    'We are experiencing high traffic. Please try again later.',
    'Your feedback is important to us. Thank you for your input.'
]

# Fake/Spam messages - More diverse examples
fake_messages = [
    'URGENT! Your account has been SUSPENDED! Click here NOW to verify: http://bit.ly/verify-now',
    'CONGRATULATIONS! You won $1,000,000! Claim your prize NOW at: https://claim-prize.tk',
    'Your payment has EXPIRED! Update immediately or your account will be LOCKED!',
    'VERIFY your account NOW or it will be DELETED! Click below: http://verify-account.ml',
    'URGENT SECURITY ALERT! Your account was accessed from unknown location. Verify NOW!',
    'You have been selected for a FREE iPhone! Click here to claim: http://free-phone.ga',
    'Your bank account needs verification! Click here IMMEDIATELY: https://bank-verify.cf',
    'ACT NOW! Limited time offer! Get 90% off! Click here: http://special-offer.tk',
    'Your PayPal account is LOCKED! Verify your identity NOW: https://paypal-verify.ml',
    'URGENT! Your credit card will be charged $500! Cancel now: http://cancel-charge.ga',
    'Click here to claim your prize!',
    'Act now before it is too late!',
    'Verify your identity immediately!',
    'Your account will be closed soon!',
    'Update your payment method now!',
    'Confirm your account details!',
    'Click below to verify!',
    'Urgent action required!',
    'Your subscription expires today!',
    'Claim your reward now!',
    'You won a lottery! Claim $50,000 NOW! Visit: https://lottery-win.cf',
    'Your Amazon account is SUSPENDED! Verify immediately: http://amazon-verify.gq',
    'SECURITY BREACH! Change your password NOW! Click: https://change-password.xyz',
    'Your Netflix subscription EXPIRED! Renew now to avoid interruption: http://renew-netflix.tk',
    'URGENT! Your email will be deleted in 24 hours! Verify now: https://email-verify.ml',
    'FREE MONEY! Transfer $1,000 to your account! Click here: http://free-money.ga',
    'Your account has been HACKED! Secure it NOW: https://secure-account.cf',
    'CONGRATULATIONS! You are eligible for a government grant! Apply now: http://grant-apply.gq',
    'URGENT UPDATE REQUIRED! Your software is outdated. Update now: https://update-now.xyz',
    'Your payment method FAILED! Update immediately: http://update-payment.tk',
    'You have 3 unread messages! Click here to view: https://messages-view.ml',
    'URGENT! Your insurance claim needs attention! Verify now: http://insurance-claim.ga',
    'Your tax refund is ready! Claim $2,500 now: https://tax-refund.cf',
    'SECURITY ALERT! Suspicious activity detected! Verify identity: http://verify-identity.gq',
    'Your delivery is delayed! Track package: https://track-delivery.xyz',
    'URGENT! Your subscription will be cancelled! Renew now: http://renew-sub.tk',
    'You have won a gift card! Claim $100 now: https://gift-card.ml',
    'Your account balance is LOW! Add funds now: http://add-funds.ga',
    'URGENT! Your order cannot be processed! Update payment: https://update-order.cf',
    'Your account verification is PENDING! Complete now: http://complete-verify.gq'
]

# Create labels
message_labels = [0] * len(legitimate_messages) + [1] * len(fake_messages)
all_messages = legitimate_messages + fake_messages

print(f"Total message samples: {len(all_messages)}")
print(f"Legitimate: {len(legitimate_messages)}, Fake: {len(fake_messages)}")

# Train message model
print("\n")
detector.train_message_model(all_messages, message_labels)

print("\n" + "=" * 60)
print("Training Complete!")
print("=" * 60)
print("\nModels have been saved to the 'models' directory.")
print("You can now use the detector to analyze URLs and messages.")

