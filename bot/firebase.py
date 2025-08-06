from firebase_admin import db as fb_db
import datetime

def task_ref(user_id, date=None):
    if date is None:
        date = str(datetime.date.today())
    return fb_db.reference(f"tasks/{user_id}/{date}")

def get_today_tasks(user_id):
    return task_ref(user_id).get()

def save_tasks(user_id, name, tasks):
    ref = task_ref(user_id)
    ref.set({
        "username": name,
        "tasks": tasks,
        "done": [999]
    })

def update_done_tasks(user_id, done_list):
    task_ref(user_id).update({"done": done_list})

def get_user_task_stats(user_id):
    user_data = fb_db.reference(f"tasks/{user_id}").get() or {}
    total = len(user_data)
    full_days = sum(1 for r in user_data.values() if len(r.get("done", [])) >= 3)
    return total, full_days
