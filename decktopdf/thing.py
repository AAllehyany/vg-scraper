
@app.get("/get/{code}")
async def create_pdf(code: str, size: int = 1, lang: int = 1):
    
    settings = sml_settings
    
    if size == 2:
        settings = std_settings

    website = "https://decklog-en.bushiroad.com/view"

    if lang == 2:
        website = "https://decklog.bushiroad.com/view"

    sc = scraper.Scraper(code, settings.end_point, settings, website)

    try:
        sc.scrape_deck()
        result = sc.upload_deck()

        return {
            "pdf_link": result,
            "success": 1
        }
    except:
        return {
            "success": 0,
            "message": "Invalid deck code"
        }


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

