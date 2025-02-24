import pickle
import pandas as pd
from urllib.parse import urlparse
import tldextract
import requests

# Feature extraction function
def extract_features(url):
    features = {}
    parsed_url = urlparse(url)
    domain_info = tldextract.extract(url)

    # Domain-based features
    features["has_https"] = 1 if parsed_url.scheme == "https" else 0
    features["domain_length"] = len(domain_info.domain)
    features["num_subdomains"] = len(domain_info.subdomain.split(".")) if domain_info.subdomain else 0
    features["has_ip"] = 1 if any(part.isdigit() for part in domain_info.domain.split(".")) else 0

    # Content-based features
    try:
        response = requests.get(url, timeout=5)
        features["has_login_form"] = 1 if "login" in response.text.lower() else 0
    except:
        features["has_login_form"] = 0

    return features

# Prediction function
def predict_phishing(url):
    # Load the model and scaler
    with open("../models/phishing_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("../models/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    # Extract features and predict
    features = extract_features(url)
    features_df = pd.DataFrame([features])
    features_scaled = scaler.transform(features_df)
    prediction = model.predict(features_scaled)
    return "Phishing" if prediction[0] else "Legitimate"

# Test the function
if __name__ == "__main__":
    url = input("Enter a URL to check: ")
    print(f"URL: {url}")
    print(f"Prediction: {predict_phishing(url)}")