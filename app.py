from flask import Flask, render_template, request ,  jsonify ,send_file , redirect
import pandas as pd
from validators import validate_all
from rules import save_rules, load_rules

app = Flask(__name__)

clients_df = tasks_df = workers_df = None  # Global cache

#@app.route("/", methods=["GET"])
#def index():
  #  return render_template("index.html", clients=None, tasks=None, workers=None, query_results=None)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # No CSV data sent here


@app.route("/upload", methods=["POST"])
def upload():
    global clients_df, tasks_df, workers_df

    try:
        files = request.files
        clients_df = pd.read_csv(files["clients"])
        tasks_df = pd.read_csv(files["tasks"])
        workers_df = pd.read_csv(files["workers"])

        result = validate_all(clients_df, tasks_df, workers_df)

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "errors": [str(e)]})

@app.route("/query", methods=["POST"])
def query():
    global clients_df, tasks_df, workers_df

    if clients_df is None:
        return render_template("index.html", clients=None, tasks=None, workers=None, query_results=["Please upload CSVs first."])

    query_text = request.form["query"].lower()
    results = []

    if "high priority" in query_text:
        high_priority = clients_df[clients_df["PriorityLevel"] <= 2]
        results = high_priority["ClientName"].tolist()

    elif "t17" in query_text:
        filtered = clients_df[clients_df["RequestedTaskIDs"].str.contains("T17", na=False)]
        results = filtered["ClientName"].tolist()
    elif "unassigned tasks" in query_text:
         assigned_task_ids = pd.Series(clients_df["RequestedTaskIDs"].dropna()).str.split(",").explode().str.strip()
         unassigned = tasks_df[~tasks_df["TaskID"].isin(assigned_task_ids)]
         results = unassigned["TaskName"].tolist()


    else:
        results = ["❓ No match found for your query. Try: 'high priority clients' or 'clients with T17'"]

    return render_template("index.html",
                           clients=clients_df.to_dict(orient="records"),
                           tasks=tasks_df.to_dict(orient="records"),
                           workers=workers_df.to_dict(orient="records"),
                           query_results=results)
from flask import send_file
import io

@app.route("/download/<string:filetype>")
def download(filetype):
    global clients_df, tasks_df, workers_df

    dfs = {
        "clients": clients_df,
        "tasks": tasks_df,
        "workers": workers_df
    }

    if filetype not in dfs or dfs[filetype] is None:
        return "File not available", 400

    buffer = io.StringIO()
    dfs[filetype].to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(io.BytesIO(buffer.getvalue().encode()), mimetype="text/csv", as_attachment=True, download_name=f"{filetype}_cleaned.csv")
@app.route("/download/json")
def download_json():
    import json
    result = {
        "clients": clients_df.to_dict(orient="records"),
        "tasks": tasks_df.to_dict(orient="records"),
        "workers": workers_df.to_dict(orient="records")
    }
    return jsonify(result)
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    global clients_df, tasks_df, workers_df

    tables = {
        "Clients": clients_df.to_dict(orient="records") if clients_df is not None else [],
        "Tasks": tasks_df.to_dict(orient="records") if tasks_df is not None else [],
        "Workers": workers_df.to_dict(orient="records") if workers_df is not None else []
    }
    return render_template("edit.html", tables=tables)


@app.route("/save_edits", methods=["POST"])
def save_edits():
    global clients_df, tasks_df, workers_df

    data = request.get_json()

    try:
        # Convert lists of dicts back to DataFrames
        clients_df = pd.DataFrame(data.get("clients", []))
        tasks_df = pd.DataFrame(data.get("tasks", []))
        workers_df = pd.DataFrame(data.get("workers", []))

        return jsonify({"status": "success", "message": "✅ Changes saved successfully!"})
    except Exception as e:
        return jsonify({"status": "fail", "message": f"❌ Failed to save: {str(e)}"})
    
@app.route('/rules', methods=['GET'])
def show_rules_ui():
    return render_template('rules.html')

@app.route('/save_rules', methods=['POST'])
def save_rules_api():
    data = request.get_json()
    rules = data.get('rules', [])
    weights = data.get('weights', {})
    save_rules(rules, weights)
    return jsonify({"status": "success"})

@app.route('/download/rules', methods=['GET'])
def download_rules():
    return send_file("rules.json", as_attachment=True)
import json

@app.route('/load_rules')
def load_rules():
    try:
        with open('rules.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"rules": []})
@app.route("/save_rules", methods=["POST"])
def save_rules():
    rules = request.json.get("rules", [])
    with open("rules.json", "w") as f:
        json.dump({"rules": rules}, f, indent=2)
    return jsonify({"status": "success"})

import re

@app.route("/nl_to_rule", methods=["POST"])
def nl_to_rule():
    text = request.json.get("text", "").lower()

    # Simple match for co-run rule
    match = re.findall(r'tasks?\s+(t\d+)\s+(?:and|,)\s+(t\d+)', text)
    if match:
        task1, task2 = match[0]
        return jsonify({"rule": {"type": "coRun", "tasks": [task1.upper(), task2.upper()]}})
    
    return jsonify({})
@app.route("/")
def home():
    return redirect("/rules")


import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)
