import requests


class Location:
    """This class creates a location. A location is built
    with a city and a country code."""

    def __init__(self, city_name, country_code):
        self.city = city_name
        self.country_code = country_code
        self.state = ''
        self.API_key = "fece147fbfe5d6faef2345aa1252676b"
        self.base_url = "http://api.openweathermap.org/"

    def get_coordinates(self):
        """The method get_coordinates() returns a dictionnary containing the
        latitude ["lat"] and longitude ["lon"] of the location. """

        base_url_geo = f"{self.base_url}geo/1.0/direct?q={self.city},{self.country_code}&limit=5&appid={self.API_key}"
        answer_geo = requests.get(base_url_geo)
        json_loc = answer_geo.json()

        # Cas où la ville n'existe pas, on demande à l'utilisateur
        # de rentrer une ville jusqu'à ce qu'elle existe
        while len(json_loc) == 0:
            self.city = input("La ville que vous souhaitez n'existe pas. Entrez la ville\n")
            self.country_code = input("Entrez le code du pays (ex: FR, US...)\n")
            base_url_geo = f"{self.base_url}geo/1.0/direct?q={self.city},{self.country_code}&limit=5&appid={self.API_key}"
            answer_geo = requests.get(base_url_geo)
            json_loc = answer_geo.json()

        # Si plusieurs résultats et villes dans différents états:
        if (len(json_loc) > 1) and ("state" in json_loc[0]):

            if (json_loc[0]["state"] != json_loc[1]["state"]):
                list_state = []

                # on crée une liste de choix de "state"
                # à proposer à l'utilisateur
                for i in range(len(json_loc)):
                    list_state.append(json_loc[i]["state"])
                self.state = input(f"Veuillez précisez l'état parmi : {list_state} \n")

                # On relance la requête en précisant l'état recherché, et on limite la réponse à 1
                base_url_geo = f"{self.base_url}geo/1.0/direct?q={self.city},{self.state},{self.country_code}&limit=1&appid={self.API_key}"
                answer_geo = requests.get(base_url_geo)
                json_loc = answer_geo.json()

        # Récupération des coordonnées
        lat_searched = json_loc[0]['lat']
        lon_searched = json_loc[0]["lon"]

        # Ajout au final json
        # final_json["forecast_location"] = (f"{city_name}({country_code})")

        result = {"lat": lat_searched, "lon": lon_searched}
        return result

    def to_string(self):
        '''Returns a string describing the location'''
        
        if len(self.state) > 0:
            return f"{self.city}, {self.state} ({self.country_code})"
        else:
            return f"{self.city} ({self.country_code})"
