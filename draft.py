from requests import request
import requests


import requests
import json


#1 -DEMANDE USER CE QU'IL VEUT 
#Prompt user city and state
    #If no result => error handling
    #If One result only => no choice => next step
    #If several result => offer choice to user 



city_name = input("Entrez la ville")

country_code = input("Entrez le code du pays (ex: FR, US...")


API_key="fece147fbfe5d6faef2345aa1252676b"


base_url_geo = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit=5&appid={API_key}"


#2 - LECTURE/TRAITEMENT DE LA REPONSE 

answer_geo = requests.get(base_url_geo)

#Code de retour de la requête  
print(answer_geo)

#Json de réponse 
print(answer_geo.json())


#Boucle sur les résultats, dans State

#Proposition à l'utilisateur 

#Input user sur le choix final

#lancement de la requête forecast 