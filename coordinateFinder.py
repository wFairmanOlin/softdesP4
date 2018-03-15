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
    for i in results:
        print('num=', i)
        address = results[i]['address']
        print(address)
        location = geolocator.geocode(address)
        if location is not None:
            results[i]['lon'] = location.latitude
            results[i]['lat'] = location.longitude
        else:
            results[i]['lon'] = 0
            results[i]['lat'] = 0
        time.sleep (2000)
    return results
        #time.sleep(100)


if __name__ == "__main__":

    #location = geolocator.geocode("10901 sw 60th ave Miami 33156 Murica")
    #print((location.latitude, location.longitude))
    #print(location.address)
    results = add_coordinates("analyzed_data/severity1_violation_percentage.pickle")

    with open("analyzed_data/completeSeverity1.pickle", "w") as handle:
        pickle.dump(result[0], handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(results)
