import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN تنظیم نشده است. توکن ربات را در Variables هاست وارد کنید.")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")


def safe(value):
    """نمایش امن مقدارهای متنی در HTML."""
    if value is None or value == "":
        return "ندارد"
    return (str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


@bot.message_handler(commands=["start"])
def start(message):
    user = message.from_user

    # فقط اطلاعات عمومی حساب همان شخصی که به ربات پیام داده نمایش داده می‌شود.
    username = f"@{safe(user.username)}" if user.username else "ندارد"
    full_name = " ".join(
        part for part in [user.first_name, user.last_name] if part
    )

    details = (
        "👋 سلام! اطلاعات حساب تلگرام شما:\n\n"
        f"🆔 آیدی عددی: <code>{user.id}</code>\n"
        f"👤 نام: {safe(full_name)}\n"
        f"🔗 نام کاربری: {username}\n"
        f"🌐 زبان حساب: <code>{safe(user.language_code)}</code>\n"
        f"🤖 ربات هستید؟: {'بله' if user.is_bot else 'خیر'}\n\n"
        "برای دیدن دوباره این اطلاعات، دستور /start را بفرستید."
    )
    bot.reply_to(message, details)


@bot.message_handler(commands=["id"])
def show_id(message):
    bot.reply_to(
        message,
        f"🆔 آیدی عددی شما: <code>{message.from_user.id}</code>"
    )


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.reply_to(
        message,
        "دستورات ربات:\n"
        "/start - نمایش مشخصات حساب خودتان\n"
        "/id - نمایش آیدی عددی\n"
        "/help - راهنما"
    )


print("Bot is running...")
bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
