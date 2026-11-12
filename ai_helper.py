import os


def ask_groq(prompt):
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return "AI is not configured. Add your Groq API key in the .env file to use AI features."

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        model = os.getenv("GROQ_MODEL", "").strip() or "llama-3.3-70b-versatile"
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as error:
        return (
            "The AI service could not complete the request. Check your internet connection, "
            "Groq API key and model setting. Details: " + str(error)
        )


def student_summary(student):
    return (
        f"Name: {student.get('name')}; Class: {student.get('class_name')}; "
        f"Subjects: {student.get('subjects')}; Marks: {student.get('marks')}; "
        f"Average: {student.get('average')}%; Grade: {student.get('grade')}."
    )


def analyze_performance(student):
    prompt = (
        "You are a helpful academic assistant. Give supportive, practical feedback. "
        "Identify strong subjects, subjects needing improvement, and 3 specific suggestions. "
        "Do not shame the student. Student record: " + student_summary(student)
    )
    return ask_groq(prompt)


def generate_study_tips(student):
    prompt = (
        "Create a simple, realistic weekly study plan and practical study tips based on this record. "
        "Use clear headings and short bullet points. Student record: " + student_summary(student)
    )
    return ask_groq(prompt)
