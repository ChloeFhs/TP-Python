import geoloc as geo
import requests
from datetime import date
import json


class Weather_Forecast:
    """Weather_Forecast is built with the following input parameters:

    city: string: the city of the desired location
    country_code: string: the country code of the desired location

    It contains the following methods:

    get_forecast()
        allows to call the API openweather and returns a forecast in JSON.

    get_min_max_temp()
        returns the minimum and the maximum temperature within entire forecast.

    get_detailed_forecast()
        calculates the specified values desired by teachers. Returns a list
        containing the "forecast_details".

    get_final_forecast()
        Creates the final JSON file containing details desired by teachers.
    """

    def __init__(self, city, country_code):
        self.location = geo.Location(city, country_code)
        self.coordinates = self.location.get_coordinates()
        self.final_json = {}
        self.API_key = "fece147fbfe5d6faef2345aa1252676b"
        self.base_url = "http://api.openweathermap.org/"

    def get_forecast(self):
        url_forecast = f"{self.base_url}data/2.5/forecast?lat={self.coordinates['lat']}&lon={self.coordinates['lon']}&appid={self.API_key}&units=metric"
        forecast = requests.get(url_forecast)
        if forecast.status_code != 200:
            raise Exception("Something went wrong....")
        return forecast.json()

    def get_min_max_temp(self):
        # On crée deux listes, l'une va récupérer toutes
        # les valeurs min et l'autre les max
        forecast = self.get_forecast()
        min_list = []
        max_list = []

        # On remplit les listes
        for i in range(0, len(forecast["list"])):
            min_list.append(forecast["list"][i]["main"]["temp_min"])
            max_list.append(forecast["list"][i]["main"]["temp_max"])

        return (min(min_list), max(max_list))

    def get_detailed_forecast(self):
        # Initialisation des variables
        forecast = self.get_forecast()
        sum_temp = 0
        measure_count = 0
        forecast_details = []
        day = (date.fromtimestamp(forecast["list"][0]["dt"]))

        # Bougeoe sur les températures
        for i in range(0, len(forecast["list"])):

            # Si le day est le même que celui traité,  cumul des températures
            # dans une variable et incrémentation du comptage de mesures
            if (day == (date.fromtimestamp(forecast["list"][i]["dt"]))):
                sum_temp += forecast["list"][i]["main"]["temp"]
                measure_count = measure_count + 1

            # Sinon, calcul de la valeur moyenne,
            # réinitialisation des variables et passage au jour d'après
            else:
                average_temp = round((sum_temp / measure_count), 1)

                # ajout de l'entrée dans le dictionnaire et
                # du dictionnaire dans la liste
                forecast_day = {"date": day.strftime("%Y-%m-%d"), "temp": average_temp, "measure_count": measure_count}
                forecast_details.append(forecast_day)

                # Le day prend la valeur du nouveau jour et
                # on remet les variables à la bonne valeur
                day = (date.fromtimestamp(forecast["list"][i]["dt"]))
                sum_temp = forecast["list"][i]["main"]["temp"]
                measure_count = 1

            # Pour le dernier measure_count,
            # il ne rentre jamais dans le else donc on l'ajoute ici
            if i == len(forecast["list"])-1:
                forecast_day = {"date": day.strftime("%Y-%m-%d"), "temp": average_temp, "measure_count": measure_count}
                forecast_details.append(forecast_day)

        return forecast_details

    def get_final_forecast(self):
        # Remplissage des entrées du dictionnaire "final_json"
        self.final_json["forecast_location"] = self.location.to_string()
        self.final_json["forecast_min_temp"] = self.get_min_max_temp()[0]
        self.final_json["forecast_max_temp"] = self.get_min_max_temp()[1]
        self.final_json["forecast_details"] = self.get_detailed_forecast()

        # Création du fichier JSON final
        with open(f'Forecast_{self.location.to_string()}.json', 'w', encoding="utf_8") as file:
            json.dump(self.final_json, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    city_name = input("Entrez la ville\n")
    country_code = input("Entrez le code du pays (ex: FR, US...)\n")
    forecast_wanted = Weather_Forecast(city_name, country_code)
    forecast_wanted.get_final_forecast()

    print(f"\nForecast for *** {forecast_wanted.location.to_string()} *** has been created.")
