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
    
    for i in elements:
        
        getFirstStripNumeroFacture(i, compteurNumeroFacture, arrayNumeroFacture) #On decoupe en un premier tableau
        

        if (parse1 < 2):
            test.append(i)
            parse1 + 1

        if("numero" in i):
                        

                    test.append(i)
                    parse1 = 1
        if ('°' in i):
            test.append(i)
            parse1 = 1
         #on parse le 2 nd tableau
    last_array = []
    # print(test)
    for elem in test: 
        compteurint = 0

        if len(elem) > 6:
            if ((elem[2] == "/" and elem[5] == "/") or (elem[2] == "." and elem[5] == ".")):
                pass


            for i in elem:
                try:  
                    int(i)
                    compteurint += 1
                except Exception:
                    pass
                if (len(elem) - compteurint < 3) or (elem[0] == 'n' and elem[1] == '°' and len(elem) > 6):
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
