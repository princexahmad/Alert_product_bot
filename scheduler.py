import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import CHECK_INTERVAL
from tracker import parse_url
from supabase_client import (
    get_products,
    update_product,
)
from alert import (
    send_price_drop,
    send_price_increase,
    send_restock,
    send_out_of_stock,
)


async def check_products():
    """
    Check all tracked products for price or stock changes.
    """

    print("Checking tracked products...")

    try:
        result = get_products()

        if not result.data:
            print("No products found.")
            return

        for product in result.data:

            parsed = parse_url(product["product_url"])

            if "error" in parsed:
                print(f"Skipped: {parsed['error']}")
                continue

            old_price = product["price"]
            new_price = parsed["price"]

            old_stock = product["in_stock"]
            new_stock = parsed["in_stock"]

            chat_id = product["chat_id"]
            title = parsed["title"]

            # Price Drop
            if (
                new_price is not None
                and old_price is not None
                and new_price < old_price
            ):
                await send_price_drop(
                    chat_id,
                    title,
                    old_price,
                    new_price,
                )

            # Price Increase
            elif (
                new_price is not None
                and old_price is not None
                and new_price > old_price
            ):
                await send_price_increase(
                    chat_id,
                    title,
                    old_price,
                    new_price,
                )

            # Restock
            if (not old_stock) and new_stock:
                await send_restock(chat_id, title)

            # Out of Stock
            elif old_stock and (not new_stock):
                await send_out_of_stock(chat_id, title)

            # Update database
            update_product(
                chat_id,
                product["product_url"],
                new_price,
                new_stock,
            )

        print("Check completed.")

    except Exception as e:
        print(f"[Scheduler Error] {e}")


def start_scheduler():
    """
    Start APScheduler.
    """

    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        lambda: asyncio.create_task(check_products()),
        trigger="interval",
        minutes=CHECK_INTERVAL,
        id="price_checker",
        replace_existing=True,
    )

    scheduler.start()

    print(
        f"Scheduler started. Checking every {CHECK_INTERVAL} minutes."
    )

    return scheduler
