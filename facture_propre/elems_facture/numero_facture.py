
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