from telegram import Bot
from telegram.constants import ParseMode
from config import TELEGRAM_TOKEN

# Create Telegram Bot instance
bot = Bot(token=TELEGRAM_TOKEN)


async def send_alert(chat_id, message):
    """
    Send a Telegram message.
    """

    try:
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN
        )
        return True

    except Exception as e:
        print(f"[ALERT ERROR] {e}")
        return False


async def send_price_drop(chat_id, title, old_price, new_price):
    message = (
        "📉 *Price Dropped!*\n\n"
        f"*{title}*\n\n"
        f"💰 Old Price: ₹{old_price}\n"
        f"🔥 New Price: ₹{new_price}"
    )

    return await send_alert(chat_id, message)


async def send_price_increase(chat_id, title, old_price, new_price):
    message = (
        "📈 *Price Increased!*\n\n"
        f"*{title}*\n\n"
        f"💰 Old Price: ₹{old_price}\n"
        f"💵 New Price: ₹{new_price}"
    )

    return await send_alert(chat_id, message)


async def send_restock(chat_id, title):
    message = (
        "✅ *Back in Stock!*\n\n"
        f"*{title}*\n\n"
        "The product is available again."
    )

    return await send_alert(chat_id, message)


async def send_out_of_stock(chat_id, title):
    message = (
        "❌ *Out of Stock!*\n\n"
        f"*{title}*\n\n"
        "The product is currently unavailable."
    )

    return await send_alert(chat_id, message)
