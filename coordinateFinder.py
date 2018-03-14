from geopy.geocoders import Nominatim
from Read_data import read_json, read_pickle
import time

geolocator = Nominatim()
def add_coordinates(filename):
    print('getting results...')
    results = read_pickle(filename)
    print('results returned...')
    print(len(results))
    print(type(results))
    for key in results:
        a = results[key]
        print(key)
        for key1 in a:
            print(key1)
            print(type(a['address']))
            for key2 in a['address']:
                print(type(key2))
        #print(results[key])
        pass
        #i = results[key]
        #print(i)
        #address = i['address']
        #print(address)
        #print('next \n\n')
        #location = geolocator.geocode(address)
        #i['lon'] = location.latitude
        #i['lat'] = location.longitude
        #time.sleep(100)


if __name__ == "__main__":

    #location = geolocator.geocode("175 5th Avenue NYC")
    #print((location.latitude, location.longitude))
    #print(location.address)
    add_coordinates("analyzed_data/severity1_violation_percentage.pickle")
