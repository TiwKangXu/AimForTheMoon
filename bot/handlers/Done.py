from telegram import Update
from telegram.ext import ContextTypes
import logging
import datetime
from bot.firebase import task_ref

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
    done_items = [f"✔️ {entry['tasks'][i]}" for i in entry["done"] if i != 999]
    logging.info(f"/setgoals, tasks: {task_ref(user_id, today)["tasks"]}; done: {task_ref(user_id, today)["done"]}")
    await update.message.reply_text("📌 Tasks marked done:\n" + "\n".join(done_items))