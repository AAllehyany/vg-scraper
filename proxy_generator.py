from fpdf import FPDF


def generate_pdf_proxy(print_settings, print_list):
    """Generates a pdf file of cards proxy ready to be printed

    Parameters:
    print_settings (dict): Contains card size, and spaces between each card
    print_list (list): List of dict of card images/links to images with copies

    Returns:
    stream: PDF file stream
    """

    pdf = FPDF('P', 'mm', 'A4')
    line = 0
    counter = 0

    for card in print_list:
        for _ in range(int(card.copies)):
            mod = counter % 9
            img = card.img_link
            sp = counter % 3

            if sp == 0:
                line += 1

            if mod == 0:
                pdf.add_page()
                line = 0

            x = print_settings["x_padding"] + (sp * (print_settings["card_width"] + print_settings["x_margin"]))
            y = print_settings["y_padding"] + (line * (print_settings["card_height"] + print_settings["y_margin"]))
            pdf.image(img, x=x, y=y, w=print_settings["card_width"], h=print_settings["card_height"])
            counter += 1

    return pdf

