from matplotlib.path import Path
import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM
import cartopy.io.img_tiles as cimgt
import cartopy.feature as cfeature

from pyowm import OWM
from pyowm.tiles.enums import MapLayerEnum

from matplotlib.offsetbox import AnchoredText
from matplotlib.transforms import offset_copy

try:
    from key import _KEY
except:
    _KEY = ''
 

class Map():
    
    def __init__(self):
         
        self.layer = 'clouds_new'


    def map(self, figure, layer, lon, lat):
        
        url = 'https://tile.openweathermap.org/map/' + layer +'/{z}/{x}/{y}.png?appid='+ _KEY  

        print(url)
        # Create a tile instance
        weather_tile = cimgt.GoogleTiles(url=url)
    

        # Create a GeoAxes in the tile's projection.
        ax = figure.add_subplot(1,1,1, projection=weather_tile.crs)

        # Limit the extent of the map to a small longitude/latitude range
        #[longLeft,longRight,latTop,latBot]
        #ax.set_extent([100, 160, -5, -44]) 
        lon_cen = lon
        lat_cen = lat

        longLeft = lon_cen - 10
        longRight = lon_cen + 10
        latTop = lat_cen - 5 
        lateBottom = lat_cen + 5
        ax.set_extent([longLeft,longRight,latTop,lateBottom])
        #marker
        

        # Add the tile data at zoom level 8.
        ax.add_image(weather_tile, 4)
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.COASTLINE)
 
         
      
        # Add a text annotation for the license information to the
        # the bottom right corner.
    
        text = AnchoredText( "Source: OpenWeatherMap 1.0",
                            loc=4, prop={'size': 8}, frameon=True)
        ax.add_artist(text)
      
        ax.plot(145.01667, -37.75,  markersize=10, marker='o', color='red') 
         
            
       
     
        return ax

    def update(self, axe, layer):
        axe.clear()
        
        url = 'https://tile.openweathermap.org/map/' + layer +'/{z}/{x}/{y}.png?appid='+ _KEY   

        print(url)
        # Create a Stamen Terrain instance.
        weather_tile = cimgt.GoogleTiles(url=url)
    
        axe.add_image(weather_tile, 4)
        
        return axe


if __name__ == '__main__':

    fig = plt.figure()
    map = Map()
    lat = -37.8142176
    lon = 144.9631608
    map.map(fig, "clouds_new", lon, lat)
    plt.show()
 
    