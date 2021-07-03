from fastapi import FastAPI
from decktopdf import scraper

CARD_W=63
CARD_H=88
PADDING_W = 10
PADDING_H = 10
MARGIN_W = 5
MARGIN_H = 5
ENDPOINT = 'https://s3.eu-central-1.wasabisys.com'

settings = {
    "card_width": CARD_W,
    "card_height": CARD_H,
    "x_margin": MARGIN_W,
    "y_margin": MARGIN_H,
    "x_padding": PADDING_W,
    "y_padding": PADDING_H
}

app = FastAPI()

@app.get("/")
def index():
    link = scraper.scrape_and_upload("M6H5", settings)
    return {"deck_pdf": link}
