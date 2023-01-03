#!/bin/sh


ftp -i -n proba.canevas.enm.meteo.fr <<eof
user proba probabilite2022
cd web/
put graph_test_RR_Toulouse.html
put graph_test_RR_Bordeaux.html
put graph_test_RR_Strasbourg.html
put graph_test_RR_Lyon.html
put graph_test_RR_Aix.html
put graph_test_RR_Rennes.html
put graph_test_RR_Lille.html
put graph_test_RR_Paris.html
quit
eof