from requests import request
import requests


import requests
import json


#1 -DEMANDE USER CE QU'IL VEUT 
#Prompt user city and state
    #If no result => error handling
    #If One result only => no choice => next step
    #If several result => offer choice to user 



city_name = input("Entrez la ville\n")

country_code = input("Entrez le code du pays (ex: FR, US...)\n")


API_key="fece147fbfe5d6faef2345aa1252676b"


base_url_geo = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit=5&appid={API_key}"


#2 - LECTURE/TRAITEMENT DE LA REPONSE 

answer_geo = requests.get(base_url_geo)



json_loc = answer_geo.json()


#Cas où la ville n'existe pas, on demande à l'utilisateur de rentrer une ville jusqu'à ce qu'elle existe
while len(json_loc) == 0 :
    city_name = input("La ville que vous souhaitez n'existe pas. Entrez la ville\n")
    country_code = input("Entrez le code du pays (ex: FR, US...)\n")
    base_url_geo = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit=5&appid={API_key}"
    answer_geo = requests.get(base_url_geo)
    json_loc = answer_geo.json()


#Si plusieurs résultats, 
if len(json_loc) > 1:
    state = []

    #on crée une liste de choix de "state" à proposer à l'utilisateur 
    for i in range (len(json_loc)):
            state.append(json_loc[i]["state"])
    state_choosen = input(f"Veuillez précisez l'état parmi : {state} \n")

    #On relance la requête en précisant l'état recherché, et on limite la réponse à 1
    base_url_geo = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_choosen},{country_code}&limit=1&appid={API_key}"
    answer_geo = requests.get(base_url_geo)
    json_loc = answer_geo.json()

#Récupération des coordonnées 
lat_searched = json_loc[0]['lat']
lon_searched = json_loc[0]["lon"]




#2 - lancement de la requête forecast 

#route forecast (on oublie pas de mettre en celsius)
base_url_forecast =f"https://api.openweathermap.org/data/2.5/forecast?lat={lat_searched}&lon={lon_searched}&appid={API_key}&units=metric"

answer_forecast = requests.get(base_url_forecast)

forecast_json = answer_forecast.json()

#3 - Calculs sur les résultats

#Initialisation des variables 
compt=0
sum_min=0
sum_max =0

#Boucle sur les températures
for forecast_json["dt"] in  forecast_json["list"] :
    sum_min += forecast_json["dt"]["main"]["temp_min"]
    sum_max += forecast_json["dt"]["main"]["temp_max"]

    compt = compt+1


#Calcul des moyennes
average_min = sum_min / compt
average_max = sum_max / compt
print(f"Température moyenne minimale : {round(average_min,2)} \nTempérature moyenne maximale : {round(average_max,2)}")