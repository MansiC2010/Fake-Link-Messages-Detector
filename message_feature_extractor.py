"""
Message Feature Extractor
Extracts linguistic and structural features from messages to detect fake/spam content
"""

import re
import math
from collections import Counter


class MessageFeatureExtractor:
    """Extracts features from text messages for fake message detection"""
    
    def __init__(self):
        # Suspicious words/phrases
        self.suspicious_phrases = [
            'click here', 'act now', 'limited time', 'urgent', 'verify',
            'suspended', 'locked', 'expired', 'confirm', 'update now',
            'congratulations', 'you won', 'free money', 'claim now',
            'click below', 'verify account', 'update payment', 'security alert'
        ]
        
        # Urgency indicators
        self.urgency_words = [
            'urgent', 'immediate', 'asap', 'now', 'today', 'expires',
            'limited', 'hurry', 'act fast', 'deadline'
        ]
        
        # Financial scam indicators
        self.financial_keywords = [
            'bank', 'account', 'payment', 'credit card', 'debit',
            'transfer', 'refund', 'invoice', 'billing', 'paypal',
            'bitcoin', 'crypto', 'investment', 'profit'
        ]
        
        # Authority impersonation
        self.authority_keywords = [
            'irs', 'fbi', 'police', 'court', 'government', 'official',
            'legal', 'warrant', 'arrest', 'lawsuit'
        ]
    
    def extract_features(self, message):
        """
        Extract comprehensive features from a message
        
        Returns:
            dict: Dictionary of features
        """
        if not message or not isinstance(message, str):
            return self._get_default_features()
        
        message_lower = message.lower()
        features = {}
        
        # Basic text features
        features['message_length'] = len(message)
        features['word_count'] = len(message.split())
        features['char_count'] = len(message.replace(' ', ''))
        features['sentence_count'] = len(re.split(r'[.!?]+', message))
        features['avg_word_length'] = sum(len(word) for word in message.split()) / max(len(message.split()), 1)
        
        # Character type features
        features['uppercase_count'] = sum(1 for c in message if c.isupper())
        features['lowercase_count'] = sum(1 for c in message if c.islower())
        features['digit_count'] = sum(1 for c in message if c.isdigit())
        features['special_char_count'] = sum(1 for c in message if c in '!@#$%^&*()_+-=[]{}|;:,.<>?')
        features['exclamation_count'] = message.count('!')
        features['question_mark_count'] = message.count('?')
        features['all_caps_ratio'] = features['uppercase_count'] / max(len(message), 1)
        
        # URL/Link features in message
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, message)
        features['url_count'] = len(urls)
        features['has_url'] = 1 if len(urls) > 0 else 0
        
        # Suspicious phrase features (more sensitive)
        features['suspicious_phrase_count'] = sum(1 for phrase in self.suspicious_phrases if phrase in message_lower)
        features['has_suspicious_phrase'] = 1 if features['suspicious_phrase_count'] > 0 else 0
        # Add weight for multiple suspicious phrases
        features['suspicious_phrase_weight'] = min(features['suspicious_phrase_count'] * 0.5, 3.0)
        
        # Urgency features (more sensitive)
        features['urgency_word_count'] = sum(1 for word in self.urgency_words if word in message_lower)
        features['has_urgency'] = 1 if features['urgency_word_count'] > 0 else 0
        # Add weight for urgency
        features['urgency_weight'] = min(features['urgency_word_count'] * 0.3, 2.0)
        
        # Financial scam features
        features['financial_keyword_count'] = sum(1 for keyword in self.financial_keywords if keyword in message_lower)
        features['has_financial_keywords'] = 1 if features['financial_keyword_count'] > 0 else 0
        
        # Authority impersonation features
        features['authority_keyword_count'] = sum(1 for keyword in self.authority_keywords if keyword in message_lower)
        features['has_authority_keywords'] = 1 if features['authority_keyword_count'] > 0 else 0
        
        # Linguistic features
        features['entropy'] = self._calculate_entropy(message)
        features['punctuation_density'] = features['special_char_count'] / max(len(message), 1)
        
        # Repetition features (spam often has repeated words)
        words = message_lower.split()
        if words:
            word_freq = Counter(words)
            most_common_count = word_freq.most_common(1)[0][1] if word_freq else 0
            features['max_word_repetition'] = most_common_count
            features['unique_word_ratio'] = len(set(words)) / max(len(words), 1)
        else:
            features['max_word_repetition'] = 0
            features['unique_word_ratio'] = 0
        
        # Email/phone pattern features
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        features['email_count'] = len(re.findall(email_pattern, message))
        features['phone_count'] = len(re.findall(phone_pattern, message))
        
        # Grammar/spelling indicators (very basic - high ratio might indicate issues)
        features['typo_indicators'] = self._count_potential_typos(message)
        
        # Ratio features
        if features['word_count'] > 0:
            features['url_to_word_ratio'] = features['url_count'] / features['word_count']
            features['suspicious_to_word_ratio'] = features['suspicious_phrase_count'] / features['word_count']
        else:
            features['url_to_word_ratio'] = 0
            features['suspicious_to_word_ratio'] = 0
        
        return features
    
    def _calculate_entropy(self, text):
        """Calculate Shannon entropy of text"""
        if not text:
            return 0
        
        prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        entropy = -sum([p * math.log2(p) for p in prob if p > 0])
        return entropy
    
    def _count_potential_typos(self, text):
        """Count potential typo indicators (repeated characters, unusual patterns)"""
        # Count repeated characters (like "loooook", "freeee")
        repeated_chars = len(re.findall(r'(.)\1{2,}', text))
        return repeated_chars
    
    def _get_default_features(self):
        """Return default feature values for invalid messages"""
        return {
            'message_length': 0, 'word_count': 0, 'char_count': 0, 'sentence_count': 0,
            'avg_word_length': 0, 'uppercase_count': 0, 'lowercase_count': 0,
            'digit_count': 0, 'special_char_count': 0, 'exclamation_count': 0,
            'question_mark_count': 0, 'all_caps_ratio': 0, 'url_count': 0, 'has_url': 0,
            'suspicious_phrase_count': 0, 'has_suspicious_phrase': 0, 'urgency_word_count': 0,
            'has_urgency': 0, 'financial_keyword_count': 0, 'has_financial_keywords': 0,
            'authority_keyword_count': 0, 'has_authority_keywords': 0, 'entropy': 0,
            'punctuation_density': 0, 'max_word_repetition': 0, 'unique_word_ratio': 0,
            'email_count': 0, 'phone_count': 0, 'typo_indicators': 0,
            'url_to_word_ratio': 0, 'suspicious_to_word_ratio': 0
        }
    
    def get_feature_names(self):
        """Get list of all feature names"""
        return list(self._get_default_features().keys())

