import forecast_tools as ft

city_name = input("Entrez la ville\n")

country_code = input("Entrez le code du pays (ex: FR, US...)\n")

location = ft.get_location(city_name, country_code)

forecast_full = ft.get_forecast(location)

ft.get_min_max(forecast_full)

ft.get_forecast_details_by_day(forecast_full)


print (ft.final_json)
