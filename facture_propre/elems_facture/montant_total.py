import sys

def getElementsTotalFacture(elem, i, arrayTotalMontant1):
    if (elem == "montant" or elem == "montant :" or elem == "payer :" or elem == "montant:"  or elem == "total" or elem == "total :" or elem == "total:" or elem == "euros" or elem == "dollars"):
        arrayTotalMontant1.append(elem)
        print("yes")
        
    try:
        float(elem)
        arrayTotalMontant1.append(elem)
    except Exception:
        pass


    return (arrayTotalMontant1)


def GetObviousELementsTotalFacture(elem, i, arrayTotalMontant2):

    for x in elem[i]:
        if (x == "€" or x == "euros" or x == "dollars" or x == "$" ):
            arrayTotalMontant2.append(elem[i])

    if (elem[i] == "€" or elem[i] == "euros" or elem[i] == "dollars" or elem[i] == "$"):
            arrayTotalMontant2.append(elem[i - 1])


    return(arrayTotalMontant2)


def check_price(source, arrayTotalMontant2, tmp):
    if (not source.endswith(".txt")):
        source = tmp + ".txt"


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




def convert_symbols(arrayTotalMontant2, arrayTotalMontant2_convert):  #convertit pour trasnfortmer en float
    for i in arrayTotalMontant2:
        conversion = i.replace(",", ".") 
        conversion2 = conversion.replace('€', ' ')
        conversion3 = conversion2.replace('$', ' ')

        arrayTotalMontant2_convert.append(conversion3)

    return (arrayTotalMontant2_convert)


def str_to_float_montant_total(i, range_array_obviouse_elem, arrayTotalMontant2_convert):
    for i in range(0, range_array_obviouse_elem): 
        try:
            arrayTotalMontant2_convert[i] = float(arrayTotalMontant2_convert[i]) 
    
        except Exception:
            arrayTotalMontant2_convert[i] = 0

    return(arrayTotalMontant2_convert)




def remove_useless_numbers(arrayTotalMontant2_convert, array_montant_societe):
    max_array = max(arrayTotalMontant2_convert)

    if (max_array == 0):
         print(max_array[1])
    try:
        if (max_array == float(array_montant_societe[0])):
            arrayTotalMontant2_convert.remove(max_array)
    except Exception:
        pass


    return (arrayTotalMontant2_convert)

