#!/bin/sh


ftp -i -n proba.canevas.enm.meteo.fr <<eof
user proba probabilite2022
cd web/
put graph_test_T_*
quit
eof

