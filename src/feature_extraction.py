import tldextract
import requests
from urllib.parse import urlparse

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