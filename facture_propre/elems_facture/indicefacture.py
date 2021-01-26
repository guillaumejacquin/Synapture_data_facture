  
def number_indice(i, nb_indiceFacture):
    if i == "facture" or i == "facturé" or "facture :" or i == "factur" or i == "factures":
                nb_indiceFacture += 3
    if i == "total" or i == "tva" or i == "ttc" or  i == "iban" or i == "ban" or i == "siret" or i == "paiement" or i == "paiemen":
                nb_indiceFacture += 1

    return (nb_indiceFacture)



def printFactureOrNot(facture):
    if (facture >= 0 and  facture <= 200):
        print("il ne s'agit surement pas d'une facture")
        print("Nous sommes désolé, nous n'arrivons pas a determiner le type du fichier")
        return False
    
    if (facture > 201 and  facture <= 1000):
        print("il s'agit surement d'une facture")
        return True
  
    if (facture > 1001):
        print("il s'agit d'une facture")
        return True
