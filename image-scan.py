# import packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os, subprocess
from matplotlib import pyplot as plt
import sys
import fitz
from tika import parser # pip

global factureDate
global numeroFacture



#numéro de facture  galere mais fait
# factureDate       fait
# montantHT         trop 
# montantTTC        dur
# montantTVA        ptn
# frais de port    ahhhhhhh
# fournisseur     a voir

def find_facture_png(access):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", required = True, help = "Path to the image")

    args = vars(parser.parse_args())
    if (access == 1):
        img = cv2.imread(args["image"],0)

    file_ta = "{}.png".format(os.getpid())
    if access == 0:
        file_ta = convert_pdf_to_png()

    if (access == 1):
        cv2.imwrite(file_ta, img)


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

    count_elems_factur(text)

def count_elems_factur(text):
    global factureDate
    global numeroFacture
    facture = 0
    contrat = 0
    unique = 1
    elements = text.lower().split()
    arrayNumeroFacture = []
    arrayNumero2Facture = []

    compteur1 = -1


    #ici on recupere les elements tels la date le fournisseur etc
    for i in elements:
        try:  
            if (i[2] == "/" and i[5] == "/" and unique == 1):
                factureDate = i
                unique = 0
        except Exception:
            pass

        
        if (i == "facture" or "facture :"):
            compteur1 += 1
            
        if (compteur1 >= 0):
            compteur1 += 1
            if (compteur1 > 2):   
                compteur1 = -1
            else:
                arrayNumeroFacture.append(i)



        if i == "facture" or i == "facturé":
            facture += 3

        if i == "total" or i == "tva" or i == "ttc":
            facture += 1

        if i == "iban" or i == "ban":
            facture += 1

        if i == "factur" or i == "factures":
            facture += 1
        
        if i == "siret" or i == "paiement" or i == "paiemen":
            facture += 1


    print(facture)
    print(contrat)


    if (facture >= 0 and  facture <= 10):
        print("il ne s'agit surement pas d'une facture")
        print("Nous sommes désolé, nous n'arrivons pas a determiner le type du fichier")

    
    if (facture > 10 and  facture <= 30):
        print("il s'agit surement d'une facture")
  
    if (facture > 30):
        print("il s'agit d'une facture")

    # if (contrat == facture):
    #     print("Nous sommes désolé, nous n'arrivons pas a determiner le type du fichier")

    arrayResultNumeroFacture = []
    arrayNumero4Facture = []

    for elem in arrayNumeroFacture:
        compteurint = 0

        if len(elem) > 6:
            arrayNumero2Facture.append(elem)
            if ((elem[2] == "/" and elem[5] == "/") or (elem[2] == "." and elem[5] == ".")):
                elem = "tupasseraspas"

            if(elem[0] == 'n' and elem[1] == '°'):
                arrayResultNumeroFacture.append(elem)
                break

            for i in elem:
                try:  
                    int(i)
                    compteurint += 1
                except Exception:
                    pass
            if (len(elem) - compteurint < 3):
                arrayResultNumeroFacture.append(elem)
                
    compteurFinalFacture = 0
    if (len(arrayResultNumeroFacture) == 1):
        numeroFacture = (arrayResultNumeroFacture[0])
    else:
        
        for elem in arrayResultNumeroFacture:
            if (elem == arrayResultNumeroFacture[0]):
                compteurFinalFacture += 1
            
        if compteurFinalFacture > 1:
            numeroFacture = (arrayResultNumeroFacture[0])
        
        else: numeroFacture = ""


    print()
    print ("Date de facture:", factureDate)
    print("Numero de facture:", numeroFacture)




def find_facture_pdf(raw):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    args = ["pdftotext",
            '-enc',
            'UTF-8',
            sys.argv[2].format(SCRIPT_DIR),
            '-']
    res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = res.stdout.decode('utf-8')
    file_txt = sys.argv[2] + ".txt"
    f = open(file_txt, "w")
    txt = output.lower()
    f.write(txt)
    f.close()
    count_elems_factur(txt)


access = 1
error = 1
tmp = sys.argv[2]

if (tmp.endswith(".png") or tmp.endswith(".jpg") or tmp.endswith(".jpeg")):
    access = 1
    error = 0
    find_facture_png(access)

elif (tmp.endswith(".pdf")):
    error = 0
    raw = parser.from_file(tmp)
    # print(raw['content'])
    find_facture_pdf(raw)

if (error == 1):
    print("Il y'a une erreur, le format du fichier n'est pas le bon. \nSeuls les fichiers de type .pdf, .jpg, .jpeg ou .png sont autorisés")
    exit (84)


 
