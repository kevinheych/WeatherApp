import requests
import json
from geopy.geocoders import Nominatim





class Model:
    def __init__(self):
         pass
       

    def get_location(self,location):
        geolocator = Nominatim(user_agent='myapplication')
        loc = geolocator.geocode(location)
        return loc
        
    def get_weather_c(self, location):
        weather_key = "7350831d27d44e16e6a543a8f49dbf81"
       
        url = 'https://api.openweathermap.org/data/2.5/onecall'
        params = {'appid':  weather_key, 
            'lat': location.latitude, 
            'lon': location.longitude, 
            'units' : 'metric',
             }

        response = requests.get(url, params=params)
        return response.json()

    def get_weather_f(self, location):
        weather_key = "7350831d27d44e16e6a543a8f49dbf81"
       
        url = 'https://api.openweathermap.org/data/2.5/onecall'
        params = {'appid':  weather_key, 
            'lat': location.latitude, 
            'lon': location.longitude, 
            'units' : 'imperial',
             }

        response = requests.get(url, params=params)
        return response.json()

    def get_weathertest(self):
        with open('weatherjson_testdata.json') as json_file:
            return json.load(json_file)




if __name__ == "__main__":
    geolocator = Nominatim(user_agent='myapplication')
    location = geolocator.geocode("Preston VIC ")
    #print(location.address) 

    address = location.address
    split = address.split(",")
    print(split[0], split[2]) 
    model = Model()
    #print(model.get_weather(location))