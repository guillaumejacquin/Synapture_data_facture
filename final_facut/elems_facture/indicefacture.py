  
def number_indice(i, nb_indiceFacture):
    if i == "facture" or i == "facturé" or "facture :" or i == "factur" or i == "factures":
                nb_indiceFacture += 3
    if i == "total" or i == "tva" or i == "ttc" or  i == "iban" or i == "ban" or i == "siret" or i == "paiement" or i == "paiemen":
                nb_indiceFacture += 1

    return (nb_indiceFacture)



def printFactureOrNot(facture):
    if (facture >= 0 and  facture <= 200):
        print("il ne s'agit surement pas d'une facture")
        print("Nous sommes désolé, nous n'arrivons pas a determiner le type du fichier")
        return False
    
    if (facture > 201 and  facture <= 1000):
        print("il s'agit surement d'une facture")
        return True
  
    if (facture > 1001):
        print("il s'agit d'une facture")
        return True




def define_if_facture_or_not(text, file_given):
    source = ""
    source = give_source_name(file_given)

    elements = text.lower().split()
    nb_indiceFacture = 0

    for i in elements:
        nb_indiceFacture = number_indice(i, nb_indiceFacture)

    factureornot = printFactureOrNot(nb_indiceFacture)   #ICI JE DIS SI IL S AGIT D UNE FACTURE
    return (facture)


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


def give_source_name(file_given):
    if (file_given.endswith(".txt")):
        source = file_given

    else:
        source = file_given + ".txt"
    return (source)
