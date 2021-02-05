def getFirstStripNumeroFacture(i, compteurNumeroFacture, arrayNumeroFacture):
    if (i == "facture" or "facture :"):
        compteurNumeroFacture += 1               
        if (compteurNumeroFacture >= 0):
                compteurNumeroFacture += 1
        if (compteurNumeroFacture > 2):   
                    compteurNumeroFacture = -1
        else:
            arrayNumeroFacture.append(i)


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


def get_number_facture(elements):
    compteurNumeroFacture = -1
    arrayNumeroFacture = []
    arrayResultNumeroFacture = []
    
    for i in elements:
        getFirstStripNumeroFacture(i, compteurNumeroFacture, arrayNumeroFacture) #On decoupe en un premier tableau

    for elem in arrayNumeroFacture: 
        FirstTabNumeroFacture(elem, arrayResultNumeroFacture)      #on parse le 2 nd tableau

    return (getResultNumeroFacture(arrayResultNumeroFacture))       #on recupere le resultat



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