from telegram import Update
from telegram.ext import ContextTypes
import logging
from bot.firebase import task_ref

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_tasks = task_ref.get() or {}
    total_days = len(user_tasks)
    full_days = sum(1 for r in user_tasks.values() if len(r.get("done", [])) >= 3)
    logging.info(f"/stats")
    await update.message.reply_text(f"📈 Your Productivity Stats:\nTotal days tracked: {total_days}\nDays all tasks completed: {full_days}")
