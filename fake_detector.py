"""
Fake Message and Link Detector
Main AI module for detecting fake messages and links using machine learning
"""

import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

from url_feature_extractor import URLFeatureExtractor
from message_feature_extractor import MessageFeatureExtractor


class FakeDetector:
    """Main AI module for fake message and link detection"""
    
    def __init__(self):
        self.url_extractor = URLFeatureExtractor()
        self.message_extractor = MessageFeatureExtractor()
        self.url_model = None
        self.message_model = None
        self.url_scaler = StandardScaler()
        self.message_scaler = StandardScaler()
        self.model_dir = 'models'
        
        # Create models directory if it doesn't exist
        os.makedirs(self.model_dir, exist_ok=True)
    
    def train_url_model(self, urls, labels):
        """
        Train the URL detection model
        
        Args:
            urls: List of URLs (strings)
            labels: List of labels (1 for fake, 0 for legitimate)
        """
        print("Extracting URL features...")
        features = []
        for url in urls:
            feat_dict = self.url_extractor.extract_features(url)
            features.append(list(feat_dict.values()))
        
        X = np.array(features)
        y = np.array(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.url_scaler.fit_transform(X_train)
        X_test_scaled = self.url_scaler.transform(X_test)
        
        # Create ensemble model for higher accuracy
        rf = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        gb = GradientBoostingClassifier(
            n_estimators=150,
            max_depth=10,
            learning_rate=0.1,
            random_state=42
        )
        
        # Voting classifier for ensemble
        self.url_model = VotingClassifier(
            estimators=[('rf', rf), ('gb', gb)],
            voting='soft',
            weights=[2, 1]
        )
        
        print("Training URL detection model...")
        self.url_model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.url_model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"URL Model Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fake']))
        
        # Save model
        self._save_url_model()
        return accuracy
    
    def train_message_model(self, messages, labels):
        """
        Train the message detection model
        
        Args:
            messages: List of messages (strings)
            labels: List of labels (1 for fake, 0 for legitimate)
        """
        print("Extracting message features...")
        features = []
        for message in messages:
            feat_dict = self.message_extractor.extract_features(message)
            features.append(list(feat_dict.values()))
        
        X = np.array(features)
        y = np.array(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.message_scaler.fit_transform(X_train)
        X_test_scaled = self.message_scaler.transform(X_test)
        
        # Create ensemble model with better parameters for message detection
        rf = RandomForestClassifier(
            n_estimators=300,
            max_depth=25,
            min_samples_split=3,
            min_samples_leaf=1,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'  # Balance fake/legitimate detection
        )
        
        gb = GradientBoostingClassifier(
            n_estimators=200,
            max_depth=12,
            learning_rate=0.08,
            random_state=42,
            subsample=0.8
        )
        
        self.message_model = VotingClassifier(
            estimators=[('rf', rf), ('gb', gb)],
            voting='soft',
            weights=[3, 2]  # Give more weight to Random Forest
        )
        
        print("Training message detection model...")
        self.message_model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.message_model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Message Model Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fake']))
        
        # Save model
        self._save_message_model()
        return accuracy
    
    def detect_url(self, url):
        """
        Detect if a URL is fake
        
        Returns:
            dict: Detection result with prediction, probability, and reasons
        """
        if not self.url_model:
            self._load_url_model()
        
        if not self.url_model:
            return {
                'is_fake': False,
                'confidence': 0.0,
                'reasons': ['Model not trained. Please train the model first.']
            }
        
        # Extract features
        features = self.url_extractor.extract_features(url)
        feature_vector = np.array([list(features.values())])
        feature_vector_scaled = self.url_scaler.transform(feature_vector)
        
        # Predict using AI model
        predictions = self.url_model.predict(feature_vector_scaled)
        prediction = int(predictions[0])  # type: ignore
        probabilities = self.url_model.predict_proba(feature_vector_scaled)
        proba_array = probabilities[0]  # type: ignore
        confidence = float(proba_array[1] if prediction == 1 else proba_array[0])
        
        # Use AI prediction directly - no whitelist override
        # The model analyzes URL characteristics to determine if it's fake
        # This works for all links, not just known domains
        
        # Generate reasons
        reasons = self._explain_url_result(features, prediction, confidence)
        
        return {
            'is_fake': bool(prediction),
            'confidence': float(confidence),
            'reasons': reasons,
            'url': url
        }
    
    def detect_message(self, message):
        """
        Detect if a message is fake
        
        Returns:
            dict: Detection result with prediction, probability, and reasons
        """
        if not self.message_model:
            self._load_message_model()
        
        if not self.message_model:
            return {
                'is_fake': False,
                'confidence': 0.0,
                'reasons': ['Model not trained. Please train the model first.']
            }
        
        # Extract features
        features = self.message_extractor.extract_features(message)
        feature_vector = np.array([list(features.values())])
        feature_vector_scaled = self.message_scaler.transform(feature_vector)
        
        # Predict
        predictions = self.message_model.predict(feature_vector_scaled)
        prediction = int(predictions[0])  # type: ignore
        probabilities = self.message_model.predict_proba(feature_vector_scaled)
        proba_array = probabilities[0]  # type: ignore
        confidence = float(proba_array[1] if prediction == 1 else proba_array[0])
        
        # Generate reasons
        reasons = self._explain_message_result(features, prediction, confidence)
        
        return {
            'is_fake': bool(prediction),
            'confidence': float(confidence),
            'reasons': reasons,
            'message': message
        }
    
    def _explain_url_result(self, features, prediction, confidence):
        """Generate explanations for URL detection result"""
        reasons = []
        
        # Check if URL was invalid/malformed
        if features['url_length'] == 0 and features['suspicious_keyword_count'] >= 5:
            return ["[ERROR] Invalid or malformed URL format detected. Please check the URL and try again."]
        
        # AI-based detection - analyzes URL characteristics
        # Works for all links, not just whitelisted domains
        
        if prediction == 1:  # Fake
            reasons.append(f"Detected as FAKE with {confidence:.1%} confidence.")
            
            if features['is_short_url'] == 1:
                reasons.append("[WARNING] Contains a URL shortener (bit.ly, tinyurl, etc.) which can hide malicious destinations.")
            
            if features['suspicious_tld'] == 1:
                reasons.append("[WARNING] Uses a suspicious top-level domain (.tk, .ml, .ga, etc.) commonly used for scams.")
            
            if features['has_ip'] == 1:
                reasons.append("[WARNING] Uses an IP address instead of a domain name, which is unusual and suspicious.")
            
            if features['suspicious_keyword_count'] >= 3:
                reasons.append(f"[WARNING] Contains {features['suspicious_keyword_count']} suspicious keywords (verify, click, account, etc.).")
            
            if features['url_length'] > 150:
                reasons.append("[WARNING] URL is unusually long, which may indicate obfuscation or tracking parameters.")
            
            if features['url_entropy'] > 5.0:
                reasons.append("[WARNING] High URL entropy suggests random/obfuscated characters, common in phishing URLs.")
            
            if features['has_https'] == 0:
                reasons.append("[WARNING] Does not use HTTPS encryption, which is a security risk.")
            
            if features['special_char_ratio'] > 0.15:
                reasons.append("[WARNING] High number of special characters, which may indicate URL manipulation.")
            
            if features['is_known_legitimate'] == 0 and features['domain_length'] < 5:
                reasons.append("[WARNING] Domain name is very short and not from a known legitimate source.")
        else:  # Legitimate
            reasons.append(f"Detected as LEGITIMATE with {confidence:.1%} confidence.")
            
            if features['has_https'] == 1:
                reasons.append("[OK] Uses HTTPS encryption for secure communication.")
            
            if features['is_known_legitimate'] == 1:
                reasons.append("[OK] Domain is from a known legitimate source.")
            
            if features['suspicious_keyword_count'] == 0:
                reasons.append("[OK] No suspicious keywords detected.")
            
            if features['suspicious_tld'] == 0:
                reasons.append("[OK] Uses a standard, reputable top-level domain.")
        
        return reasons
    
    def _explain_message_result(self, features, prediction, confidence):
        """Generate explanations for message detection result"""
        reasons = []
        
        if prediction == 1:  # Fake
            reasons.append(f"Detected as FAKE with {confidence:.1%} confidence.")
            
            if features['has_suspicious_phrase'] == 1:
                reasons.append(f"[WARNING] Contains {features['suspicious_phrase_count']} suspicious phrase(s) like 'click here', 'act now', 'verify account'.")
            
            if features['has_urgency'] == 1:
                reasons.append(f"[WARNING] Uses urgency language ({features['urgency_word_count']} urgency words) to pressure quick action.")
            
            if features['has_financial_keywords'] == 1:
                reasons.append(f"[WARNING] Contains {features['financial_keyword_count']} financial-related keywords, common in payment scams.")
            
            if features['has_authority_keywords'] == 1:
                reasons.append(f"[WARNING] Mentions authority figures ({features['authority_keyword_count']} mentions), common in impersonation scams.")
            
            if features['url_count'] > 0:
                reasons.append(f"[WARNING] Contains {features['url_count']} URL(s) - be cautious of links in unsolicited messages.")
            
            if features['all_caps_ratio'] > 0.3:
                reasons.append("[WARNING] Excessive use of capital letters, a common spam/scam tactic.")
            
            if features['exclamation_count'] >= 3:
                reasons.append(f"[WARNING] Contains {features['exclamation_count']} exclamation marks, indicating aggressive/pushy language.")
            
            if features['suspicious_to_word_ratio'] > 0.1:
                reasons.append("[WARNING] High ratio of suspicious phrases to total words.")
            
            if features['max_word_repetition'] >= 3:
                reasons.append("[WARNING] Contains repeated words, a common spam pattern.")
        else:  # Legitimate
            reasons.append(f"Detected as LEGITIMATE with {confidence:.1%} confidence.")
            
            if features['has_suspicious_phrase'] == 0:
                reasons.append("[OK] No suspicious phrases detected.")
            
            if features['has_urgency'] == 0:
                reasons.append("[OK] No urgency language detected.")
            
            if features['url_count'] == 0:
                reasons.append("[OK] No embedded URLs detected.")
            
            if features['all_caps_ratio'] < 0.1:
                reasons.append("[OK] Normal capitalization pattern.")
        
        return reasons
    
    def _save_url_model(self):
        """Save URL model and scaler"""
        if self.url_model:
            with open(os.path.join(self.model_dir, 'url_model.pkl'), 'wb') as f:
                pickle.dump(self.url_model, f)
            with open(os.path.join(self.model_dir, 'url_scaler.pkl'), 'wb') as f:
                pickle.dump(self.url_scaler, f)
    
    def _save_message_model(self):
        """Save message model and scaler"""
        if self.message_model:
            with open(os.path.join(self.model_dir, 'message_model.pkl'), 'wb') as f:
                pickle.dump(self.message_model, f)
            with open(os.path.join(self.model_dir, 'message_scaler.pkl'), 'wb') as f:
                pickle.dump(self.message_scaler, f)
    
    def _load_url_model(self):
        """Load URL model and scaler"""
        model_path = os.path.join(self.model_dir, 'url_model.pkl')
        scaler_path = os.path.join(self.model_dir, 'url_scaler.pkl')
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            with open(model_path, 'rb') as f:
                self.url_model = pickle.load(f)
            with open(scaler_path, 'rb') as f:
                self.url_scaler = pickle.load(f)
    
    def _load_message_model(self):
        """Load message model and scaler"""
        model_path = os.path.join(self.model_dir, 'message_model.pkl')
        scaler_path = os.path.join(self.model_dir, 'message_scaler.pkl')
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            with open(model_path, 'rb') as f:
                self.message_model = pickle.load(f)
            with open(scaler_path, 'rb') as f:
                self.message_scaler = pickle.load(f)

