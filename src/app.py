import requests
from flask import Flask, jsonify, request

import preprocess

app = Flask(__name__)




@app.route("/process", methods=["POST"])
def process_request():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Invalid input, 'prompt' is required"}), 400

    try:
        enriched_prompt = preprocess.add_template(data["prompt"])
    except Exception as e:
        return jsonify({"error": f"Error in prompt processing: {str(e)}"}), 500

    model_name = "llama3.1"
    outgoing_payload = {"model": model_name, "prompt": enriched_prompt, "stream": False}

    url = "http://localhost:11434/api/generate"
    try:
        response = requests.post(url=url, json=outgoing_payload)
    except requests.RequestException as e:
        return jsonify({"error": f"External service request failed: {str(e)}"}), 500

    if response.status_code != 200:
        return jsonify({"error": "Internal server error. Failed to get response from external service"}), response.status_code

    response_data = response.json()
    if "response" not in response_data:
        return jsonify({"error": "Internal server error. Missing 'response' field in external API response"}), 500

    return jsonify({"status": response_data["response"] == "69"})  # Update as per logic


if __name__ == "__main__":
    app.run(port=5000, debug=True)