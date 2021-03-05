from tika import parser # pip install tika
import ocrmypdf


raw = parser.from_file('synapture/test3.pdf')
print(raw['content'])

ocrmypdf.ocr("synapture/test3.pdf", "synapture/test3.pdf", rotate_pages=True)