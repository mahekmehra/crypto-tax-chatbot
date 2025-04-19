from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    payload = {'sender': 'user', 'message': user_message}
    response = requests.post(RASA_URL, json=payload)
    rasa_response = response.json()
    bot_message = rasa_response[0]['text'] if rasa_response else "Sorry, I didn’t understand that."
    return jsonify({'message': bot_message})

if __name__ == '__main__':
    app.run(debug=True)