import os
import datetime
from datetime import timedelta

from matplotlib.cbook import ls_mapper

def convert(str_time):
    format = '%Y%m%d%H'
    datetime_value = datetime.datetime.strptime(str_time, format)
    return datetime_value

#delta = timedelta(hours=4)
#print(((convert("2022100421")-convert("2022100115")).seconds)/3600) 
#print((convert("2022100421")-convert("2022100115")).days) 

def diff(datetime_1,datetime_2):
    days = ((convert(datetime_1)-convert(datetime_2)).days)*24
    hours = ((convert(datetime_1)-convert(datetime_2)).seconds)/3600
    return days+hours

def recovery_data(echeance,run_debut,param,hauteur,membre):
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

membres_PEARO = ["PEAROME000","PEAROME001","PEAROME002","PEAROME003","PEAROME004","PEAROME005","PEAROME006","PEAROME007","PEAROME008","PEAROME009","PEAROME010","PEAROME011","PEAROME012","PEAROME013","PEAROME014","PEAROME015","PEAROME016"]
for x in membres_PEARO:
    recovery_data("2022100409","2022100315","T","2",x)