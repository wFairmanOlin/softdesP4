from Read_data import read_json, read_pickle
from bokeh.colors import RGB
import time

def generate_dictionary(severityLevel, color):
    results = read_pickle(filename)
    colors = read_pickle('color_data/{}'.format(filename))
    data = dict(lat=[], lon=[], color=[], name=[])
    limit = 0
    for name in results:
        print(results[name]['location'][0])
        data['lat'].append(results[name]['location'][0])
        data['lon'].append(results[name]['location'][1])
        data['color'].append(colors[name]['color'])
        data['name'].append(name)
        # if limit > stop:
        #     break
        limit += 1
    return data


# def generate_dictionary(filename='word', color='red', stop=49):
#     results = read_pickle(filename)
#     data = dict(lat=[], lon=[], color=[])
#     limit = 0
#     for name in results:
#         data['lat'].append(results[name]['lon'])
#         data['lon'].append(results[name]['lat'])
#         data['color'].append(RGB(255,0,0))
#         if limit > stop:
#             break
#         limit += 1
#     return data


if __name__ == "__main__":
    pass
    #generate_dictionary('completeSeverity1.pickle', color='red')
