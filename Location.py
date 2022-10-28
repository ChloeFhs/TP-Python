import forecast_tools as ft

class Location:
    def __init__(self, city_name, country_code):
        self.city = city_name
        self.country_code = country_code
        self.state =''
    
    def get_coordinates(self):
        base_url_geo = f"{ft.base_url}geo/1.0/direct?q={city_name},{country_code}&limit=5&appid={ft.API_key}"
        answer_geo = ft.requests.get(base_url_geo)
        json_loc = answer_geo.json()

        #Cas où la ville n'existe pas, on demande à l'utilisateur de rentrer une ville jusqu'à ce qu'elle existe
        while len(json_loc) == 0 :
            city_name = input("La ville que vous souhaitez n'existe pas. Entrez la ville\n")
            country_code = input("Entrez le code du pays (ex: FR, US...)\n")
            base_url_geo = f"{ft.base_url}geo/1.0/direct?q={city_name},{country_code}&limit=5&appid={ft.API_key}"
            answer_geo = ft.requests.get(base_url_geo)
            json_loc = answer_geo.json()


        #Si plusieurs résultats et villes dans différents états:
        if (len(json_loc) > 1) and ("state" in json_loc[0]) :

            if (json_loc[0]["state"] != json_loc[1]["state"]):
                state = []

                #on crée une liste de choix de "state" à proposer à l'utilisateur 
                for i in range (len(json_loc)):
                        state.append(json_loc[i]["state"])
                state_choosen = input(f"Veuillez précisez l'état parmi : {state} \n")

                #On relance la requête en précisant l'état recherché, et on limite la réponse à 1
                base_url_geo = f"{ft.base_url}geo/1.0/direct?q={self.city},{self.state},{self.country_code}&limit=1&appid={ft.API_key}"
                answer_geo = ft.requests.get(base_url_geo)
                json_loc = answer_geo.json()


        #Récupération des coordonnées 
        lat_searched = json_loc[0]['lat']
        lon_searched = json_loc[0]["lon"]


        # #Ajout au final json 
        # final_json["forecast_location"] = (f"{city_name}({country_code})")


        result = {"lat":lat_searched, "lon":lon_searched}
        return result