
def tva_array_possible(tva_probable, max_array):
    tva_probable.append(round((max_array / 1.2), 2))
    tva_probable.append(round((max_array / 1.1), 2))
    tva_probable.append(round((max_array / 1.155), 2))
    tva_probable.append(round((max_array / 1.11), 2))
    return (tva_propable)

def get_tva(montantHt, compteur, tva):
    if montantHt != 0.0:
        if (compteur == 0):
            tva = 20.0
        elif (compteur == 1):
            tva = 10.0
        elif (compteur == 2):
            tva = 5.5
        elif (compteur == 3):
                tva = 2.55
        elif (compteur == 4):
                tva = 2.1
        else:
            compteur = "rip"
    return(tva)

def define_tva(arrayTotalMontant2_convert, tva_probable, montantHt):
        compteur = 0
        find = False

        for i in arrayTotalMontant2_convert:
            compteur = 0
            for j in tva_probable:
                if i == j:
                    montantHt = i
                    find = True
                    break
                compteur += 1

            if (find == True):
                break
        return (compteur)


def all_results_tva(tva_probable, montantTotal):
    tva_probable.append(round((montantTotal / 1.2), 2))
    tva_probable.append(round((montantTotal / 1.1), 2))
    tva_probable.append(round((montantTotal / 1.155), 2))
    tva_probable.append(round((montantTotal / 1.179), 2))

    return(tva_probable)

def get_compteur(arrayTotalMontant2_convert, tva_probable, montantHt):
    compteur = 0
    find = False
    for i in arrayTotalMontant2_convert:
        compteur = 0
        for j in tva_probable:
                if i == j:
                    montantHt = i
                    find = True
                    break
                compteur += 1

        if (find == True):
                break
   
    return(montantHt,compteur)


def get_tva_complicated(montantTotal, array_number):
        tva_probable = []
        tva = 0
        tva_probable = all_results_tva(tva_probable, montantTotal)
        array_number = list(dict.fromkeys(array_number))

        array_number.sort()
        possible_tva = array_number[-2]

        array_possible_tva = [round(possible_tva -0.01, 2), round(possible_tva, 2), round(possible_tva +0.01, 2)]

        montantHt = 0
        compteur = 0

        montantHt,compteur = get_compteur(array_possible_tva, tva_probable, montantHt)
        tva = get_tva(montantHt, compteur, tva)

        return (montantHt,tva)