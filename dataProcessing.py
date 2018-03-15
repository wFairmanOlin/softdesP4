from Read_data import read_json, read_pickle
from bokeh.colors import RGB
import time

def generate_dictionary(filename='word', color='red', stop=49):
    results = read_pickle('analyzed_data/1_50Severity1.pickle')
    data = dict(lat=[], lon=[], color=[])
    limit = 0
    for name in results:
        data['lat'].append(results[name]['lat'])
        data['lon'].append(results[name]['lon'])
        data['color'].append(RGB(255,0,0))
        if limit > stop:
            break
        limit += 1
    return data



if __name__ == "__main__":
    results = read_pickle('analyzed_data/testSeverity1.pickle')
    data = dict(lat=[], lon=[], color='red')

    for name in results:
        print(results[name])
        data['lat'].append(results[name]['lat'])
        data['lon'].append(results[name]['lon'])
    print(data)
