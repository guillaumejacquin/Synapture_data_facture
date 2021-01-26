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
import time

start_time = time.time()
factureDate = ""
fournisseur = ""
numeroFacture = ""
montantTotal = 0.0


#numéro de facture  galere mais fait
# factureDate       fait
# montantHT         trop 
# montantTTC        dur
# montantTVA        ptn
# frais de port    ahhhhhhh
# fournisseur     a voir

def differentfile():
    tmp = sys.argv[2]
    error = 1

    if (tmp.endswith(".png") or tmp.endswith(".jpg") or tmp.endswith(".jpeg")):
        error = 0
        find_facture_png()

    elif (tmp.endswith(".pdf")):
        error = 0
        raw = parser.from_file(tmp)
        # print(raw['content'])
        find_facture_pdf(raw)
    
    if (error == 1):
        print("Il y'a une erreur, le format du fichier n'est pas le bon. \nSeuls les fichiers de type .pdf, .jpg, .jpeg ou .png sont autorisés")
        exit (84)

    
def find_facture_png():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", required = True, help = "Path to the image")
    args = vars(parser.parse_args())

    img = cv2.imread(args["image"],0)
    file_ta = "{}.png".format(os.getpid())

    
    cv2.imwrite(file_ta, img)

    file_txt = sys.argv[2] + ".txt"
    img = cv2.imread(file_ta,0)
    file_ta = "{}.png".format(os.getpid())
    cv2.imwrite(file_ta, img)
    text = pytesseract.image_to_string(Image.open(file_ta))
    os.remove(file_ta)

    f = open(file_txt, "w")
    f.write(text.lower())
    f.close()
    general(text)



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
    general(txt)


def getResultNumeroFacture(arrayResultNumeroFacture):
    compteurFinalFacture = 0

    if (len(arrayResultNumeroFacture) == 1):
        numeroFacture = (arrayResultNumeroFacture[0])
    else:   
        for elem in arrayResultNumeroFacture:
            if (elem == arrayResultNumeroFacture[0]):
                compteurFinalFacture += 1
            if (elem[0] == 'n' and elem[1] == '°'):
                numeroFacture = elem
                return (numeroFacture)
            
        if compteurFinalFacture > 1:
            numeroFacture = (arrayResultNumeroFacture[0])
        else: numeroFacture = ""

    return (numeroFacture)

def getFirstStripNumeroFacture(i, compteurNumeroFacture, arrayNumeroFacture):
    if (i == "facture" or "facture :"):
        compteurNumeroFacture += 1               
        if (compteurNumeroFacture >= 0):
                compteurNumeroFacture += 1
        if (compteurNumeroFacture > 2):   
                    compteurNumeroFacture = -1
        else:
            arrayNumeroFacture.append(i)


# def getElementsTotalFacture(i, arrayTotalMontant1):
#     if (i == "montant" or i == "montant :" or i == "montant:"  or i == "total" or i == "total :" or i == "total:"):
#         arrayTotalMontant1.append(i)
        
#     return (arrayTotalMontant1)


# def GetObviousELementsTotalFacture(i, arrayTotalMontant2):
#     print (i)
#     if (i == "€" or i == "euros" or i == "dollars" or i == "$"):
#             arrayTotalMontant2.append(int(i -1))

#     return(arrayTotalMontant2)

        
def getFactureDate(i, unique):

    global factureDate
    try:  
        if (i[2] == "/" and i[5] == "/" and unique == 1):
                factureDate = i
                unique = 0
    except Exception:
        pass
    return (unique)

def FirstTabNumeroFacture(elem, arrayResultNumeroFacture):
    compteurint = 0

    if len(elem) > 6:

        if ((elem[2] == "/" and elem[5] == "/") or (elem[2] == "." and elem[5] == ".")):
            return()

        for i in elem:
            try:  
                int(i)
                compteurint += 1
            except Exception:
                pass
            if (len(elem) - compteurint < 3) or (elem[0] == 'n' and elem[1] == '°'):
                arrayResultNumeroFacture.append(elem)

def printFactureOrNot(facture):
    
    if (facture >= 0 and  facture <= 200):
        print("il ne s'agit surement pas d'une facture")
        print("Nous sommes désolé, nous n'arrivons pas a determiner le type du fichier")
    
    if (facture > 201 and  facture <= 1000):
        print("il s'agit surement d'une facture")
  
    if (facture > 1001):
        print("il s'agit d'une facture")


def general(text):

    nb_indiceFacture = 0
    unique = 1
    elements = text.lower().split()
    arrayNumeroFacture = []
    arrayResultNumeroFacture = []
    compteurNumeroFacture = -1
    compteurMontalTotant = -1


    arrayTotalMontant1 = []
    arrayTotalMontant2 = []
    arrayTotalMontantFloat = []
    compteur_postal = 0
    montantTotal = 0.0
    

    #ici on recupere les elements tels la date le fournisseur etc
    for i in elements:
        if i == "facture" or i == "facturé" or "facture :" or i == "factur" or i == "factures":
            nb_indiceFacture += 3
        if i == "total" or i == "tva" or i == "ttc" or  i == "iban" or i == "ban" or i == "siret" or i == "paiement" or i == "paiemen":
            nb_indiceFacture += 1

        elem2 = i.replace(",", ".")


        try:
            float(elem2)
            compteur_postal += 1
            if (compteur_postal > 2):
                arrayTotalMontantFloat.append(elem2)
    
        except Exception:
            pass



        unique = getFactureDate(i, unique)
        getFirstStripNumeroFacture(i, compteurNumeroFacture, arrayNumeroFacture)


        # arrayTotalMontant1= getElementsTotalFacture(i, arrayTotalMontant1)
        # arrayTotalMontant2 = GetObviousELementsTotalFacture(i, arrayTotalMontant2)
      
    result_array_total = []




    printFactureOrNot(nb_indiceFacture)
  
    for elem in arrayNumeroFacture:
        FirstTabNumeroFacture(elem, arrayResultNumeroFacture)


      


        


    
    numeroFacture = getResultNumeroFacture(arrayResultNumeroFacture)


    print()
    print ("Date de facture:", factureDate)
    print("Numero de facture:", numeroFacture)
    print("Fournisseur:")
    print ("Montant:", montantTotal)

    

    print("--- %s seconds ---" % (time.time() - start_time))

differentfile()



 
