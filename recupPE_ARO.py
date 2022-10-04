import os

def recovery_data(echeance,run_debut,param,hauteur):
    os.system("mkdir PE-ARO_"+str(echeance)+"_"+str(param)+"_"+str(hauteur)+"_"+str(profondeur))
    path = "PE-ARO_"+str(echeance)+"_"+str(param)+"_"+str(hauteur)+"_"+str(profondeur)
    reseaux = ["0300","0900","1500","2100"]
    for i in range(echeance):
        os.system("./recupPrevisionAROME_hauteur.sh ")
