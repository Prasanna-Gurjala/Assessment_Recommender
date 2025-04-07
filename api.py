from flask import Flask, request, jsonify
from recommender import recommend_assessments

app = Flask(__name__)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    results = recommend_assessments(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

