# code: utf-8

import os
from pdfrw import PdfReader
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

doc = PDFDocument()
rsrcmgr = PDFResourceManager()
laparams = LAParams()


class PdfParser():
    def __init__(self, path):
        self.path = path
        reader = PdfReader(path)
        self.info = reader.Info
        self.title = self.info.Title.title()
        self.context = []

    def print_brief(self):
        print('-' * 80)
        print(self.path)
        print(self.title)
        print(self.context)

    def parse_pdf(self):
        with open(self.path, 'rb') as fp:
            praser = PDFParser(fp)
            praser.set_document(doc)
            doc.set_parser(praser)
            doc.initialize()

            if not doc.is_extractable:
                raise PDFTextExtractionNotAllowed

            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            layout = device.get_result()
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            page = doc.get_pages()[0]
            interpreter.process_page(page)
            for x in layout:
                if not isinstance(x, LTTextBoxHorizontal):
                    continue
                self.context.append(x.get_text())


target_dir = 'C:\\Users\\zcc\\OneDrive\\Documents\\schorlar'

pdf_path = [os.path.join(target_dir, f)
            for f in os.listdir(target_dir) if f.endswith('.pdf')]

for path in pdf_path:
    pp = PdfParser(path)
    pp.print_brief()

'''
for fname in os.listdir(target_dir):
    # for fname in ['07264993.pdf']:
    if fname.endswith('.pdf'):
        try:
            pp = PdfParser(os.path.join(pdf_dir, fname))
            pp.print_brief()
        except UnicodeEncodeError as error:
            print(error)
            pass
        except AttributeError as error:
            print(error)
            pass
'''
