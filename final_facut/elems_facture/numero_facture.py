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
    test = []
    parse1 = 4
    
    for i in range(len(elements)):
        if elements[i] == "numero" or elements[i] == "°" or elements[i] == "n°" or elements[i] == "n°:" or elements[i][0] == "n" and  elements[i][1] == "°":
            try:
              

                test.append(elements[i])
                test.append(elements[i+1])
                test.append(elements[i+2])
            except Exception:
                pass
        
        if elements[i] == "facture" or elements[i] ==  "facture :" and elements[i -1] == "de":
            try:
                # if i[1] == "/" and i[4] == "/" or i[3] == "/" or i[1] == "-" and i[4] == "-" or i[3] == "-" or i[1] == ":" and i[4] == ":" or i[3] == ":":
                #     print("mtn")
                #     test.append[elements[i+80]] #je le fais encore crash
                test.append(elements[i])
                test.append(elements[i+1])
                test.append(elements[i+2])
            except Exception:
                pass

    array_semi_ranged = []

    for i in range(len(test)): 
        if(len(test[i]) >= 5): 
            if (test[i][1] == "/" and test[i][3] == "/" or test[i][1] == ":" and test[i][3] == ":" or test[i][1] == "-" and test[i][3] == "-"):
                continue
            if (test[i][2] == "/" and test[i][4] == "/" or test[i][2] == ":" and test[i][4] == ":" or test[i][2] == "-" and test[i][4] == "-"):
                continue
            else:
                array_semi_ranged.append(test[i])

       
    last_array = []

    for elem in array_semi_ranged: 
        compteurint = 0

        if len(elem) > 6:
            for i in elem:
                try:  
                    int(i)
                    compteurint += 1
                except Exception:
                    pass
                if (len(elem) - compteurint < 5) or (elem[0] == 'n' and elem[1] == '°' and len(elem) > 6):
                    last_array.append(elem)

    if (len(last_array) == 0):
        return('')
    if (len(last_array[0]) < 4):
        result = last_array[0] + arrayResultNumeroFacture[1]
    else:
        result = last_array[0]
    return (result)       #on recupere le resultat



def FirstTabNumeroFacture(elem, test):
    compteurint = 0
    last_array = []

    if len(elem) > 6:
        if ((elem[2] == "/" and elem[5] == "/") or (elem[2] == "." and elem[5] == ".")or (elem[2] == "-" and elem[5] == "-")):
            return()


        for i in elem:
            try:  
                int(i)
                compteurint += 1
            except Exception:
                pass
            if (len(elem) - compteurint < 3) or (elem[0] == 'n' and elem[1] == '°' and len(elem) > 6):
                test.append(elem)
