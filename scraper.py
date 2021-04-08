from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import requests
from fpdf import FPDF
from deck import CardEntry
from proxy_generator import generate_pdf_proxy

CARD_W=59
CARD_H=86
PADDING_W = 10
PADDING_H = 10
MARGIN_W = 5
MARGIN_H = 5

driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
page_link = "https://decklog.bushiroad.com/view/B2RN"
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

    img_link = card.find_element_by_tag_name("img").get_attribute("data-src")
    num = card.find_element_by_class_name("num").get_attribute("textContent")
    deck.append(CardEntry(img_link, num))

pdf = generate_pdf_proxy({
    "card_width": CARD_W,
    "card_height": CARD_H,
    "x_margin": MARGIN_W,
    "y_margin": MARGIN_H,
    "x_padding": PADDING_W,
    "y_padding": PADDING_H
}, deck)

pdf.output("deck.pdf", 'F')
