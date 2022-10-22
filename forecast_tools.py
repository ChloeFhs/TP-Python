import string
import requests
from datetime import date



API_key="fece147fbfe5d6faef2345aa1252676b"
base_url="http://api.openweathermap.org/"
final_json={}

def get_location(city_name: string, country_code: string,):
    
    base_url_geo = f"{base_url}geo/1.0/direct?q={city_name},{country_code}&limit=5&appid={API_key}"
    answer_geo = requests.get(base_url_geo)
    json_loc = answer_geo.json()

    #Cas où la ville n'existe pas, on demande à l'utilisateur de rentrer une ville jusqu'à ce qu'elle existe
    while len(json_loc) == 0 :
        city_name = input("La ville que vous souhaitez n'existe pas. Entrez la ville\n")
        country_code = input("Entrez le code du pays (ex: FR, US...)\n")
        base_url_geo = f"{base_url}geo/1.0/direct?q={city_name},{country_code}&limit=5&appid={API_key}"
        answer_geo = requests.get(base_url_geo)
        json_loc = answer_geo.json()


    #Si plusieurs résultats et villes dans différents états:
    if (len(json_loc) > 1) and (json_loc[0]["state"] != json_loc[1]["state"]):

        state = []

        #on crée une liste de choix de "state" à proposer à l'utilisateur 
        for i in range (len(json_loc)):
                state.append(json_loc[i]["state"])
        state_choosen = input(f"Veuillez précisez l'état parmi : {state} \n")

        #On relance la requête en précisant l'état recherché, et on limite la réponse à 1
        base_url_geo = f"{base_url}geo/1.0/direct?q={city_name},{state_choosen},{country_code}&limit=1&appid={API_key}"
        answer_geo = requests.get(base_url_geo)
        json_loc = answer_geo.json()

    #Récupération des coordonnées 
    lat_searched = json_loc[0]['lat']
    lon_searched = json_loc[0]["lon"]


    #Ajout au final json 
    final_json["forecast_location"] = (f"{city_name}({country_code})")


    result = {"lat":lat_searched, "lon":lon_searched}
    return result



def get_forecast(location: dict):
    lat = location["lat"]
    lon = location ["lon"]
    url_forecast =f"{base_url}data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=metric"
    answer = requests.get(url_forecast)
    if answer.status_code != 200 :
        raise Exception("Something went wrong")
    return answer.json()


def get_forecast_details_by_day(forecast_json):
    #Initialisation des variables 
    sum_temp=0        
    measure_count=0
    forecast_details=[]
    day = (date.fromtimestamp(forecast_json["list"][0]["dt"]))


    #Boucle sur les températures
    for i in range (0, len(forecast_json["list"])):

        #Si le day est le même que celui traité,  cumul des températures dans une variable et incrémentation du comptage de mesures
        if (day == (date.fromtimestamp(forecast_json["list"][i]["dt"]))):
            sum_temp += forecast_json["list"][i]["main"]["temp"]
            measure_count = measure_count +1

        #Sinon, calcul de la valeur moyenne, réinitialisation des variables et passage au jour d'après
        else:
            average_temp = round((sum_temp / measure_count),1)

            #ajout de l'entrée dans le dictionnaire et du dictionnaire dans la liste
            forecast_day = {"date = ": day.strftime("%Y-%m-%d"), "temp" : average_temp,"measure_count" : measure_count}
            forecast_details.append(forecast_day)

            #Le day prend la valeur du nouveau jour et on remet les variables à la bonne valeur
            day=(date.fromtimestamp(forecast_json["list"][i]["dt"]))
            sum_temp=  forecast_json["list"][i]["main"]["temp"]
            measure_count= 1


        #Pour le dernier measure_count, il ne rentre jamais dans le else donc on l'ajoute ici 
        if i == len(forecast_json["list"])-1:
            forecast_day = {"date ": day.strftime("%Y-%m-%d"), "temp" : average_temp,"measure_count" : measure_count}
            forecast_details.append(forecast_day)

    final_json["forecast_details"]=forecast_details
    return forecast_details


def get_min_max(forecast_json):
    #On crée deux listes, l'une va récupérer toutes les valeurs min et l'autre les max
    min_list=[]
    max_list=[]

    #On remplit les listes
    for i in range (0, len(forecast_json["list"])):
       min_list.append(forecast_json["list"][i]["main"]["temp_min"])
       max_list.append(forecast_json["list"][i]["main"]["temp_max"])

    #Ajout au final json des min et max 
    final_json["forecast_min_temp"] = min(min_list)
    final_json["forecast_max_temp"] = max(max_list)