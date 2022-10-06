#!/bin/bash
# DSM/CS/DC O. Roulle recuperation grib AROME dans BDAP
# pour un run, une echeance, une hauteur et un parametre
# donnes en arguments du script
# la grille demandee est FRANGP0025
# le domaine geographique est delimite par :
# 46.5N 44N 4E et 8E (noter l'ordre qui peut 
# etre trompeur latN puis latS puis lonW puis lonE
# les valeurs de longitude et latitudes sont en
# milliemes de degres 
# membre PEAROME001 ex 
#UTEMP 6eme argument /home/mpma/henona/path     
if [ $# -ne 6 ]; then
  echo "Usage: $0 date AAAAMMJJHH echeance hauteur param"
  exit 1;
fi
# mode "verbeux"
set -vx
run=$1
echeance=$2
hauteur=$3
param=$4
membre=$5
grille=EURAT01
# pour unicite des fichiers et travail en parallele
suffixe=$(date +%s).$$
validite=$(opedates ${run} +${echeance}hours)
jour=${run:0:8}
UTEMP=$6
# pour creer sans erreur un repertoir et ses sous repertoires
#mkdir -p ${UTEMP}/${jour}
#Construction de la requete DAP3
echo "#RQST
#NFIC P-${param}-${hauteur}-m-${grille}-${run}-ECH-${echeance}.grb
#PARAM  ${param}
#MOD ${membre}
#Z_REF ${grille}
#T_LST ${echeance}
#D_LST ${run}0000
#L_TYP HAUTEUR
#L_LST ${hauteur}
#FORM BINAIRE
" > requete.${suffixe}

dap3_dev_date_ech requete.${suffixe}
rm requete.${suffixe}

if [ -f P-${param}-${hauteur}-m-${grille}-${run}-ECH-${echeance}.grb ]
then
  rm -f ${UTEMP}/Prevision-${param}-${hauteur}-m-${grille}-${run}-ECH-${echeance}.grb
  mv P-${param}-${hauteur}-m-${grille}-${run}-ECH-${echeance}.grb ${UTEMP}/Prevision-${param}-${hauteur}-m-${grille}-${run}-ECH-${echeance}.grb
fi
