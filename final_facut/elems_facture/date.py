
def get_facture_date(elements):
    unique = True
    factureDate = ""
    for i in elements:
        try:  
            if (i[2] == "/" and i[5] == "/" and unique == True):
                factureDate = i
                unique = False
        except Exception:
            pass
    return(factureDate)

