from flask import Flask, request, jsonify
from main import get_similar_questions

app = Flask(__name__)

@app.route('/get_questions', methods=['POST'])
def get_questions():
    try:
        data = request.get_json()
        topic = data.get("topic", "").strip()
        num_of_questions = data.get("number_of_questions", 15)

        if not topic:
            return jsonify({"error": "يرجى إرسال الموضوع (topic)"}), 400

        try:
            num_of_questions = int(num_of_questions)
            if num_of_questions <= 0:
                raise ValueError
        except ValueError:
            return jsonify({"error": "number_of_questions يجب أن يكون عددًا صحيحًا موجبًا"}), 400

        result = get_similar_questions(topic, num_of_questions)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"حدث خطأ غير متوقع: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
