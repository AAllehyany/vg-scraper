from selenium import webdriver
from selenium.webdriver.chrome import options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
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
ENDPOINT = 'https://s3.eu-central-1.wasabisys.com'

class Scraper:

    def __init__(__self, code, endpoint, settings, website):
        __self.code = code
        __self.endpoint = endpoint
        __self.settings = settings
        __self.website = website
        __self.deck = []

    
    def scrape_deck(__self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM,).install(), options=options)
        driver.set_window_size(1120, 500)
        page_link = f'{__self.website}/{__self.code}'
        print(page_link)
        driver.get(page_link)

        try:
            wait = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".deckview"))
            )

            cards = wait.find_elements_by_class_name("card-item")

            deck = []
            for card in cards:
                # WebDriverWait(driver, 30).until(
                #     EC.presence_of_element_located((By.CSS_SELECTOR, ".num"))
                # )

                img_tag = card.find_element_by_tag_name("img")
                wide = img_tag.find_element_by_xpath('..').get_attribute("class").find("wide-card") != -1
                img_link = img_tag.get_attribute("data-src")
                num = card.find_element_by_class_name("num").get_attribute("textContent")
                deck.append(CardEntry(img_link, num, wide))
            
            driver.quit()
            __self.deck = deck
        except TimeoutException:
            raise

    def upload_deck(__self):
        pdf = generate_pdf_proxy(__self.settings, __self.deck)
        output = pdf.output('file.pdf', 'S').encode('latin-1')
        
        client = boto3.client('s3', 
            endpoint_url = __self.endpoint,
            aws_access_key_id = accessKey,
            aws_secret_access_key = secretKey)
        
        client.put_object(
            Body=output,
            Bucket="deck-pdfs",
            ACL="public-read",
            Key=f"{__self.code}.pdf"
        )

        public_link = f"{__self.endpoint}/deck-pdfs/{__self.code}.pdf"

        return public_link