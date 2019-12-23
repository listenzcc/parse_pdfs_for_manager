# code: utf-8

from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfrw import PdfReader
from io import StringIO
import unicodedata
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
        print('-' * 80)
        print('PdfPath  :', self.path)
        print('Title    :', self.title)
        print('Keywords :', self.keywords)

    def str_filter(self, raw):
        normalized = unicodedata.normalize('NFKC', raw)
        changed = ''.join(c for c in normalized if unicodedata.category(c) in
                          ['Ll', 'Lu', 'Zs', 'Po', 'Ps', 'Pe', 'Cc'])
        for c in ['(', ')', '\n', ':']:
            changed = changed.replace(c, ',')
        out = [e.strip().lower() for e in changed.split(',') if len(e) > 0]
        return out

    def parse(self):
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
            # pdb.set_trace()
            page_limit -= 1
            if page_limit == 0:
                break
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if not isinstance(x, LTTextBoxHorizontal):
                    continue
                results = x.get_text()

                # print(results.encode())

                if results.startswith('Keywords'):
                    self.keywords = self.str_filter(results[8:])
                    break

                if results.startswith('Key words'):
                    self.keywords = self.str_filter(results[9:])
                    break

                if results.startswith('Index Terms'):
                    self.keywords = self.str_filter(results[11:])
                    break


def pdf2text(pdf_file):
    from io import StringIO
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfinterp import PDFResourceManager, process_pdf

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdf_file)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return (content)

pdf_dir = os.path.join(os.environ.get('ONEDRIVE'), 'documents', 'schorlar')

for fname in os.listdir(pdf_dir):
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

# x = pdf2text(open(os.path.join(pdf_dir, fname), 'rb'))
# print(x)
