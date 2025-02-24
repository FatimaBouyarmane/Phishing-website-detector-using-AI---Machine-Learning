import unittest
from src.feature_extraction import extract_features

class TestFeatureExtraction(unittest.TestCase):
    def test_phishing_url(self):
        url = "http://fake-login-page.com"
        features = extract_features(url)
        self.assertEqual(features["has_https"], 0)
        self.assertEqual(features["has_ip"], 0)

    def test_legitimate_url(self):
        url = "https://www.google.com"
        features = extract_features(url)
        self.assertEqual(features["has_https"], 1)
        self.assertEqual(features["has_ip"], 0)

if __name__ == "__main__":
    unittest.main()