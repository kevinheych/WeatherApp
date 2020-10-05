from matplotlib.path import Path
import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM
import cartopy.io.img_tiles as cimgt
import cartopy.feature as cfeature

from pyowm import OWM
from pyowm.tiles.enums import MapLayerEnum

try:
    from key import _KEY
except:
    _KEY = ''
 

class Map():
    
    def __init__(self):
         
        self.layer = 'clouds_new'


    def map(self, figure, layer):
        
        url = 'https://tile.openweathermap.org/map/' + layer +'/{z}/{x}/{y}.png?appid='+ _KEY  

        print(url)
        # Create a Stamen Terrain instance.
        weather_tile = cimgt.GoogleTiles(url=url)
    

        # Create a GeoAxes in the tile's projection.
        ax = figure.add_subplot(1,1,1, projection=weather_tile.crs)

        # Limit the extent of the map to a small longitude/latitude range
        ax.set_extent([100, 160, -5, -44])

        # Add the Stamen data at zoom level 8.
        ax.add_image(weather_tile, 1)
        ax.add_feature(cfeature.LAND)

        ax.coastlines(resolution='50m', color='black', linewidth=1)
        
        plt.title('Radar')
       
     
        return ax

    def update(self, axe, layer):
        axe.clear()
        
        url = 'https://tile.openweathermap.org/map/' + layer +'/{z}/{x}/{y}.png?appid='+ _KEY   

        print(url)
        # Create a Stamen Terrain instance.
        weather_tile = cimgt.GoogleTiles(url=url)
    
        axe.add_image(weather_tile, 1)
        
        return axe


if __name__ == '__main__':

    fig = plt.figure()
    map = Map()
    map.map(fig, "clouds_new")
    