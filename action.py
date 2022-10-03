#!/usr/bin/python3
import web 

@web.app
def action(selection_parametre ="T2m",selection_modele="EPS",selection_pt="Toulouse"):
	if (selection_parametre =="T2m"):
		return(web.vue("test.html"))
