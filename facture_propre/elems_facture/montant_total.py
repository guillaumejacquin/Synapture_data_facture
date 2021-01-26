import sys
source = sys.argv[2] + ".txt"

def getElementsTotalFacture(elem, i, arrayTotalMontant1):
    if (i == "montant" or i == "montant :" or i == "montant:"  or i == "total" or i == "total :" or i == "total:"):
        arrayTotalMontant1.append(i)
        
    return (arrayTotalMontant1)


def GetObviousELementsTotalFacture(elem, i, arrayTotalMontant2):

    for x in elem[i]:
        if (x == "€" or x == "euros" or x == "dollars" or x == "$" ):
            arrayTotalMontant2.append(elem[i])

    if (elem[i] == "€" or elem[i] == "euros" or elem[i] == "dollars" or elem[i] == "$"):
            arrayTotalMontant2.append(elem[i - 1])


    return(arrayTotalMontant2)


def check_price(source, arrayTotalMontant2):
    non = False
    compteur = 0
    tmp = ""

    array_result = []
    with open(source) as f:
        for i, w in enumerate(f.read().split()):
            
            if (non == True):
                compteur +=1

                if (compteur >= 12):
                    non = False
                    pass
                try:
                    if (w == "€" or w == "euros" or w == "dollars" or w == "$" and float(tmp)):
                        tmp = tmp.replace(",", ".")
                        array_result.append(tmp)
                except Exception:
                    pass

            if w == "capital":
                non = True
                compteur = 0
            tmp = w

    return (array_result)


