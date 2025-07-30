from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from tinydb import TinyDB, Query
import firebase_admin
from firebase_admin import credentials, db as fb_db
import datetime
from keep_alive import keep_alive
import os
import json
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]  # e.g. https://your-app.onrender.com
PORT = int(os.environ.get("PORT", 8443))

# Firebase setup
firebase_cred_json = os.getenv("FIREBASE_CRED")
cred_dict = json.loads(firebase_cred_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://aimforthemoon-753bc-default-rtdb.asia-southeast1.firebasedatabase.app'
})

# Helper to get reference
def task_ref(user_id, date):
    return fb_db.reference(f"tasks/{user_id}/{date}")


# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "there"
    message = (
        "🎯 *Welcome to Daily Task Manager Bot!*\n\n"
        f"Hi {name}! I'm here to help you manage your daily tasks and boost your productivity.\n\n"
        "*Available Commands:*\n"
        "`/start` - Show this welcome message\n"
        "`/setgoals` - Set your daily tasks (e.g., /setgoals Task 1, Task 2, Task 3)\n"
        "`/done` - Mark a task as complete (e.g., /done 1)\n"
        "`/tasks` - View your current tasks\n"
        "`/stats` - View your progress statistics\n"
        "`/help` - Show detailed help\n\n"
        "*How to use:*\n"
        "1. Use /setgoals to add your daily tasks\n"
        "2. Use /done with task number to mark tasks complete\n"
        "3. Use /tasks to see your current task list\n"
        "4. Use /stats to track your progress\n\n"
        "Let's get productive! 🚀")
    await update.message.reply_markdown(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


async def setgoals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    name = update.effective_user.first_name
    today = str(datetime.date.today())
    tasks = " ".join(context.args).split(",")
    tasks = [t.strip() for t in tasks]

    if len(tasks) != 3:
        await update.message.reply_text("❗ Please enter exactly 3 tasks, separated by commas.")
        return

    task_ref(user_id, today).set({
        "username": name,
        "tasks": tasks,
        "done": []
    })

    await update.message.reply_text(
        f"✅ Got it, {name}! Your tasks for today are:\n"
        f"1. {tasks[0]}\n2. {tasks[1]}\n3. {tasks[2]}"
    )


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    today = str(datetime.date.today())
    ref = task_ref(user_id, today)
    entry = ref.get()

    if not entry:
        await update.message.reply_text("⚠️ You haven't set your goals today. Use /setgoals first.")
        return

    indexes = [int(i) - 1 for i in context.args if i.isdigit()]
    for i in indexes:
        if 0 <= i < 3 and i not in entry.get("done", []):
            entry["done"].append(i)

    ref.update({"done": entry["done"]})
    done_items = [f"✔️ {entry['tasks'][i]}" for i in entry["done"]]
    await update.message.reply_text("📌 Tasks marked done:\n" + "\n".join(done_items))


async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    today = str(datetime.date.today())
    entry = task_ref(user_id, today).get()

    if not entry:
        await update.message.reply_text("⚠️ You haven't set your tasks yet. Use /setgoals.")
        return

    tasks_text = ""
    for i, task in enumerate(entry["tasks"]):
        prefix = "✔️" if i in entry["done"] else "❌"
        tasks_text += f"{prefix} {i+1}. {task}\n"

    await update.message.reply_text(f"📋 Your tasks today:\n{tasks_text}")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_tasks = fb_db.reference(f"tasks/{user_id}").get() or {}

    total_days = len(user_tasks)
    full_days = sum(1 for r in user_tasks.values() if len(r.get("done", [])) == 3)

    await update.message.reply_text(
        f"📈 Your Productivity Stats:\n"
        f"Total days tracked: {total_days}\n"
        f"Days all tasks completed: {full_days}"
    )


# Main async entry
async def main():
    keep_alive()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("setgoals", setgoals))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("tasks", tasks))
    app.add_handler(CommandHandler("stats", stats))

    # Clean up any existing webhook
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.bot.set_webhook(WEBHOOK_URL)

    await app.start()
    await app.updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="",
        webhook_url=WEBHOOK_URL,
    )
    await app.updater.idle()

# Run async
if __name__ == "__main__":
    asyncio.run(main())
