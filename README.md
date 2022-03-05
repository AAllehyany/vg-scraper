# VG Scraper

Scrapes deck data from [](https://decklog-en.bushiroad.com/) or [](https://decklog.bushiroad.com/) and creates a PDF proxy for the deck that is ready to print.

### Technologies:
Uses Selenium for scraping and Typer for the command line interface.

### Example
![Command Line Example](https://s3.us-west-1.wasabisys.com/decks-project/deck-image/2022-03-05%2007_07_30-Command%20Prompt.png)

You can provide different options for the command line app. --standard makes the scraper treat the card size as Standard Card Size (Weiss), --jp makes it scrape from the japanese website.

![Result PDF Example](https://s3.us-west-1.wasabisys.com/decks-project/deck-image/2022-03-05%2007_08_18-8YP4%20(1).pdf.png)

The resulting PDF file contains all the cards laid out nicely in a PDF form.