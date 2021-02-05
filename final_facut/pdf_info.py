from imports.imports_facture import *

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
        source = file_given

        return (create_txt_txt(file_given))
            
    if (error == True):
        print("Il y'a une erreur, le format du fichier n'est pas le bon. \nSeuls les fichiers de type .pdf, .jpg, .jpeg ou .png sont autorisés")
        exit (84)  


def create_txt_pdf(raw, file_given):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    args = ["pdftotext", '-enc', 'UTF-8', file_given.format(SCRIPT_DIR), '-']
    res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = res.stdout.decode('utf-8')
    file_txt = file_given + ".txt"
    f = open(file_txt, "w")
    txt = output.lower()
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
    # print(factureDate)
############################################################################ DATE ##############################################################
############################################################################ NUMERO FACTURE ##############################################################
    numberFacture = get_number_facture(elements)
    # print(numberFacture)

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
        # print (montantTotal)


############################################################################ FACTURE  MAX obvious ##############################################################
############################################################################ MONTANT WITHOUT TAXS AND TVA ##############################################################


        tva_probable = []
        tva = 0
        tva_probable = all_results_tva(tva_probable, montantTotal)
        montantHt = 0
        compteur = 0

        montantHt,compteur = get_compteur(arrayTotalMontant2_convert, tva_probable, montantHt)
        tva = get_tva(montantHt, compteur, tva)

        # print(montantHt)
        # print(tva)

############################################################################ MONTANT WITHOUT TAXS AND TVA ##############################################################
#SI Il n'y a pas de signes distinctifs comme "500 $" on prend le plus grand nombre a virugle (sinon risque que le code postal passe avant)
    except Exception:
        print("Pas evident a retrouver")
        array_number = []

        for i in elements:
            i = i.replace(",", ".") 

            try:
                float(i)
                if (not i.isnumeric()):
                    array_number.append(float(i))
            except Exception:
                pass
        
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
