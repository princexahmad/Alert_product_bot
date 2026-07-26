import re
import requests
from bs4 import BeautifulSoup
from config import REQUEST_TIMEOUT

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9"
}


def clean_price(price_text):
    """
    Convert ₹12,999.00 -> 12999.00
    """
    if not price_text:
        return None

    cleaned = re.sub(r"[^\d.]", "", price_text)

    try:
        return float(cleaned)
    except ValueError:
        return None


def get_text(soup, selectors):
    """
    Try multiple selectors and return first non-empty text.
    """
    for selector in selectors:
        tag = soup.select_one(selector)
        if tag:
            text = tag.get_text(strip=True)
            if text:
                return text

    return None


def parse_amazon(soup):
    title = get_text(soup, [
        "#productTitle"
    ])

    price = get_text(soup, [
        ".a-price-whole",
        ".a-offscreen",
        "#priceblock_ourprice",
        "#priceblock_dealprice"
    ])

    availability = get_text(soup, [
        "#availability",
        "#availability span"
    ])

    return {
        "title": title or "Unknown Product",
        "price": clean_price(price),
        "in_stock": (
            availability is not None
            and "out of stock" not in availability.lower()
        )
    }


def parse_flipkart(soup):
    title = get_text(soup, [
        "span.VU-ZEz",
        "span.B_NuCI"
    ])

    price = get_text(soup, [
        "div.Nx9bqj",
        "div._30jeq3"
    ])

    return {
        "title": title or "Unknown Product",
        "price": clean_price(price),
        "in_stock": price is not None
    }


def parse_url(url):
    """
    Parse Amazon or Flipkart product page.
    """

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        if "amazon." in url:
            return parse_amazon(soup)

        elif "flipkart." in url:
            return parse_flipkart(soup)

        else:
            return {
                "error": "Only Amazon and Flipkart URLs are supported."
            }

    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out."
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {e}"
        }
