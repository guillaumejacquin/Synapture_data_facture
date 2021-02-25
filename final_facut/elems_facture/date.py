
def get_facture_date(elements):
    unique = True
    factureDate = ""
    for i in elements:
        try:  
            if (i[2] == "/" and i[5] == "/" and unique == True) or (i[2] == "-" and i[5] == "-" and unique == True):
                factureDate = i
                unique = False
        except Exception:
            pass
    return(factureDate)


def get_facture_if_date_is_digit(elements):
    unique = True
    compteur = 0
    numero1 = ''
    numero2 = ''
    numero3 = ''

    for i in elements:
        if (i == "janvier" or i == "février" or i == "fevrier" or i == "mars" or i == "avril" or
        i == "mai" or i == "juin" or i == "juillet" or i == "aout" or i == "août" or i == "septembre" 
        or i == "octobre" or i == "novembre" or i == "décembre" or i == "decembre" and unique == True):
            unique = False
            try:
                numero2 = elements[compteur]
                numero3 = elements[compteur + 1]
                numero1 =  elements[compteur - 1]
            except Exception:
                pass

        
        compteur += 1
    date = numero1 + numero2 + numero3
    return (date)
