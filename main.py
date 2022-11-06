import forecast

city_name = input("Entrez la ville\n")
country_code = input("Entrez le code du pays (ex: FR, US...)\n")
forecast_wanted = forecast.Weather_Forecast(city_name, country_code)
forecast_wanted.get_final_forecast()
print(f"\nForecast for *** {forecast_wanted.location.to_string()} *** has been created.")
