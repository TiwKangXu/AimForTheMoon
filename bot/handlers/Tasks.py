from telegram import Update
from telegram.ext import ContextTypes
import logging
import datetime
from bot.firebase import task_ref

async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    today = str(datetime.date.today())
    entry = task_ref(user_id, today).get()
    
    if not entry:
        await update.message.reply_text("⚠️ You haven't set your tasks yet. Use /setgoals.")
        return
    tasks_text = ""
    done_list = entry.get("done", [])
    for i, task in enumerate(entry["tasks"]):
        prefix = "✔️" if i in done_list else "❌"
        tasks_text += f"{prefix} {i+1}. {task}\n"
    logging.info(f"/tasks, tasks: {entry["tasks"]}; done: {entry["done"]}")
    await update.message.reply_text(f"📋 Your tasks today:\n{tasks_text}")