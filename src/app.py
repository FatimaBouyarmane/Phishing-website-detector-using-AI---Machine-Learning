from flask import Flask, request, jsonify
from predict import predict_phishing

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Phishing Website Detector API is running!"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"error": "Missing 'url' field"}), 400
        
        url = data["url"]
        prediction = predict_phishing(url)
        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
