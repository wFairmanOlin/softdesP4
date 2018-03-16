from geopy.geocoders import Nominatim
from Read_data import read_json, read_pickle
import time, pickle

geolocator = Nominatim()
def add_coordinates(filename):
    results = read_pickle(filename)
    limit = 0
    for i in results:
        print('num=', limit)
        address = results[i]['address']
        coordinates = results[i]['location']

        if len(coordinates) < 1:
            try:
                location = geolocator.geocode(address)
                if location is not None:
                    print(location.latitude, location.longitude)
                    results[i]['location'] = [location.latitude, location.longitude]
                else:
                    results[i]['location'] = [0,0]
            except:
                results[i]['location'] = [0,0]
                pass
            time.sleep (3)
        #if limit > 49:
        #    break
        limit += 1
    return results


def add_fake_coordinates(filename):

    results = read_pickle(filename)
    limit = 0
    for i in results:
        results[i]['lat'] = 42.2932 + limit*.001
        results[i]['lon'] = -71.2637
        limit += 1
    return results

if __name__ == "__main__":

    #location = geolocator.geocode("10901 sw 60th ave Miami 33156 Murica")
    #print((location.latitude, location.longitude))
    #print(location.address)
    #results = add_fake_coordinates("analyzed_data/severity1_violation_percentage.pickle")
    results = add_coordinates("analyzed_data/severity3_violation_percentage.pickle")

    #f = open("analyzed_data/severity1_violation_percentage.pickle", 'wb')
    #pickle.dump(retFile, f)
    with open("completeSeverity3.pickle", "wb") as handle:
        pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)