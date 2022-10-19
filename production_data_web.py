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
            list_data.append(membre)
        else:
            pass
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
            list_data.append(membre)
        else:
            pass
    return list_data


def sort(tab):
    for i in range(np.shape(tab)[0]):
        if tab[i][0] == "PE_PEAROME000":
            run_deterministe = tab[i][1:]
    Q_10 = []
    Q_90 = []
    run = []
    for j in range(1,np.shape(tab)[1]):
        for i in range(np.shape(tab)[0]):
            run.append(tab[i][j])
        Q_10.append(np.quantile(run,0.10))
        Q_90.append(np.quantile(run,0.90))
    return [run_deterministe,Q_10,Q_90]


def making_output(data,filename):
    file = open(filename,"a")
    for x in data:
        file.write(str(x))
        file.write("\n")


ARO = recup_ARO()
output = sort(ARO)
making_output(output[0],"/home/mpma/henona/run_determiste.txt")
making_output(output[1],"/home/mpma/henona/Q_10.txt")
making_output(output[2],"/home/mpma/henona/Q_90.txt")



