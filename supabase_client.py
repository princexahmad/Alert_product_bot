from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_product(chat_id, url, title, price, in_stock):
    """
    Save a new product if it is not already being tracked.
    """

    existing = (
        supabase.table("products")
        .select("id")
        .eq("chat_id", chat_id)
        .eq("product_url", url)
        .execute()
    )

    if existing.data:
        return {
            "success": False,
            "message": "Product is already being tracked."
        }

    result = (
        supabase.table("products")
        .insert({
            "chat_id": chat_id,
            "product_url": url,
            "title": title,
            "price": price,
            "in_stock": in_stock
        })
        .execute()
    )

    return {
        "success": True,
        "data": result.data
    }


def get_products(chat_id=None):
    """
    Get all tracked products.
    If chat_id is provided, return only that user's products.
    """

    query = supabase.table("products").select("*")

    if chat_id is not None:
        query = query.eq("chat_id", chat_id)

    return query.execute()


def update_product(chat_id, url, new_price, in_stock):
    """
    Update price and stock status.
    """

    return (
        supabase.table("products")
        .update({
            "price": new_price,
            "in_stock": in_stock
        })
        .eq("chat_id", chat_id)
        .eq("product_url", url)
        .execute()
    )


def remove_product(chat_id, url):
    """
    Remove a tracked product.
    """

    return (
        supabase.table("products")
        .delete()
        .eq("chat_id", chat_id)
        .eq("product_url", url)
        .execute()
    )


def get_product(chat_id, url):
    """
    Get a single tracked product.
    """

    return (
        supabase.table("products")
        .select("*")
        .eq("chat_id", chat_id)
        .eq("product_url", url)
        .limit(1)
        .execute()
    )


def delete_all_products(chat_id):
    """
    Delete all products for one user.
    """

    return (
        supabase.table("products")
        .delete()
        .eq("chat_id", chat_id)
        .execute()
    )
