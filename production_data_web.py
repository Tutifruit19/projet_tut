import xarray as xr
import numpy as np 
import os

list_dossier = os.listdir("/home/mpma/henona/recovery_data/temporaire")

def recup_ARO():
    list_data = []
    for x in list_dossier:
        if x[:10] == "PE_PEAROME":
            list_files = os.listdir("/home/mpma/henona/recovery_data/temporaire/"+x)
            membre = [x[:13]]
            for y in list_files:
                data = xr.open_dataset("/home/mpma/henona/recovery_data/temporaire/"+x+"/"+y)
                membre.append(data["t2m"].values[0][0][0])
        else:
            pass
        list_data.append(membre)
    return list_data

def recup_ARP():
    list_data = []
    for x in list_dossier:
        if x[:8] == "PE_PEARP":
            list_files = os.listdir("/home/mpma/henona/recovery_data/temporaire/"+x)
            membre = [x[:11]]
            for y in list_files:
                data = xr.open_dataset("/home/mpma/henona/recovery_data/temporaire/"+x+"/"+y)
                membre.append(data["t2m"].values[0][0][0])
        else:
            pass
        list_data.append(membre)
    return list_data


recup_ARO()