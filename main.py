from fastapi import FastAPI
from decktopdf import scraper
import typer

ENDPOINT = 'https://s3.eu-central-1.wasabisys.com'

std_settings = {
    "card_width": 63,
    "card_height": 88,
    "x_margin": 3,
    "y_margin": 3,
    "x_padding": 5,
    "y_padding": 5,
    "end_point": "https://s3.eu-central-1.wasabisys.com"
}

sml_settings = {
    "card_width": 59,
    "card_height": 86,
    "x_margin": 5,
    "y_margin": 5,
    "x_padding": 8,
    "y_padding": 8,
    "end_point": "https://s3.eu-central-1.wasabisys.com"
}


def main(code: str, standard: bool = typer.Option(False), jp: bool = typer.Option(False)):
    
    print(code)
    settings = sml_settings
    
    if standard:
        settings = std_settings

    website = "https://decklog-en.bushiroad.com/view"

    if jp:
        website = "https://decklog.bushiroad.com/view"

    sc = scraper.Scraper(code, ENDPOINT, settings, website)

    try:
        sc.scrape_deck()
        print(sc.upload_deck())
    except:
        print("The deck code you have entered is invalid. Please make sure the deck code belongs to a real deck on the bushiroad website")
    

if __name__ == "__main__":
    typer.run(main)
