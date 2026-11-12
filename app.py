import json
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from ai_helper import analyze_performance, generate_study_tips

load_dotenv()
app = Flask(__name__)
DATA_FILE = Path(__file__).with_name("students.json")


def load_students():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_students(students):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


def calculate_result(marks):
    total = sum(marks)
    average = total / len(marks) if marks else 0
    if average >= 85:
        grade = "A"
    elif average >= 70:
        grade = "B"
    elif average >= 60:
        grade = "C"
    elif average >= 50:
        grade = "D"
    else:
        grade = "F"
    return total, round(average, 2), grade


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify(load_students())


@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}
    student_id = str(data.get("student_id", "")).strip()
    name = str(data.get("name", "")).strip()
    class_name = str(data.get("class_name", "")).strip()
    subjects = [s.strip() for s in str(data.get("subjects", "")).split(",") if s.strip()]
    raw_marks = [m.strip() for m in str(data.get("marks", "")).split(",") if m.strip()]

    if not student_id or not name or not class_name:
        return jsonify({"error": "Please enter Student ID, Student Name and Class / Semester."}), 400
    if not subjects or len(subjects) != len(raw_marks):
        return jsonify({"error": "Enter matching subject names and marks, separated by commas."}), 400
    try:
        marks = [float(value) for value in raw_marks]
    except ValueError:
        return jsonify({"error": "Marks must be numbers."}), 400
    if any(mark < 0 or mark > 100 for mark in marks):
        return jsonify({"error": "Each mark must be between 0 and 100."}), 400

    students = load_students()
    if any(student["student_id"] == student_id for student in students):
        return jsonify({"error": "That Student ID already exists."}), 400

    total, average, grade = calculate_result(marks)
    student = {
        "student_id": student_id, "name": name, "class_name": class_name,
        "subjects": subjects, "marks": marks, "total": total,
        "average": average, "grade": grade
    }
    students.append(student)
    save_students(students)
    return jsonify(student), 201


@app.route("/api/students/<student_id>", methods=["PUT", "DELETE"])
def change_student(student_id):
    students = load_students()
    index = next((i for i, s in enumerate(students) if s["student_id"] == student_id), None)
    if index is None:
        return jsonify({"error": "Student not found."}), 404

    if request.method == "DELETE":
        students.pop(index)
        save_students(students)
        return jsonify({"message": "Student deleted."})

    data = request.get_json(silent=True) or {}
    subjects = [s.strip() for s in str(data.get("subjects", "")).split(",") if s.strip()]
    raw_marks = [m.strip() for m in str(data.get("marks", "")).split(",") if m.strip()]
    name = str(data.get("name", "")).strip()
    class_name = str(data.get("class_name", "")).strip()
    if not name or not class_name or not subjects or len(subjects) != len(raw_marks):
        return jsonify({"error": "Enter name, class, and matching subjects and marks."}), 400
    try:
        marks = [float(value) for value in raw_marks]
    except ValueError:
        return jsonify({"error": "Marks must be numbers."}), 400
    if any(mark < 0 or mark > 100 for mark in marks):
        return jsonify({"error": "Each mark must be between 0 and 100."}), 400
    total, average, grade = calculate_result(marks)
    students[index] = {
        "student_id": student_id, "name": name, "class_name": class_name,
        "subjects": subjects, "marks": marks, "total": total,
        "average": average, "grade": grade
    }
    save_students(students)
    return jsonify(students[index])


@app.route("/api/ai/<action>", methods=["POST"])
def ai_action(action):
    data = request.get_json(silent=True) or {}
    student = data.get("student")
    if not student:
        return jsonify({"error": "Select a student first."}), 400
    if action == "analyze":
        result = analyze_performance(student)
    elif action == "tips":
        result = generate_study_tips(student)
    else:
        return jsonify({"error": "Unknown AI action."}), 404
    return jsonify({"result": result})


if __name__ == "__main__":
    print("AI Student Record Manager is running!")
    print("Open this link in Chrome: http://127.0.0.1:5000")
    print("(Press Ctrl+C in this terminal to stop the app)")
    app.run(host="127.0.0.1", port=5000, debug=False)
