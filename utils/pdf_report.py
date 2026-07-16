from fpdf import FPDF
from datetime import datetime
import os

def create_pdf(
    event,
    customer,
    collective,
    profit,
    commission,
    best_menu
):

    REPORT_DIR = "reports"

    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)


    filename = os.path.join(
        REPORT_DIR,
        f"{event.replace(' ','_')}_Report.pdf"
    )


    pdf = FPDF()

    pdf.add_page()


    pdf.set_font(
        "Arial",
        "B",
        16
    )


    pdf.cell(
        0,
        10,
        "DIPAC Event Intelligence Report",
        ln=True
    )


    pdf.ln(10)


    pdf.set_font(
        "Arial",
        "",
        12
    )


    content = f"""
Event:
{event}


Customer Spending:
Rp {customer:,.0f}


Collective Income:
Rp {collective:,.0f}


Profit Contribution:
Rp {profit:,.0f}


Commission Rate:
{commission:.2f}%


Best Performing Menu:
{best_menu}


Generated:
{datetime.now().strftime('%d-%m-%Y')}
"""


    for line in content.split("\n"):

        pdf.cell(
            0,
            8,
            line,
            ln=True
        )


    pdf.output(filename)


    return filename