import tkinter as tk
from tkinter import ttk, messagebox
import pickle
import pandas as pd
from urllib.parse import urlparse
import tldextract
import requests

# Load the model and scaler
def load_model():
    try:
        with open("../models/phishing_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("../models/scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        return model, scaler
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load model: {str(e)}")
        return None, None

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

# Function to handle the "Check URL" button click
def check_url():
    url = url_entry.get().strip()  # Remove spaces
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL!")
        return

    try:
        # Extract features
        features = extract_features(url)
        features_df = pd.DataFrame([features])

        # Scale features and make prediction
        features_scaled = scaler.transform(features_df)
        prediction = model.predict(features_scaled)[0]

        # Update result label
        if prediction == 1:
            result_label.config(text="Phishing ❌", foreground="#ff4444")  # Red
        else:
            result_label.config(text="Legitimate ✅", foreground="#00C851")  # Green
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to clear the input field and reset label
def clear_fields():
    url_entry.delete(0, tk.END)
    result_label.config(text="Waiting for input...", foreground="#AAAAAA")  # Gray

# Load the model and scaler
model, scaler = load_model()
if model is None or scaler is None:
    exit()

# Create the main application window
app = tk.Tk()
app.title("Phishing Website Detector")
app.geometry("600x400")  # Window size
app.configure(bg="#1e1e1e")  # Dark background

# Apply techy theme
style = ttk.Style()
style.theme_use("clam")  # Use a modern theme

# Configure colors and fonts
style.configure("TFrame", background="#2d2d2d")
style.configure("TLabel", background="#2d2d2d", foreground="#ffffff", font=("Consolas", 12))
style.configure("TButton", background="#444444", foreground="#ffffff", font=("Consolas", 12), padding=10)
style.configure("TEntry", fieldbackground="#444444", foreground="#ffffff", font=("Consolas", 12), padding=5)

# Header Label
header_label = ttk.Label(app, text="🔍 Phishing Website Detector", font=("Consolas", 20, "bold"), background="#1e1e1e", foreground="#00ffcc")
header_label.pack(pady=20)

# Frame to hold input and buttons
frame = ttk.Frame(app, padding=20, relief="groove")
frame.pack(expand=True)

# Input Field
url_label = ttk.Label(frame, text="Enter a URL:", font=("Consolas", 14, "bold"))
url_label.pack(pady=10)
url_entry = ttk.Entry(frame, width=50)
url_entry.pack(pady=10, ipady=5)

# Buttons
button_frame = ttk.Frame(frame)
button_frame.pack(pady=20)

check_button = ttk.Button(button_frame, text="Check URL", command=check_url, style="TButton")
check_button.grid(row=0, column=0, padx=10)

clear_button = ttk.Button(button_frame, text="Clear", command=clear_fields, style="TButton")
clear_button.grid(row=0, column=1, padx=10)

# Result Label
result_label = ttk.Label(frame, text="Waiting for input...", foreground="#AAAAAA", font=("Consolas", 14, "bold"))
result_label.pack(pady=20)

# Run the application
app.mainloop()