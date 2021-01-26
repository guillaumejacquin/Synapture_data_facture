
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