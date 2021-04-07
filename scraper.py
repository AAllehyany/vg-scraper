from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import requests
from fpdf import FPDF
from deck import CardEntry

CARD_W=59
CARD_H=86
PADDING_W = 10
PADDING_H = 10
MARGIN_W = 5
MARGIN_H = 5

driver = webdriver.Chrome(executable_path=r"C:\Users\tickt\dev\chromedriver.exe")
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
    num = card.find_element_by_class_name("num").text
    deck.append(CardEntry(img_link, num))

pdf = FPDF('P', 'mm', 'A4')

line = 0
counter = 0
for card in deck:
    for _ in range(int(card.copies)):
        mod = counter % 9
        img = card.img_link
        sp = counter % 3

        if sp == 0:
            line += 1

        if mod == 0:
            pdf.add_page()
            line = 0

        x = PADDING_W + (sp * CARD_W) + (sp * MARGIN_W)
        y = PADDING_H + (line * CARD_H) + (line * MARGIN_H)
        pdf.image(img, x=x, y=y, w=CARD_W, h=CARD_H)
        counter += 1

pdf.output("deck.pdf", 'F')
