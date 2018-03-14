from geopy.geocoders import Nominatim
from Data_Minng_sofdesmp4 import *
from Read_data import *
import time

geolocator = Nominatim()
def add_coordinates(filename):
    print('works')
    results = read_json(filename)
    for i in results:
        print(i)
        address = i['address']
        location = geolocator.geocode(address)
        i['lon'] = location.latitude
        i['lat'] = location.longitude
        time.sleep(100)


if __name__ == "__main__":

    #location = geolocator.geocode("175 5th Avenue NYC")
    #print((location.latitude, location.longitude))
    #print(location.address)
    add_coordinates('analyzed_data/severity1_violation_percentage.txt')
