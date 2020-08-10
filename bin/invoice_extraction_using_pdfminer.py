from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

output_string = StringIO()
invoice_file = 'path/to/invoice'

# This is our quantitative template
custom_laparams_for_paytm = LAParams(line_overlap=0.5, char_margin=100.0, line_margin=0.5, 
                                     word_margin=100, boxes_flow=0.5, detect_vertical=False, all_texts=False)

with open(invoice_file, 'rb') as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=custom_laparams_for_paytm)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)

# print(output_string.getvalue())

lines = output_string.getvalue().split('\n')
print('Number of lines in invoice : ' + str(len(lines)))
# print(lines)

for line in lines:
    if ':' in line and 'Total Amount Paid' in line:
        print('Invoice total : ' + line.split(':')[1])