from telegram import Update
from telegram.ext import ContextTypes
import logging

# Command: /start
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
        "Let's get productive! 🚀"
    )
    logging.info(f"/start by user {update.effective_user.id}")
    await update.message.reply_markdown(message)

# Command: /help — reuse /start message
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"/help by user {update.effective_user.id}")
    await start(update, context)
