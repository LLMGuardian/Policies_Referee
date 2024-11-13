import pandas as pd
import requests
from flask import Flask, request, jsonify
import preprocess
import validators
import postprocess

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

dataset = pd.read_csv('mixed_data.csv')

app = Flask(__name__)

MODEL_API_URL = "http://localhost:11434/api/generate"

#Send the prompt to the model API
def send_to_llama_3_1(prompt):
    headers = {'Content-Type': 'application/json'}
    payload = {'prompt': prompt}
    
    response = requests.post(MODEL_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Model request failed"}

#Validate prompts from dataset
def validate_and_process_prompts(dataset):
    safe_prompts = []
    unsafe_prompts = []
    processed_prompts = []

    # Process each prompt
    for _, row in dataset.iterrows():
        prompt = row['prompt']
        if validators.validate_prompt(prompt) == 0:  # "safe"
            safe_prompts.append(prompt)
        else:
            unsafe_prompts.append(prompt)

    # Process safe prompts
    for prompt in safe_prompts:
        enriched_prompt = preprocess.add_template(prompt=prompt)
        outgoing_payload = {"model": "llama3.1", "prompt": enriched_prompt, "stream": False}
        
        response = requests.post(MODEL_API_URL, json=outgoing_payload)
        
        if response.status_code == 200:
            response_data = response.json()
            if "response" in response_data:
                response_text = response_data.get("response", "")
                result = postprocess.process_response(result=response_text)
                print(f"Processed response: {result}")
            else:
                print("Error: No 'response' field in model API response.")
        else:
            print(f"Error: Failed to get response from model. Status code: {response.status_code}")

@app.route('/process_prompt', methods=['POST'])
def process_prompt():
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    enriched_prompt = preprocess.add_template(prompt)
    
    is_malicious = validators.validate_prompt(enriched_prompt)
    
    if is_malicious == 0:
        #Send the safe prompt to LLaMA 3.1
        model_response = send_to_llama_3_1(enriched_prompt)
        return jsonify({"status": "safe", "response": model_response})
    else:
        #Block
        return jsonify({"status": "malicious", "response": "The prompt violates safety guidelines."})

@app.route('/evaluate', methods=['GET'])
def evaluate():
    dataset = pd.read_csv('mixed_data.csv')
    prompts = dataset['prompt']
    labels = dataset['target']
    
    predictions = []

    for prompt in prompts:
        enriched_prompt = preprocess.add_template(prompt)
        
        is_malicious = validators.validate_prompt(enriched_prompt)
        predictions.append(is_malicious)
    
    accuracy = accuracy_score(labels, predictions)
    
    evaluation_result = {
        "Accuracy": round(accuracy, 2)
    }

    return jsonify(evaluation_result)

@app.route('/process_dataset', methods=['GET'])
def process_dataset():
    dataset = pd.read_csv('mixed_data.csv')
    validate_and_process_prompts(dataset)

    return jsonify({"status": "processing completed"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
