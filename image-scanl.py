# import packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
from matplotlib import pyplot as plt
import sys
import fitz


facture = 0
contrat = 0

def convert_pdf_to_png():
    pdffile = sys.argv[2]
    doc = fitz.open(pdffile)
    page = doc.loadPage(0)  # number of page
    pix = page.getPixmap()
    file_ta = pdffile + ".png"
    pix.writePNG(file_ta)
    return (file_ta)
#Construct and Parse The Argument

access = True
tmp = sys.argv[2]
print (tmp)

if (tmp[len(tmp)-4:]) == ".pdf":
    access = False

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required = True, help = "Path to the image")

args = vars(parser.parse_args())
if (access == True):
    img = cv2.imread(args["image"],0)



file_ta = "{}.png".format(os.getpid())

if access == False:
    file_ta = convert_pdf_to_png()

if (access == True):
    cv2.imwrite(file_ta, img)



# else :
#     print("Error with file, need a pdf")
#     exit (84)


file_txt = sys.argv[2] + ".txt"
img = cv2.imread(file_ta,0)

file_ta = "{}.png".format(os.getpid())
# print(filename)
cv2.imwrite(file_ta, img)

# Load the image using PIL (Python Imaging Library), Apply OCR, and then delete the temporary file
text = pytesseract.image_to_string(Image.open(file_ta))
os.remove(file_ta)

f = open(file_txt, "w")
f.write(text.lower())
f.close()















#"algo" determinant a dire s'il s agit d'une facture ou d'un contrat

# print(text)
# print (file_txt)
elements = text.lower().split()

    
for i in elements:
    if i == "facture" or i == "facturé":
        facture += 1

    if i == "total" or i == "tva" or i == "ttc":
        facture += 1

    if i == "iban" or i == "ban":
        facture += 1

    if i == "factur" or i == "factures":
        facture += 1
    
    if i == "siret" or i == "paiement" or i == "paiemen":
        facture += 1
    #ici les elements d'un contrat
    # if 'contrat' in f.read():
    #     contrat += 1


print(facture)
print(contrat)
if (facture > contrat and facture >= 5):
    print("il s'agit tres certainement d'une facture")

if (contrat > facture):
    print("il s'agit tres certainement d'un contrat")

if (contrat == facture):
    print("Nous sommes désolé, nous n'arrivons pas a determiner le type du fichier")
 



 