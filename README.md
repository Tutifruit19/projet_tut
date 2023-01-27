## Version 1 du code pour l'historique de probabilité prévue en un point.

    * Auteur: Henon Aurélien
    * date: Janvier 2023
    * Projet tutoré avec Joly Bruno et Chabot Etienne

# Description de la partie backend:

1. **Programmes nécéssaires**:
    * Paramètre T2m:
        - Routine python principal: *prod_data.py*
        - Script shell pour interroger la BDAP: *recupPrevisionAROME_hauteur.sh*, *recupPrevisionARPEGE_hauteur.sh*
        - Script shell pour envoyer la sortie vers le serveur web: *ftp_script.sh*
    * Paramètre RR:
        - Routine python principal: *prod_data_RR.py*
        - Script shell pour interroger la BDAP: *recupPrevisionAROME_sol.sh*, *recupPrevisionARPEGE_sol.sh*
        - Script shell pour envoyer la sortie vers le serveur web: *ftp_script_RR.sh*

2. **Fonctionnement général de la routine python**
    Dans tout ce qui suit on décrira uniquement le paramètre T2m pour évider la redondance mais il seulement quelques variations avec 
    * ***Description des fonctions:***
        - *convert*: Permet de convertir une date sous forme de str en type datetime
        - *diff*:
            input: 
                datetime1, datetime2. Type: str
            output: 
                La différence entre les deux dates. Type: datetime
        - *recovery_data_aro*: Permet de récupérer les des datas d'arome dans la BDAP. ***Besoin du script recupPrevisionAROME_hauteur.sh***
            input: 
                echeance: échéance voulu pour le produit. Type str
                run_debut: date de début du produit. La fonction récupère de la date de debut à l'échéance tout les runs (toutes les 6h). Type: str
                param: Le paramètre souhaité ici la T. Type str
                hauteur: Ici la hauteur souhaitée pour le paramètre ici 2. Type: str
                membre: Le membre souhaité par exemple PEAROME012. Type: str
            output:
                list_timerun_aro: Une liste avec toutes les dates des runs aromes. Type: list
                Procédure qui crée aussi des fichiers avec tout les fichier netcdf pour tout les membres et tout les runs pour l'échéance donnée.
        - *recovery_data_arp*: Même chose que pour *recovery_data_aro* mais avec arpège. ***Besoin du script recupPrevisionARPEGE_hauteur.sh***
        - *extraction_pt_grille*: Fonction qui permet de creer un nouveau fichier netcdf à partir d'un autre avec seulement un point de grille dedans. Extraction du pt de grille voulu.
            input:
                lat:
                lon:
                filename:
                path:
                cible:
            output:
                Crée des fichiers netcdf avec seulement 1 pt de grille


# Description de la partie frontend: