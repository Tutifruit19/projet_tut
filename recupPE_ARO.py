import os
import datetime
from datetime import timedelta

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

def recovery_data(echeance,run_debut,param,hauteur):
    os.system("mkdir PE-ARO_"+str(run_debut)+"_"+str(echeance)+"_"+str(param)+"_"+str(hauteur))
    path = "PE-ARO_"+str(run_debut)+"_"+str(echeance)+"_"+str(param)+"_"+str(hauteur)
    #construction de la liste de date:
    delta = timedelta(hours=6)
    t = convert(run_debut)
    difference = diff(echeance,run_debut)
    list_timerun = [t.strftime('%Y%m%d%H%M')]
    list_echeance = [difference]
    while t < convert(echeance):
        t = t + delta
        difference = difference-6
        list_timerun.append(t.strftime('%Y%m%d%H%M'))
        list_echeance.append(difference)
    print(list_timerun)
    print(list_echeance)
    

    

recovery_data("2022100509","2022100315","T","2")