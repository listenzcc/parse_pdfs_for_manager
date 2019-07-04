# code: utf-8

from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfrw import PdfReader
import os
import sys
import importlib
import pdb
importlib.reload(sys)


class PdfParser():
    def __init__(self, path):
        self.path = path
        self.info = None
        self.keywords = None
        self.title = None
        self.parse()

    def print_brief(self):
        # for e in pp.info.items():
        #     print(e[0], ': ', e[1])
        print('Title    :', self.title)
        print('Keywords :', self.keywords)

    def parse(self):
        print('-' * 80)
        print('PdfPath  :', self.path)
        reader = PdfReader(self.path)
        self.info = reader.Info
        title = self.info.Title.title()
        self.title = title[1:-1]

        fp = open(self.path, 'rb')
        praser = PDFParser(fp)
        doc = PDFDocument()
        praser.set_document(doc)
        doc.set_parser(praser)

        doc.initialize()

        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed

        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        page_limit = 3
        for page in doc.get_pages():
            page_limit -= 1
            if page_limit == 0:
                break
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    results = x.get_text()
                    results = ' '.join(results.split())

                    if results.startswith('Keywords'):
                        self.keywords = results.split()
                        break

                    if results.startswith('Key words'):
                        self.keywords = results.split()
                        break


pdf_dir = 'C:\\Users\\liste\\OneDrive\\Documents\\schorlar'
for fname in os.listdir(pdf_dir):
    if fname.endswith('.pdf'):
        try:
            pp = PdfParser(os.path.join(pdf_dir, fname))
            pp.print_brief()
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
