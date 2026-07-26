# 🛒 Telegram Price Tracker Bot

A production-ready Telegram bot that monitors Amazon and Flipkart product prices and sends instant Telegram alerts whenever a product price changes or comes back in stock.

---

# ✨ Features

- 📦 Track Amazon products
- 🛍️ Track Flipkart products
- 🔔 Instant Telegram notifications
- 📉 Price Drop Alerts
- 📈 Price Increase Alerts
- ✅ Restock Alerts
- ❌ Out of Stock Alerts
- 💾 Supabase Database
- 🔄 Automatic background checking every 15 minutes
- 🚀 Deploy on Render
- 🔒 Environment variable support
- 📝 Logging

---

# 📁 Project Structure

```
telegram-price-tracker-bot/

│── main.py
│── tracker.py
│── scheduler.py
│── alert.py
│── supabase_client.py
│── config.py
│── logger.py

│── requirements.txt
│── render.yaml
│── README.md
│── .env.example
│── .gitignore
```

---

# 🤖 Telegram Commands

### Start Bot

```
/start
```

### Help

```
/help
```

### Track Product

```
/track PRODUCT_URL
```

Example

```
/track https://www.amazon.in/dp/B0XXXXXXX
```

or

```
/track https://www.flipkart.com/....
```

---

### Show Tracked Products

```
/list
```

---

### Remove Product

```
/remove PRODUCT_URL
```

---

### Bot Status

```
/status
```

---

# ⚙️ Environment Variables

Create a file named

```
.env
```

Add

```env
TELEGRAM_TOKEN=YOUR_BOT_TOKEN

SUPABASE_URL=https://xxxxxxxx.supabase.co

SUPABASE_KEY=YOUR_SUPABASE_KEY
```

---

# 📦 Install

Clone repository

```bash
git clone https://github.com/yourusername/telegram-price-tracker-bot.git
```

Move into project

```bash
cd telegram-price-tracker-bot
```

Install packages

```bash
pip install -r requirements.txt
```

---

# ▶️ Run

```bash
python main.py
```

---

# 🚀 Deploy on Render

Build Command

```bash
pip install -r requirements.txt
```

Start Command

```bash
python main.py
```

---

# 🗄️ Database

Supabase Table

```
products
```

Columns

| Column | Type |
|----------|---------|
| id | uuid |
| chat_id | bigint |
| product_url | text |
| title | text |
| price | numeric |
| in_stock | boolean |
| created_at | timestamp |
| updated_at | timestamp |

---

# 🔔 Alert Types

✅ Price Drop

Example

```
Price dropped!

Old Price : ₹25,999

New Price : ₹23,999
```

---

✅ Price Increased

```
Price Increased

Old Price : ₹21,999

New Price : ₹22,499
```

---

✅ Back in Stock

```
Product is now available.
```

---

✅ Out of Stock

```
Product is currently unavailable.
```

---

# 📜 License

MIT License

---

# ❤️ Author

Made with ❤️ using Python, Telegram Bot API and Supabase.
