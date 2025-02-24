import unittest
from src.predict import predict_phishing

class TestPredict(unittest.TestCase):
    def test_phishing_url(self):
        url = "http://fake-login-page.com"
        prediction = predict_phishing(url)
        self.assertEqual(prediction, "Phishing")

    def test_legitimate_url(self):
        url = "https://www.google.com"
        prediction = predict_phishing(url)
        self.assertEqual(prediction, "Legitimate")

if __name__ == "__main__":
    unittest.main()