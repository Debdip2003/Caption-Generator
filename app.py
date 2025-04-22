from flask import Flask, render_template, request
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def generate_product_caption(user_input, max_tokens=500):
    prompt = f"Write a sophisticated and appealing e-commerce product caption based on: '{user_input}'"

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

@app.route('/generate_caption', methods=['POST'])
def generate_caption():
    data = request.get_json()  # Expecting JSON payload
    user_input = data.get('product')
    if not user_input:
        return {"error": "No product description provided."}, 400
    caption = generate_product_caption(user_input)
    return {"caption": caption}, 200


if __name__ == '__main__':
    app.run(debug=True)
