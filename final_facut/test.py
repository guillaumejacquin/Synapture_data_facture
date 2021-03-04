import pytesseract

img1 = "alaid.png"
text = pytesseract.image_to_string(img1)

print(text)