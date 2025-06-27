# Smart-Sheet
# SmartSheet

SmartSheet is a smart, AI-powered spreadsheet validator and rule engine designed to manage, validate, and correct CSV files such as clients, tasks, and workers.

## Features

- Upload and validate CSVs (clients, tasks, workers)
- AI-assisted rule builder using natural language
- Inline editing with validation
- Configure prioritization weights
- Download generated `rules.json` file

## Sample Data

Sample CSV files are located in the `/sample_data` folder:
- `clients.csv`
- `tasks.csv`
- `workers.csv`

## How to Run

1. Clone the repository:
git clone https://github.com/shaivalya/Smart-Sheet.git
cd Smart-Sheet

2. Install the required dependencies:
pip install -r requirements.txt


3. Start the Flask app:
python app.py

4. Open your browser and navigate to:

http://127.0.0.1:5000

## Folder Structure

SmartSheet/
├── app.py
├── validators.py
├── rules.py
├── requirements.txt
├── sample_data/
│ ├── clients.csv
│ ├── tasks.csv
│ └── workers.csv
├── static/
│ ├── style.css
│ ├── script.js
│ └── edit.js
├── templates/
│ ├── index.html
│ ├── edit.html
│ └── rules.html

## AI Enhancements

The application supports basic AI features like:
- Mapping incorrectly labeled or unordered CSV columns to expected formats
- Suggesting natural language rules for scheduling or coordination logic
- Making validation suggestions based on uploaded data

## Deployment

To deploy this project, you can use platforms like:
- Render.com
- PythonAnywhere
- Replit

## License

This project is open-source and available under the MIT License.

