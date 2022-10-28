from abc import ABC


class Url(ABC) :
    def __init__(self, base_url, *args ):
        self.base_url = f"{base_url}"

class Url_Geo (Url):
    def __init__(self, base_url, city_name, country_code):
        super().__init__(base_url)
