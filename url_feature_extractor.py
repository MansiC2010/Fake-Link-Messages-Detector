"""
URL Feature Extractor
Extracts various features from URLs to detect fake/malicious links
"""

import re
from urllib.parse import urlparse
import ipaddress
import math


class URLFeatureExtractor:
    """Extracts features from URLs for fake link detection"""
    
    def __init__(self):
        # Suspicious keywords in URLs
        self.suspicious_keywords = [
            'bit.ly', 'tinyurl', 't.co', 'goo.gl', 'ow.ly', 'short.link',
            'click', 'verify', 'update', 'secure', 'account', 'suspended',
            'urgent', 'confirm', 'validate', 'login', 'password', 'bank',
            'paypal', 'amazon', 'ebay', 'microsoft', 'apple', 'facebook'
        ]
        
        # Suspicious TLDs
        self.suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz']
        
        # Common legitimate domains
        self.legitimate_domains = [
            'google.com', 'meet.google.com', 'docs.google.com', 'drive.google.com',
            'gmail.com', 'mail.google.com', 'calendar.google.com', 'maps.google.com',
            'facebook.com', 'amazon.com', 'microsoft.com',
            'apple.com', 'github.com', 'stackoverflow.com', 'wikipedia.org',
            'youtube.com', 'twitter.com', 'linkedin.com', 'instagram.com',
            'chatgpt.com', 'openai.com', 'reddit.com', 'netflix.com',
            'spotify.com', 'paypal.com', 'ebay.com', 'wikipedia.org',
            'medium.com', 'quora.com', 'tumblr.com', 'pinterest.com',
            'snapchat.com', 'whatsapp.com', 'telegram.org', 'discord.com',
            'zoom.us', 'slack.com', 'dropbox.com', 'onedrive.com'
        ]
    
    def extract_features(self, url):
        """
        Extract comprehensive features from a URL
        
        Returns:
            dict: Dictionary of features
        """
        if not url or not isinstance(url, str):
            return self._get_default_features()
        
        # Check for malformed URL patterns (like http/domain.com instead of http://domain.com)
        if re.match(r'^https?/[^/]', url):
            # URL has http/ or https/ instead of http:// or https://
            return self._get_default_features()
        
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            parsed = urlparse(url)
            # Validate that the parsed URL has a proper netloc (domain)
            if not parsed.netloc or not parsed.scheme:
                return self._get_default_features()
        except Exception:
            return self._get_default_features()
        
        features = {}
        
        # Basic URL features
        features['url_length'] = len(url)
        features['domain_length'] = len(parsed.netloc) if parsed.netloc else 0
        features['path_length'] = len(parsed.path) if parsed.path else 0
        features['query_length'] = len(parsed.query) if parsed.query else 0
        
        # Protocol features
        features['has_https'] = 1 if parsed.scheme == 'https' else 0
        features['has_http'] = 1 if parsed.scheme == 'http' else 0
        
        # Domain features
        domain = parsed.netloc.lower() if parsed.netloc else ''
        features['subdomain_count'] = domain.count('.')
        features['has_ip'] = self._is_ip_address(domain)
        features['has_port'] = 1 if ':' in domain else 0
        
        # TLD features
        tld = self._extract_tld(domain)
        features['tld_length'] = len(tld)
        features['suspicious_tld'] = 1 if any(tld.endswith(stld) for stld in self.suspicious_tlds) else 0
        
        # Suspicious keyword features
        url_lower = url.lower()
        features['suspicious_keyword_count'] = sum(1 for keyword in self.suspicious_keywords if keyword in url_lower)
        features['has_click'] = 1 if 'click' in url_lower else 0
        features['has_verify'] = 1 if 'verify' in url_lower else 0
        features['has_update'] = 1 if 'update' in url_lower else 0
        features['has_account'] = 1 if 'account' in url_lower else 0
        features['has_login'] = 1 if 'login' in url_lower else 0
        
        # URL structure features
        features['special_char_count'] = sum(1 for c in url if c in '!@#$%^&*()_+-=[]{}|;:,.<>?')
        features['digit_count'] = sum(1 for c in url if c.isdigit())
        features['letter_count'] = sum(1 for c in url if c.isalpha())
        features['hyphen_count'] = url.count('-')
        features['underscore_count'] = url.count('_')
        features['dot_count'] = url.count('.')
        features['slash_count'] = url.count('/')
        features['equal_count'] = url.count('=')
        features['question_mark_count'] = url.count('?')
        features['ampersand_count'] = url.count('&')
        
        # Entropy (randomness measure - higher entropy might indicate random/obfuscated URLs)
        features['url_entropy'] = self._calculate_entropy(url)
        features['domain_entropy'] = self._calculate_entropy(domain)
        
        # Ratio features
        if len(url) > 0:
            features['digit_ratio'] = features['digit_count'] / len(url)
            features['letter_ratio'] = features['letter_count'] / len(url)
            features['special_char_ratio'] = features['special_char_count'] / len(url)
        else:
            features['digit_ratio'] = 0
            features['letter_ratio'] = 0
            features['special_char_ratio'] = 0
        
        # Short URL detection (only check actual short URL services, not paths)
        short_url_services = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly', 'short.link', 'tiny.cc']
        features['is_short_url'] = 1 if any(short in domain for short in short_url_services) else 0
        
        # Path depth
        features['path_depth'] = parsed.path.count('/') - 1 if parsed.path else 0
        
        # Query parameters count
        features['query_param_count'] = len(parsed.query.split('&')) if parsed.query else 0
        
        # Domain legitimacy check - check if domain matches or is a subdomain of legitimate domains
        features['is_known_legitimate'] = 0
        for leg_domain in self.legitimate_domains:
            if domain == leg_domain or domain.endswith('.' + leg_domain):
                features['is_known_legitimate'] = 1
                break
        
        return features
    
    def _is_ip_address(self, domain):
        """Check if domain is an IP address"""
        try:
            ipaddress.ip_address(domain.split(':')[0])
            return 1
        except (ValueError, AttributeError):
            return 0
    
    def _extract_tld(self, domain):
        """Extract top-level domain"""
        parts = domain.split('.')
        if len(parts) >= 2:
            return '.' + parts[-1]
        return ''
    
    def _calculate_entropy(self, string):
        """Calculate Shannon entropy of a string"""
        if not string:
            return 0
        
        prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
        entropy = -sum([p * math.log2(p) for p in prob if p > 0])
        return entropy
    
    def _get_default_features(self):
        """Return default feature values for invalid URLs"""
        return {
            'url_length': 0, 'domain_length': 0, 'path_length': 0, 'query_length': 0,
            'has_https': 0, 'has_http': 0, 'subdomain_count': 0, 'has_ip': 0,
            'has_port': 0, 'tld_length': 0, 'suspicious_tld': 1, 'suspicious_keyword_count': 5,
            'has_click': 1, 'has_verify': 1, 'has_update': 1, 'has_account': 1,
            'has_login': 1, 'special_char_count': 10, 'digit_count': 0, 'letter_count': 0,
            'hyphen_count': 0, 'underscore_count': 0, 'dot_count': 0, 'slash_count': 0,
            'equal_count': 0, 'question_mark_count': 0, 'ampersand_count': 0,
            'url_entropy': 6.0, 'domain_entropy': 6.0, 'digit_ratio': 0.5, 'letter_ratio': 0,
            'special_char_ratio': 0.5, 'is_short_url': 0, 'path_depth': 0,
            'query_param_count': 0, 'is_known_legitimate': 0
        }
    
    def get_feature_names(self):
        """Get list of all feature names"""
        return list(self._get_default_features().keys())

