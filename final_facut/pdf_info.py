from imports.imports_facture import *
import pytesseract


start_time = time.time()
factureDate = ""
fournisseur = ""
numeroFacture = ""
montantTotal = 0.0
montantHt = 0.0


def give_source_name(file_given):
    if (file_given.endswith(".txt")):
        source = file_given
    else:
        source = file_given + ".txt"
    return (source)


def parse_type_file(file_given):
    error = True

    if (file_given.endswith(".pdf")):
        error = False
        raw = parser.from_file(file_given)
        return (create_txt_pdf(raw, file_given))

        
    if (file_given.endswith(".txt")):
        error = False
        return (create_txt_txt(file_given))
    
    if (file_given.endswith(".png") or file_given.endswith(".jpg")):
        error = False
        return(create_txt_png(file_given))


    if (error == True):
        print("Il y'a une erreur, le format du fichier n'est pas le bon. \nSeuls les fichiers de type .pdf, .jpg, .jpeg ou .png sont autorisés")
        exit (84)  

def create_txt_png(file_given):
    text = pytesseract.image_to_string(file_given)
    file_txt = file_given + ".txt"
    f = open(file_txt, "w")
    txt = text.lower()

    txt = list(txt)
    for i in range(len(txt)):
        if (txt[i].isdigit() and txt[i+1] == ' 'and txt[i+2].isdigit()):
            txt[i+1] = '_'
        if (txt[i] == ','):
            txt[i] = '.'
    txt = "".join(txt)
    f.write(txt)
    f.close()

    return (define_if_facture_or_not(txt, file_given))

def create_txt_pdf(raw, file_given):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    args = ["pdftotext", '-enc', 'UTF-8', file_given.format(SCRIPT_DIR), '-']
    res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = res.stdout.decode('utf-8')
    file_txt = file_given + ".txt"
    f = open(file_txt, "w")
    txt = output.lower()


    txt = list(txt)
    for i in range(len(txt)):
        if (txt[i].isdigit() and txt[i+1] == ' 'and txt[i+2].isdigit()):
            txt[i+1] = '_'

        if (txt[i] == ','):
            txt[i] = '.'


    txt = "".join(txt)
 

    f.write(txt)
    f.close()

    return (define_if_facture_or_not(txt, file_given))


def create_txt_txt(file_given):
    f = open(file_given, "r")
    txt = f.read()
    return (define_if_facture_or_not(txt, file_given))



def define_if_facture_or_not(text, file_given):
    source = ""
    source = give_source_name(file_given)

    elements = text.lower().split()
    nb_indiceFacture = 0

    for i in elements:
        nb_indiceFacture = number_indice(i, nb_indiceFacture)

    factureornot = printFactureOrNot(nb_indiceFacture)   #ICI JE DIS SI IL S AGIT D UNE FACTURE

    if (factureornot == True):
        return (get_all_data(source, text, file_given, elements))
    else:
        return(-1)

def get_all_data(source, text, file_given, elements):
    factureDate = ""
    montantHt = 0
    montantTotal = 0
    tva = 0
    numberFacture = 0

############################################################################ DATE ##############################################################
    factureDate = get_facture_date(elements)

    if (factureDate == ''):
        factureDate = get_facture_if_date_is_digit(elements)
############################################################################ DATE ##############################################################
############################################################################ NUMERO FACTURE ##############################################################
    numberFacture = get_number_facture(elements)

############################################################################ FACTURE  MAX obvious ##############################################################
    arrayTotalMontant2_convert = []
    arrayTotalMontant2 = []


    source = give_source_name(file_given)
    array_montant_societe = check_price(source, arrayTotalMontant2, file_given)


    
    for i in range(len(elements)):
        arrayTotalMOntant2 = GetObviousELementsTotalFacture(elements, i, arrayTotalMontant2)
    arrayTotalMontant2_convert = convert_symbols(arrayTotalMontant2, arrayTotalMontant2_convert)
    

    try:
        range_array_obviouse_elem = len(arrayTotalMontant2_convert)

        arrayTotalMontant2_convert = str_to_float_montant_total(i, range_array_obviouse_elem, arrayTotalMontant2_convert)
        arrayTotalMontant2_convert = remove_useless_numbers(arrayTotalMontant2_convert, array_montant_societe)

        
        montantTotal = max(arrayTotalMontant2_convert)

############################################################################ FACTURE  MAX obvious ##############################################################
############################################################################ MONTANT WITHOUT TAXS AND TVA ##############################################################
        if (montantTotal == 0):
            montantTotal = float(arrayTotalMontant2_convert) #je casse le try
        tva_probable = []
        tva = 0
        tva_probable = all_results_tva(tva_probable, montantTotal)
        montantHt = 0
        compteur = 0

        array_final = []
        array_tva = []

        montantHt,compteur = get_compteur(arrayTotalMontant2_convert, tva_probable, montantHt)
        tva = get_tva(montantHt, compteur, tva)

        if (tva == 0):                      #TENTATIVE SI IL ARRIVE JUSTE A RECUPERER LE MONTANT MAX
            for i in elements:
                try:
                    float(i)
                    if (not i.isnumeric()):
                        array_final.append(float(i))

                except Exception:
                    pass

            tva_probable = all_results_tva(tva_probable, montantTotal)
            array_final = list(dict.fromkeys(array_final))

            array_final.sort()
            possible_tva = array_final[-2]
            array_tva = [round(possible_tva -0.01, 2), round(possible_tva, 2), round(possible_tva +0.01, 2)]
            montantHt, tva = get_tva_complicated(montantTotal, array_tva)

############################################################################ MONTANT WITHOUT TAXS AND TVA ##############################################################
#SI Il n'y a pas de signes distinctifs comme "500 $" on prend le plus grand nombre a virugle (sinon risque que le code postal passe avant)
    except Exception:
        print("Pas evident a retrouver")
        array_number = []
        compteur = 0
        for i in elements:
            try:
                float(i)
                if (not i.isnumeric()):
                    if (float(elements[compteur]) < 99_999_999):
                        array_number.append(float(i))

            except Exception:
                pass
            compteur += 1
        

        montantTotal = max(array_number)

        try:
           if (float(array_montant_societe[0]) == montantTotal):
                array_number.remove(max(array_number))
                montantTotal = max(array_number)
        except Exception:
            montantTotal = max(array_number)
############################################################################ TAXS AND TVA (SI C EST PLUS DIFFICILE)##############################################################

        montantHt, tva = get_tva_complicated(montantTotal, array_number)

    return final_results(factureDate, numberFacture, montantTotal, tva, montantHt)




def final_results(factureDate, numberFacture, montantTotal, tva, montantHt):
    data = {
    "date" : factureDate,
    "numero de facture" : numberFacture,
    "montant total " : montantTotal,
    "tva " : tva,
    "montantHt" : montantHt
    }

    return data
