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
            os.system("./recupPrevisionARPEGE_hauteur.sh "+run+" "+str(profondeur)+" 2 T "+membre+" /home/mpma/henona/recovery_data/"+path)
            os.system("grib_to_netcdf /home/mpma/henona/recovery_data/"+path+"/Prevision-"+param+"-"+hauteur+"-m-EURAT01-"+list_timerun[i]+"-ECH-"+str(list_echeance[i])+".grb -o /home/mpma/henona/recovery_data/"+path+"/Prevision-"+param+"-"+hauteur+"-m-EURAT01-"+list_timerun[i]+"-ECH-"+str(list_echeance[i])+".nc")

membres_ARP = ["PEARP000","PEARP001","PEARP002","PEARP003","PEARP004","PEARP005","PEARP006","PEARP007","PEARP008","PEARP009","PEARP010","PEARP011","PEARP012","PEARP013","PEARP014","PEARP015","PEARP016","PEARP017","PEARP018","PEARP019","PEARP020","PEARP021","PEARP022","PEARP023","PEARP024","PEARP025","PEARP026","PEARP027","PEARP028","PEARP029","PEARP030","PEARP031","PEARP032","PEARP033","PEARP034"]
for x in membres_ARP:
    recovery_data("2022100506","2022100318","T","2",x)