# AI Student Record Manager

A beginner-friendly Flask web application to manage student records, calculate results, and optionally generate academic feedback and study tips using Groq.

## Requirements
- Windows and Python 3
- VS Code
- Internet connection for package installation and AI features
- Groq API key for AI features (record management works without it)

## Run on Windows PowerShell
1. Open this folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:
   ```powershell
   python -m venv venv
   ```
4. Activate it:
   ```powershell
   venv\Scripts\Activate
   ```
   If PowerShell blocks activation, use Command Prompt in VS Code and run:
   ```cmd
   venv\Scripts\activate.bat
   ```
5. Install packages:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Optional: copy `.env.example` to `.env`, then put your Groq API key in `.env`.
7. Start the application:
   ```powershell
   python app.py
   ```
8. Open Chrome at http://127.0.0.1:5000

Keep the terminal open while using the app. Press **Ctrl+C** in the terminal to stop it.

## Grade rules
- A: 85% or above
- B: 70% to below 85%
- C: 60% to below 70%
- D: 50% to below 60%
- F: below 50%

Student records are saved in `students.json`. Back up this file regularly. Never upload `.env` or share your API key.
