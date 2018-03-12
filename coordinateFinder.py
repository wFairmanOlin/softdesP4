from geopy.geocoders import Nominatim
from data_Mining_sofdesmp4.py import *


result = run('mayorsfoodcourt.csv', 'Boston')

geolocator = Nominatim()
location = geolocator.geocode("175 5th Avenue NYC")
print((location.latitude, location.longitude))
print(location.address)
