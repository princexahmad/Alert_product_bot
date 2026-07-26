from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import TELEGRAM_TOKEN
from tracker import parse_url
from scheduler import start_scheduler
from supabase_client import (
    save_product,
    get_products,
    remove_product,
)

# -----------------------
# /start
# -----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Welcome to Telegram Price Tracker Bot*\n\n"
        "Track Amazon & Flipkart products.\n\n"
        "Commands:\n"
        "/track <url>\n"
        "/list\n"
        "/remove <url>\n"
        "/status\n"
        "/help",
        parse_mode=ParseMode.MARKDOWN,
    )


# -----------------------
# /help
# -----------------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *Help*\n\n"
        "/track <product_url> - Track product\n"
        "/list - Show tracked products\n"
        "/remove <product_url> - Remove product\n"
        "/status - Bot status",
        parse_mode=ParseMode.MARKDOWN,
    )


# -----------------------
# /status
# -----------------------
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot is running.\n"
        "⏰ Automatic price checking is enabled."
    )


# -----------------------
# /track
# -----------------------
async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/track PRODUCT_URL"
        )
        return

    url = context.args[0]

    parsed = parse_url(url)

    if "error" in parsed:
        await update.message.reply_text(
            f"❌ {parsed['error']}"
        )
        return

    result = save_product(
        chat_id=update.effective_user.id,
        url=url,
        title=parsed["title"],
        price=parsed["price"],
        in_stock=parsed["in_stock"],
    )

    if not result["success"]:
        await update.message.reply_text(
            "⚠️ Product is already being tracked."
        )
        return

    await update.message.reply_text(
        "✅ *Tracking Started*\n\n"
        f"*{parsed['title']}*\n\n"
        f"💰 Price: ₹{parsed['price']}\n"
        f"📦 In Stock: {'Yes' if parsed['in_stock'] else 'No'}",
        parse_mode=ParseMode.MARKDOWN,
    )


# -----------------------
# /list
# -----------------------
async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE):

    products = get_products(update.effective_user.id)

    if not products.data:
        await update.message.reply_text(
            "📭 No tracked products."
        )
        return

    text = "*Tracked Products*\n\n"

    for i, product in enumerate(products.data, start=1):

        text += (
            f"{i}. {product['title']}\n"
            f"💰 ₹{product['price']}\n"
            f"📦 {'In Stock' if product['in_stock'] else 'Out of Stock'}\n\n"
        )

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
    )


# -----------------------
# /remove
# -----------------------
async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/remove PRODUCT_URL"
        )
        return

    url = context.args[0]

    remove_product(
        update.effective_user.id,
        url,
    )

    await update.message.reply_text(
        "🗑 Product removed successfully."
    )


# -----------------------
# Main
# -----------------------
def main():

    app = Application.builder().token(
        TELEGRAM_TOKEN
    ).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("track", track))
    app.add_handler(CommandHandler("list", list_products))
    app.add_handler(CommandHandler("remove", remove))
    app.add_handler(CommandHandler("status", status))

    start_scheduler()

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
