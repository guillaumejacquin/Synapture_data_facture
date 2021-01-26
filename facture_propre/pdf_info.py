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

from elems_facture.numero_facture import *
from elems_facture.date import *
from elems_facture.montant_total import *
from elems_facture.tva import *
from elems_facture.indicefacture import *
from elems_facture.print_data import *





start_time = time.time()
factureDate = ""
fournisseur = ""
numeroFacture = ""
montantTotal = 0.0
montantHt = 0.0
source = sys.argv[2] + ".txt"


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

    if (tmp.endswith(".pdf")):
        error = 0
        raw = parser.from_file(tmp)
        # print(raw['content'])
        find_facture_pdf(raw)

    
    if (tmp.endswith(".txt")):
        error = 0
        source = sys.argv[2]

        txt()


    if (error == 1):
        print("Il y'a une erreur, le format du fichier n'est pas le bon. \nSeuls les fichiers de type .pdf, .jpg, .jpeg ou .png sont autorisés")
        exit (84)

    

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


def txt():

    f = open(sys.argv[2], "r")
    text = f.read()

    print(text)

    general(text)


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

def getFactureDate(i, unique):

    global factureDate
    try:  
        if (i[2] == "/" and i[5] == "/" and unique == 1):
                factureDate = i
                unique = 0
    except Exception:
        pass
    return (unique)

def general(text):

    nb_indiceFacture = 0
    unique = 1
    elements = text.lower().split()
    arrayNumeroFacture = []
    arrayResultNumeroFacture = []
    compteurNumeroFacture = -1
    arrayTotalMontant2 = []
    arrayTotalMontantFloat = []

    array_montant_societe = []
    arrayTotalMontant2_convert = []
    compteur_postal = 0
    montantTotal = 0.0
    factureornot = True
    montantHt = 0
    tva20 = 0.0
    tva10 = 0.0
    tva5 = 0.0
    tva2 = 0.0
    tva = 0.0

    if (sys.argv[2].endswith(".txt")):
        source = sys.argv[2]
    
    if (sys.argv[2].endswith(".pdf")):
        source = sys.argv[2] + ".txt"

    #ici on recupere les elements tels la date le fournisseur etc
    for i in elements:
        nb_indiceFacture = number_indice(i, nb_indiceFacture)

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

    array_montant_societe = check_price(source, arrayTotalMontant2)



    factureornot =  printFactureOrNot(nb_indiceFacture)
    if (factureornot == False):
        return (1)


    for i in range(len(elements)):
        arrayTotalMOntant2 = GetObviousELementsTotalFacture(elements, i, arrayTotalMontant2)


    for i in arrayTotalMontant2:
        conversion = i.replace(",", ".") 
        conversion2 = conversion.replace('€', ' ')
        conversion3 = conversion2.replace('$', ' ')

        arrayTotalMontant2_convert.append(conversion3)

    try:
        for i in range(0, len(arrayTotalMontant2_convert)): 
            try:
                arrayTotalMontant2_convert[i] = float(arrayTotalMontant2_convert[i]) 

            except Exception:
                arrayTotalMontant2_convert[i] = 0

        max_array = max(arrayTotalMontant2_convert)
     
        try:
            if (max_array == float(array_montant_societe[0])):
                        arrayTotalMontant2_convert.remove(max_array)
        except Exception:
            pass

        max_array = max(arrayTotalMontant2_convert)
        montantTotal = max_array

        tva_probable = []        

        a = round((max_array / 1.2), 2)
        b = round((max_array / 1.1), 2)
        c = round((max_array / 1.155), 2)
        d = round((max_array / 1.11), 2)

        tva_probable.append(a)
        tva_probable.append(b)
        tva_probable.append(c)
        tva_probable.append(d)

        compteur = 0
        find = False
        print(tva_probable)

        for i in arrayTotalMontant2_convert:
            print(arrayTotalMontant2_convert)
            compteur = 0
            for j in tva_probable:
                if i == j:
                    montantHt = i
                    find = True
                    break

                compteur += 1

            if (find == True):
                break

        tva = get_tva(montantHt, compteur, tva)
      


    except Exception:
        print("pas encore fait")

  
    for elem in arrayNumeroFacture:
        FirstTabNumeroFacture(elem, arrayResultNumeroFacture)
    numeroFacture = getResultNumeroFacture(arrayResultNumeroFacture)



    print_data(factureDate, numeroFacture, montantTotal, tva, montantHt)
    

    print("--- %s seconds ---" % (time.time() - start_time))




def main():
    differentfile()




main()



 
