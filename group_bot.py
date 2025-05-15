
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re
import time

# === توکن رباتت رو اینجا بذار ===
BOT_TOKEN = "توکن_ربات_اینجا"

# ضد اسپم (فلود)
user_messages = {}

# خوش‌آمدگویی
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in update.message.new_chat_members:
        await update.message.reply_text(f"به گروه خوش اومدی، {user.first_name}!")

# ضد لینک
async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if re.search(r"https?://|t\.me|telegram\.me|@", update.message.text.lower()):
        await update.message.delete()

# فلود چک (بیش از حد پیام فرستادن)
async def flood_protection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    now = time.time()

    if user_id not in user_messages:
        user_messages[user_id] = []

    user_messages[user_id] = [t for t in user_messages[user_id] if now - t < 5]
    user_messages[user_id].append(now)

    if len(user_messages[user_id]) > 5:
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text(
            f"{update.message.from_user.first_name} به دلیل ارسال بیش از حد پیام، میوت شد.")

# بن کردن
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(update.message.chat_id, user.id)
        await update.message.reply_text(f"{user.first_name} بن شد.")

# آن‌بن
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.unban_chat_member(update.message.chat_id, user.id)
        await update.message.reply_text(f"{user.first_name} آزاد شد.")

# میوت
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.restrict_chat_member(
            chat_id=update.message.chat_id,
            user_id=user.id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text(f"{user.first_name} ساکت شد.")

# آن‌میوت
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.restrict_chat_member(
            chat_id=update.message.chat_id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await update.message.reply_text(f"{user.first_name} آزاد شد.")

# سنجاق کردن پیام
async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await context.bot.pin_chat_message(
            chat_id=update.message.chat_id,
            message_id=update.message.reply_to_message.message_id
        )
        await update.message.reply_text("پیام سنجاق شد.")

# اجرای ربات
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_link))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, flood_protection))

    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("pin", pin))

    print("ربات مدیریت گروه در حال اجراست...")
    app.run_polling()
