import requests
import json
 
from geopy.geocoders import Nominatim
import geocoder
 
try:
    from key import _KEY
except:
    _KEY = ''




class Model:
    def __init__(self):
        self.WEATHER_KEY = _KEY
         
       

    def get_currentLoc(self):
        g = geocoder.ip('me')
        print(g.latlng)
        geolocator = Nominatim(user_agent='myapplication')
        loc = geolocator.geocode(g.address)
        return loc


    def get_location(self,location):
        geolocator = Nominatim(user_agent='myapplication')
        loc = geolocator.geocode(location)
        return loc
        
    def get_weather_c(self, location):
        weather_key = self.WEATHER_KEY
       
        url = 'https://api.openweathermap.org/data/2.5/onecall'
        params = {'appid':  weather_key, 
            'lat': location.latitude, 
            'lon': location.longitude, 
            'units' : 'metric',
             }

        response = requests.get(url, params=params)
        return response.json()

    def get_weather_f(self, location):
        weather_key = self.WEATHER_KEY
       
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