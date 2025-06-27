def validate_all(clients_df, tasks_df, workers_df):
    errors = []

    # 1. Check for duplicate IDs
    if clients_df["ClientID"].duplicated().any():
        errors.append("Duplicate ClientID found.")
    if tasks_df["TaskID"].duplicated().any():
        errors.append("Duplicate TaskID found.")
    if workers_df["WorkerID"].duplicated().any():
        errors.append("Duplicate WorkerID found.")

    # 2. Check malformed JSON in AttributesJSON
    import json
    for idx, row in clients_df.iterrows():
        try:
            json.loads(row["AttributesJSON"])
        except Exception:
            errors.append(f"ClientID {row['ClientID']} has invalid AttributesJSON.")

    # 3. Check requested tasks exist
    task_ids = set(tasks_df["TaskID"])
    for idx, row in clients_df.iterrows():
        requested = str(row["RequestedTaskIDs"]).split(",")
        for t in requested:
            if t.strip() not in task_ids:
                errors.append(f"ClientID {row['ClientID']} requests missing TaskID {t.strip()}")

    # 4. Check RequiredSkills are present in workers
    all_worker_skills = set()
    for s in workers_df["Skills"]:
        all_worker_skills.update(tag.strip() for tag in str(s).split(","))

    for idx, row in tasks_df.iterrows():
        for skill in str(row["RequiredSkills"]).split(","):
            if skill.strip() not in all_worker_skills:
                errors.append(f"TaskID {row['TaskID']} requires unknown skill '{skill.strip()}'")

    return {
        "status": "success" if not errors else "fail",
        "errors": errors
    }
