from geopy.geocoders import Nominatim
from Data_Minng_sofdesmp4 import *




if __name__ == "__main__":
    result = run('mayorsfoodcourt.csv', 'Boston')

    geolocator = Nominatim()
    location = geolocator.geocode("175 5th Avenue NYC")
    print((location.latitude, location.longitude))
    print(location.address)
