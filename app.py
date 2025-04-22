from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

def generate_product_caption(user_input, max_tokens=500):
    prompt = f"Write a one liner caption for the : '{user_input}'"

    response = ollama.chat(
        model='mistral',
        messages=[
            {"role": "user", "content": prompt}
        ],
        options={
            "temperature": 1.5,
            "top_p": 0.9,
            "num_predict": max_tokens
        }
    )

    return response['message']['content'].strip()

@app.route('/generate-caption', methods=['POST'])
def generate_caption():
    data = request.get_json()
    user_input = data.get('product', '')
    if not user_input:
        return jsonify({'error': 'Product prompt is required'}), 400

    caption = generate_product_caption(user_input)
    return jsonify({'caption': caption})

if __name__ == '__main__':
    app.run(debug=True)
