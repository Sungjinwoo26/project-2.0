🚀 How to Run the Project
Step 1 — Open PowerShell / Terminal
Right-click anywhere in the project folder → "Open in Terminal" (or open PowerShell and navigate to the folder)

powershell
cd "d:\College\Sem 4\Mini project\project 2.0"
Step 2 — Activate the Virtual Environment
powershell
.\.venv\Scripts\activate
You'll see (.venv) appear at the start of the prompt — that means it's active.

Step 3 — Run the App
powershell
python app.py
Step 4 — Open in Browser
Once you see this in the terminal:

* Running on http://127.0.0.1:5000
Open your browser and go to: http://127.0.0.1:5000

Step 5 — Stop the Server (when done)
Press Ctrl + C in the terminal.

💡 One-time only: If you ever get a ModuleNotFoundError, run this once after activating the venv:

powershell
pip install -r requirements.txt