import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
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

# Load dataset
data = pd.read_csv("../data/combined_dataset.csv")

# Extract features and labels
X = [extract_features(url) for url in data["url"]]
y = data["label"]

# Convert features to DataFrame
X = pd.DataFrame(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize numerical features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save the model and scaler
with open("../models/phishing_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("../models/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Model trained and saved!")