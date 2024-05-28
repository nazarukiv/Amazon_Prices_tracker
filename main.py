import requests
from bs4 import BeautifulSoup
import smtplib

URL = "https://www.amazon.co.uk/CP4523G-Ecoloop-Backpack-S-curve-shoulder/dp/B0B2PXNW6Z/ref=rtpb_d_sccl_2/260-9147946-2396465?pd_rd_w=ocWsu&content-id=amzn1.sym.e10cb4c9-d937-4af1-88fd-efef05dd01e1&pf_rd_p=e10cb4c9-d937-4af1-88fd-efef05dd01e1&pf_rd_r=T74XKKA6NGJ51Y0PDAGS&pd_rd_wg=5ryDa&pd_rd_r=6ecec5a1-9d1b-46d4-bf23-b5c6ca5e950b&pd_rd_i=B0B2PXNW6Z&psc=1"
headers = {
    "User-Agent": "-"
}

def check_price():
    # Send request to the URL
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get product title
    title = soup.find(id='productTitle').get_text().strip()

    # Get price details
    price_whole = soup.find('span', {'class': 'a-price-whole'}).get_text(strip=True)
    price_fraction = soup.find('span', {'class': 'a-price-fraction'}).get_text(strip=True)

    # Combine price parts and convert to float
    converted_price_not_float = f"{price_whole}{price_fraction}".replace(',', '')
    float_converted_price = float(converted_price_not_float)

    # Check if the price is higher than a threshold
    if float_converted_price > 25:
        send_email()

    print("Title:", title)
    print("Price:", float_converted_price)

def send_email():
    # Connect to the Gmail SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # Login to the email account
    email_address = 'your_email@gmail.com'
    email_password = 'your_password'
    server.login(email_address, email_password)

    # Email details
    subject = "Price fell down!"
    body = f"Check the amazon link: {URL}"
    msg = f"Subject: {subject}\n\n{body}"

    # Send the email
    server.sendmail(
        email_address,
        'recipient_email@example.com',
        msg
    )
    print("Email has been sent")
    server.quit()

check_price()
