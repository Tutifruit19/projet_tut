import os
import datetime
from datetime import timedelta
import xarray as xr
import numpy as np
import os


def convert(str_time):
    format = '%Y%m%d%H'
    datetime_value = datetime.datetime.strptime(str_time, format)
    return datetime_value

def diff(datetime_1,datetime_2):
    days = ((convert(datetime_1)-convert(datetime_2)).days)*24
    hours = ((convert(datetime_1)-convert(datetime_2)).seconds)/3600
    return days+hours

def recovery_data_aro(echeance,run_debut,param,hauteur,membre):
    os.system("mkdir PE_"+membre+str(run_debut)+"_"+str(echeance)+"_"+str(param)+"_"+str(hauteur))
    path = "PE_"+membre+str(run_debut)+"_"+str(echeance)+"_"+str(param)+"_"+str(hauteur)
    #construction de la liste de date:
    delta = timedelta(hours=6)
    t = convert(run_debut)
    difference = diff(echeance,run_debut)
    list_timerun = [t.strftime('%Y%m%d%H')]
    list_echeance = [difference]
    while t < convert(echeance):
        t = t + delta
        difference = difference-6
        list_timerun.append(t.strftime('%Y%m%d%H'))
        list_echeance.append(difference)
    list_timerun.pop()
    list_echeance.pop()
    if len(list_timerun) == len(list_echeance):
        for i in range(len(list_timerun)):
            run = list_timerun[i]
            profondeur = list_echeance[i]
            os.system("./recupPrevisionAROME_hauteur.sh "+run+" "+str(profondeur)+" 2 T "+membre+" /home/mpma/henona/recovery_data/"+path)
            os.system("grib_to_netcdf /home/mpma/henona/recovery_data/"+path+"/Prevision-"+param+"-"+hauteur+"-m-EURW1S40-"+list_timerun[i]+"-ECH-"+str(list_echeance[i])+".grb -o /home/mpma/henona/recovery_data/"+path+"/Prevision-"+param+"-"+hauteur+"-m-EURW1S40-"+list_timerun[i]+"-ECH-"+str(list_echeance[i])+".nc")

def recovery_data_arp(echeance,run_debut,param,hauteur,membre):
    os.system("mkdir PE_"+membre+str(run_debut)+"_"+str(echeance)+"_"+str(param)+"_"+str(hauteur))
    path = "PE_"+membre+str(run_debut)+"_"+str(echeance)+"_"+str(param)+"_"+str(hauteur)
    #construction de la liste de date:
    delta = timedelta(hours=6)
    t = convert(run_debut)
    difference = diff(echeance,run_debut)
    list_timerun = [t.strftime('%Y%m%d%H')]
    list_echeance = [difference]
    while t < convert(echeance):
        t = t + delta
        difference = difference-6
        list_timerun.append(t.strftime('%Y%m%d%H'))
        list_echeance.append(difference)
    list_timerun.pop()
    list_echeance.pop()
    if len(list_timerun) == len(list_echeance):
        for i in range(len(list_timerun)):
            run = list_timerun[i]
            profondeur = list_echeance[i]
            os.system("./recupPrevisionARPEGE_hauteur.sh "+run+" "+str(profondeur)+" 2 T "+membre+" /home/mpma/henona/recovery_data/"+path)
            os.system("grib_to_netcdf /home/mpma/henona/recovery_data/"+path+"/Prevision-"+param+"-"+hauteur+"-m-EURAT01-"+list_timerun[i]+"-ECH-"+str(list_echeance[i])+".grb -o /home/mpma/henona/recovery_data/"+path+"/Prevision-"+param+"-"+hauteur+"-m-EURAT01-"+list_timerun[i]+"-ECH-"+str(list_echeance[i])+".nc")

def extraction_pt_grille(lat,lon,filename,path,cible):
    #Toulouse lat=43.5866 et lon=1.4605
    os.system("cdo -remapnn,lon="+lon+"/lat="+lat+" "+path+" "+cible+"/remap_"+filename)
    data = xr.open_dataset(cible+"/remap_"+filename)['t2m'].values
    print(data)

membres_PEARO = ["PEAROME000","PEAROME001","PEAROME002","PEAROME003","PEAROME004","PEAROME005","PEAROME006","PEAROME007","PEAROME008","PEAROME009","PEAROME010","PEAROME011","PEAROME012","PEAROME013","PEAROME014","PEAROME015","PEAROME016"]
for x in membres_PEARO:
    recovery_data_aro("2022101409","2022101215","T","2",x)

membres_ARP = ["PEARP000","PEARP001","PEARP002","PEARP003","PEARP004","PEARP005","PEARP006","PEARP007","PEARP008","PEARP009","PEARP010","PEARP011","PEARP012","PEARP013","PEARP014","PEARP015","PEARP016","PEARP017","PEARP018","PEARP019","PEARP020","PEARP021","PEARP022","PEARP023","PEARP024","PEARP025","PEARP026","PEARP027","PEARP028","PEARP029","PEARP030","PEARP031","PEARP032","PEARP033","PEARP034"]
for x in membres_ARP:
    recovery_data_arp("2022101406","2022101218","T","2",x)

os.system("mkdir temporaire")
list_files = os.listdir("/home/mpma/henona/recovery_data")
print(list_files)
for x in list_files:
    if x[:2] =='PE':
        list_nc = os.listdir("/home/mpma/henona/recovery_data/"+x)
        print(list_nc)
        os.system("mkdir temporaire/"+x)
        for y in list_nc:
            if y[-2:] =='nc':
                extraction_pt_grille("43.5866","1.4605",y,"/home/mpma/henona/recovery_data/"+x+"/"+y,"temporaire/"+x)
            else:
                pass
    else:
        pass
os.system("rm -r /home/mpma/henona/recovery_data/PE*")

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
ARP = recup_ARO()
output_ARO = sort(ARO)
output_ARP = sort(ARP)
making_output(output_ARO[0],"/home/mpma/henona/run_determiste_ARO.txt")
making_output(output_ARO[1],"/home/mpma/henona/Q_10_ARO.txt")
making_output(output_ARO[2],"/home/mpma/henona/Q_90_ARO.txt")
making_output(output_ARP[0],"/home/mpma/henona/run_determiste_ARP.txt")
making_output(output_ARP[1],"/home/mpma/henona/Q_10_ARP.txt")
making_output(output_ARP[2],"/home/mpma/henona/Q_90_ARP.txt")