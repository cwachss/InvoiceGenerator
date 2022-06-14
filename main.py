from gen_invoice import InvoiceGenerator, Utility
import openpyxl as xl

invoice_count = 1
# generates an invoice for all customers of a certain anonymous transaction if the customer has not paid


def generate_invoice_pdf(worksheet, invoice_num):
    # comment2
    for row in worksheet.iter_rows():
        if not row[2].value:
            print(f"generating invoice for {row[0].value}")
            OUTFILE_HTML = r"C:\Users\chani\PycharmProjects\InvoiceGenerator\output\\" + f"{row[0].value}.html"
            OUTFILE_PDF = r"C:\Users\chani\PycharmProjects\InvoiceGenerator\output\\" + f"{row[0].value}.pdf"

            # Load template and stylesheet data from file
            template = Utility.read_file("template.html")
            stylesheet = Utility.read_file("stylesheet.css")

            # Generate invoice
            generator = InvoiceGenerator()
            generator.generate(

                # the output HTML file
                outfile=OUTFILE_HTML,

                # invoice number

                number=f"INV{invoice_num:03}",

                # line items
                items=[
                    {
                        "Section": "Materials",
                        "Item": "Widget A",
                        "Quantity": "20",
                        "Units": "pcs",
                        "Price": "12.99"
                    }
                ],

                # Our payee details
                payee={
                    "name": "Chana Wachsstock inc.",
                    "identifier": "123456789",
                    "email": "domestic@example.com",
                    "address": [
                        "1 Widget Road",
                        "Widgetville",
                        "WID 9999"
                    ],
                    "bank": {
                        "holder": "Chana Wachsstock",
                        "bank": "River Banking Co",
                        "code": "123-456",
                        "account": "192837465"
                    }
                },

                # payer details
                payer={
                    "name": row[0].value,
                    "identifier": row[3].value,
                    "email": row[1].value,
                    "address": [
                        row[4].value,
                        f"{row[6].value}, {row[7].value}",
                        row[8].value
                    ],
                },

                # template and stylesheet
                template=template,
                stylesheet=stylesheet,

                # No tax
                tax=.08,

                # Generate a domestic invoice rather than an international one
                is_international=False,

                # Generate an invoice rather than a quote
                is_quote=False
            )

            # Render the invoice HTML to a PDF file using electron-pdf
            generator.render(OUTFILE_HTML, OUTFILE_PDF)
            print(f"done ({row[0].value})")
            invoice_num += 1


wb = xl.load_workbook("People_Info.xlsx")

sheet = wb["Sheet1"]

generate_invoice_pdf(sheet, invoice_count)