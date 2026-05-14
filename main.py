import os
import requests
from smtplib import SMTP
from dotenv import load_dotenv

load_dotenv()

URL = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
SET_PRICE = 10000000
SMTP_GMAIL = os.environ.get("SMTP_ADDRESS")
GMAIL = os.environ.get("EMAIL_ADDRESS")
PASSWORD = os.environ.get("EMAIL_PASSWORD")
from bs4 import BeautifulSoup

header= {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=0, i",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
}
# header = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
#     "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
# }

response = requests.get(url=URL, headers=header)
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")
price_element = soup.find(class_="a-offscreen")
price=price_element.getText().split("D")[1]

title = soup.find(id="productTitle").getText()

if float(price.replace(",", "")) < SET_PRICE:
    with SMTP(SMTP_GMAIL, port=587) as connection:
        message = f"{title} \n is on sale for {price}"
        connection.starttls()
        connection.login(user=GMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=GMAIL,
            to_addrs=GMAIL,
            msg=f"Subject:Your product is on sale.\n\n{message}\n{URL}".encode("utf-8")
        )
