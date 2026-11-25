import json

from flask import Flask, jsonify

app = Flask(__name__)


# no real api was given in the question so this just serves students.json
@app.route("/api/students")
def get_students():
    with open("students.json") as f:
        students = json.load(f)
    return jsonify(students)


if __name__ == "__main__":
    app.run(port=8000)
