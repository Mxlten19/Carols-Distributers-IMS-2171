from fpdf import FPDF
import os

# -------------------------------------------
# SAFE TEXT CLEANER for FPDF 
# -------------------------------------------
def sanitize(text):
    return str(text).encode("latin-1", "ignore").decode("latin-1")


# -------------------------------------------
# BEAUTIFUL RECEIPT GENERATOR
# -------------------------------------------
def generate_receipt(transaction, items):

    # Ensure receipts folder exists
    receipts_dir = "receipts"
    os.makedirs(receipts_dir, exist_ok=True)

    pdf = FPDF()
    pdf.add_page()

    # ======================
    # HEADER
    # ======================
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, sanitize("Carol's Distributors"), ln=True, align="C")

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, sanitize("OFFICIAL SALES RECEIPT"), ln=True, align="C")
    pdf.ln(4)

    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, sanitize(f"Transaction #: {transaction.transaction_id}"), ln=True)
    pdf.cell(0, 6, sanitize(f"Date: {transaction.date.strftime('%Y-%m-%d %H:%M:%S')}"), ln=True)
    pdf.ln(6)

    # ======================
    # ITEMS TABLE HEADER
    # ======================
    pdf.set_font("Arial", "B", 11)
    pdf.cell(95, 8, "Item", border=1)
    pdf.cell(30, 8, "Qty", border=1, align="C")
    pdf.cell(30, 8, "Unit Price", border=1, align="R")
    pdf.cell(35, 8, "Total", border=1, align="R")
    pdf.ln()

    # ======================
    # ITEMS
    # ======================
    pdf.set_font("Arial", "", 10)
    subtotal = 0

    for item in items:
        line_total = item["qty"] * item["price"]
        subtotal += line_total

        pdf.cell(95, 8, sanitize(item["name"][:40]), border=1)
        pdf.cell(30, 8, sanitize(item["qty"]), border=1, align="C")
        pdf.cell(30, 8, sanitize(f"${item['price']:.2f}"), border=1, align="R")
        pdf.cell(35, 8, sanitize(f"${line_total:.2f}"), border=1, align="R")
        pdf.ln()

    # ======================
    # TOTALS
    # ======================
    tax = subtotal * 0.15
    grand_total = subtotal + tax

    pdf.ln(6)
    pdf.set_font("Arial", "B", 11)

    pdf.cell(125, 8, "Subtotal:", border=0)
    pdf.cell(35, 8, sanitize(f"${subtotal:.2f}"), border=0, align="R")
    pdf.ln()

    pdf.cell(125, 8, "Tax (15%):", border=0)
    pdf.cell(35, 8, sanitize(f"${tax:.2f}"), border=0, align="R")
    pdf.ln()

    pdf.cell(125, 8, "TOTAL:", border=0)
    pdf.cell(35, 8, sanitize(f"${grand_total:.2f}"), border=0, align="R")
    pdf.ln(12)

    # ======================
    # FOOTER
    # ======================
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(
        0,
        6,
        sanitize("Thank you for shopping with Carol's Distributors.\nAll sales are final.")
    )

    # ======================
    # SAVE FILE
    # ======================
    filename = f"receipt_{transaction.transaction_id}.pdf"
    filepath = os.path.join(receipts_dir, filename)

    pdf.output(filepath)

    return filename
