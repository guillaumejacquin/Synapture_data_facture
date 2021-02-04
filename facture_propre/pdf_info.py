
import os
import subprocess
import sys
from tika import parser # pip
import time
import json
import os.path


from elems_facture.numero_facture import *
from elems_facture.date import *
from elems_facture.montant_total import *
from elems_facture.tva import *
from elems_facture.indicefacture import *
from elems_facture.print_data import *

start_time = time.time()


#numéro de facture  galere mais fait
# factureDate       fait
# montantHT         trop 
# montantTTC        dur
# montantTVA        ptn
# frais de port    ahhhhhhh
# fournisseur     a voir

def differentfile(file_given):
    error = 1

    if (file_given.endswith(".pdf")):
        error = 0
        raw = parser.from_file(file_given)
        # print(raw['content'])
        return (find_facture_pdf(raw, file_given))

    
    if (file_given.endswith(".txt")):
        error = 0
        source = file_given

        return (txt(file_given))
        
    if (error == 1):
        print("Il y'a une erreur, le format du fichier n'est pas le bon. \nSeuls les fichiers de type .pdf, .jpg, .jpeg ou .png sont autorisés")
        exit (84)  


def find_facture_pdf(raw, file_given):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    args = ["pdftotext", '-enc', 'UTF-8', file_given.format(SCRIPT_DIR), '-']
    res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = res.stdout.decode('utf-8')
    file_txt = file_given + ".txt"
    f = open(file_txt, "w")
    txt = output.lower()
    f.write(txt)
    f.close()

    return (general(txt, file_given))


def txt(file_given):
    f = open(file_given, "r")
    text = f.read()

    return (general(text, file_given))

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

def general(text, file_given):
    elements = text.lower().split()

    unique = 1
    compteurNumeroFacture = -1
    factureornot = True

    array_montant_societe = []
    arrayTotalMontant2_convert = []
    tva_probable = []  
    arrayResultNumeroFacture = []
    arrayTotalMontant2 = []
    arrayNumeroFacture = []
    arrayResultNumeroFacture = []

    nb_indiceFacture = 0
    montantTotal = 0.0
    montantHt = 0
    tva = 0.0


    source = give_source_name(file_given)

    #ici on recupere les elements tels la date le fournisseur etc
    for i in elements:
        nb_indiceFacture = number_indice(i, nb_indiceFacture)  #COMPTEUR POUR VOIR SI IL S AGIT D UNE FACTURE

        unique = getFactureDate(i, unique)                 #LA DATE EST LE PLUS FACILE A RECUPERER, on la recupere des le debut
        getFirstStripNumeroFacture(i, compteurNumeroFacture, arrayNumeroFacture)



    factureornot = printFactureOrNot(nb_indiceFacture)   #ICI JE DIS SI IL S AGIT D UNE FACTURE
    if (factureornot == False):
        return (1)

    array_montant_societe = check_price(source, arrayTotalMontant2, file_given)


    for i in range(len(elements)):
        arrayTotalMOntant2 = GetObviousELementsTotalFacture(elements, i, arrayTotalMontant2)

    arrayTotalMontant2_convert = convert_symbols(arrayTotalMontant2, arrayTotalMontant2_convert)
    try:
        range_array_obviouse_elem = len(arrayTotalMontant2_convert)

        # print(range_array_obviouse_elem)

        arrayTotalMontant2_convert = str_to_float_montant_total(i, range_array_obviouse_elem, arrayTotalMontant2_convert)

        arrayTotalMontant2_convert = remove_useless_numbers(arrayTotalMontant2_convert, array_montant_societe)  #


        montantTotal = max(arrayTotalMontant2_convert)
        tva_probable = all_results_tva(tva_probable, montantTotal)


        montantHt,compteur = get_compteur(arrayTotalMontant2_convert, tva_probable, montantHt)
        tva = get_tva(montantHt, compteur, tva)

    except Exception:
        print("pas encore fait")
        return (get_total_mount_not_obvious(arrayTotalMOntant2))



    for elem in arrayNumeroFacture:
        FirstTabNumeroFacture(elem, arrayResultNumeroFacture)
    numeroFacture = getResultNumeroFacture(arrayResultNumeroFacture)

    data = {
    "date" : factureDate,
    "numero de facture" : numeroFacture,
    "montant total " : montantTotal,
    "tva " : tva,
    "montantHt" : montantHt
    }
    
    # print_data(factureDate, numeroFacture, montantTotal, tva, montantHt)

    print("--- %s seconds ---" % (time.time() - start_time))

    return data


def get_total_mount_not_obvious(Array_Differents_Montants):
    print(Array_Differents_Montants)


def give_source_name(file_given):
    if (file_given.endswith(".txt")):
        source = file_given
    else:
        source = file_given + ".txt"
    return (source)


def get_compteur(arrayTotalMontant2_convert, tva_probable, montantHt):
    compteur = 0
    find = False
    for i in arrayTotalMontant2_convert:
        compteur = 0
        for j in tva_probable:
                if i == j:
                    montantHt = i
                    find = True
                    break
                compteur += 1

        if (find == True):
                break
            
    return(montantHt,compteur)