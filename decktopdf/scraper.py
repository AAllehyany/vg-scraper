from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from fpdf import FPDF
from .deck import CardEntry
from .proxy_generator import generate_pdf_proxy
import boto3
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

accessKey= os.environ.get("ACCESSKEY")
secretKey= os.environ.get("SECRETKEY")

CARD_W=59
CARD_H=86
PADDING_W = 10
PADDING_H = 10
MARGIN_W = 5
MARGIN_H = 5
ENDPOINT = 'https://s3.eu-central-1.wasabisys.com'

def scrape_deck_list(deck_code):
        
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 500)
    # driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    page_link = f'https://decklog.bushiroad.com/view/{deck_code}'
    driver.get(page_link)

    wait = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".deckview"))
    )

    cards = wait.find_elements_by_class_name("card-item")

    deck = []
    for card in cards:
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".num"))
        )

        img_tag = card.find_element_by_tag_name("img")
        wide = img_tag.find_element_by_xpath('..').get_attribute("class").find("wide-card") != -1
        img_link = img_tag.get_attribute("data-src")
        num = card.find_element_by_class_name("num").get_attribute("textContent")
        deck.append(CardEntry(img_link, num, wide))
    
    driver.quit()
    return deck

def scrape_and_upload(code, settings):
    deck = scrape_deck_list(code)
    pdf = generate_pdf_proxy(settings, deck)
    client = boto3.client('s3', 
        endpoint_url = ENDPOINT,
        aws_access_key_id = accessKey,
        aws_secret_access_key = secretKey)
    output = pdf.output('file.pdf', 'S').encode('latin-1')
    client.put_object(
        Body=output,
        Bucket="deck-pdfs",
        ACL="public-read",
        Key=f"{code}.pdf"
    )

    public_link = f"{ENDPOINT}/deck-pdfs/{code}.pdf"

    return public_link