import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os


# 1. Scrape the card price
def get_card_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Failed to fetch page."

    soup = BeautifulSoup(response.text, 'html.parser')

    # TODO: Update the CSS selector below to match your target site
    price_element = soup.select_one("CSS_SELECTOR_HERE")

    if price_element:
        return price_element.get_text(strip=True)
    else:
        return "Price not found"


# 2. Send the price as a text message
def send_price_text(price, recipient_sms_email, sender_email, sender_password):
    msg = EmailMessage()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg.set_content(f"{current_time} - Price: {price}")
    msg['From'] = sender_email
    msg['To'] = recipient_sms_email
    msg['Subject'] = ''  # SMS ignores subject

    try:
        with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print(f"[{current_time}] SMS sent successfully.")
    except Exception as e:
        print(f"[{current_time}] Failed to send SMS: {e}")


# 3. Configuration (fill in these values)
card_url = "https://your-price-site.com/item-page"  # TODO: Replace with actual URL
recipient_sms_email = "1234567890@carrier-sms-gateway.com"  # TODO: Replace with actual number and carrier domain
sender_email = os.environ.get("SENDER_EMAIL")  # Set this as an environment variable
sender_password = os.environ.get("SENDER_APP_PASSWORD")  # App-specific password (not your login password)

# 4. Run the process
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
price = get_card_price(card_url)

# Log to file
with open("price_log.txt", "a") as file:
    file.write(f"{current_time} - {price}\n")

print(f"[{current_time}] Logged price: {price}")

# Send SMS
if "not found" not in price.lower():
    send_price_text(price, recipient_sms_email, sender_email, sender_password)
else:
    print(f"[{current_time}] Price not found — SMS not sent.")
