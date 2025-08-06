from telegram import Update
from telegram.ext import ContextTypes
import logging
import datetime
from bot.firebase import task_ref

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
        "done": [999]
    })
    logging.info(f"/setgoals, tasks: {task_ref(user_id, today)["tasks"]}; done: {task_ref(user_id, today)["done"]}")
    await update.message.reply_text(f"✅ Got it, {name}! Your tasks for today are:\n1. {tasks[0]}\n2. {tasks[1]}\n3. {tasks[2]}")
