from flask import Flask, request, jsonify
from main import get_similar_questions

app = Flask(__name__)

@app.route('/get_questions', methods=['POST'])
def get_questions():
    data = request.get_json()
    topic = data.get("topic")
    num_of_questions = data.get("number_of_questions")
    if not topic:
        return jsonify({"error": "يرجى إرسال الموضوع (topic)"}), 400

    result = get_similar_questions(topic,num_of_questions)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
