import pytesseract

img1 = "synapture/doc.pdf"
text = pytesseract.image_to_string(img1)

print(text)