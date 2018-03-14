import matplotlib
import matplotlib.cm as cm
import simplejson as json
import pickle

minima = 0
maxima = 100
norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
mapper = cm.ScalarMappable(norm=norm, cmap=cm.CMRmap)


def read_json(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)


def colormap(filename):
    data = read_json(filename)
    for restaurant in data:
        datapoint = data[restaurant]['percentage']
        R, G, B, a = mapper.to_rgba(datapoint)
        data[restaurant]['color'] = R, G, B
    return data


def run():
    violation_color = colormap('analyzed_data/restaurant_violation_percentage.txt')
    # print(violation_color)
    severity1_color = colormap('analyzed_data/severity1_violation_percentage.txt')
    severity2_color = colormap('analyzed_data/severity2_violation_percentage.txt')
    severity3_color = colormap('analyzed_data/severity3_violation_percentage.txt')
    return violation_color, severity1_color, severity2_color, severity3_color


if __name__ == "__main__":
    result = run()

    # save violation percentage dictionary as a txt
    with open("color_data/restaurant_violation_percentage.txt", "w") as output:
        output.write(json.dumps(result[0]))

    # save violation percentage dictionary as .pickle
    with open('color_data/restaurant_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[0], handle, protocol=pickle.HIGHEST_PROTOCOL)
        #
        # # save severity1 percentage dictionary as a txt
        # with open("color_data/severity1_violation_percentage.txt", "w") as output:
        #     output.write(json.dumps(result[1]))
        #
        # # save severity1 percentage dictionary as .pickle
        # with open('color_data/severity1_violation_percentage.pickle', 'wb') as handle:
        #     pickle.dump(result[1], handle, protocol=pickle.HIGHEST_PROTOCOL)
        #
        # # save severity2 percentage dictionary as a txt
        # with open("color_data/severity2_violation_percentage.txt", "w") as output:
        #     output.write(json.dumps(result[2]))
        #
        # # save severity2 percentage dictionary as .pickle
        # with open('color_data/severity2_violation_percentage.pickle', 'wb') as handle:
        #     pickle.dump(result[2], handle, protocol=pickle.HIGHEST_PROTOCOL)
        #
        # # save severity3 percentage dictionary as a txt
        # with open("color_data/severity3_violation_percentage.txt", "w") as output:
        #     output.write(json.dumps(result[3]))
        #
        # # save severity3 percentage dictionary as .pickle
        # with open('color_data/severity3_violation_percentage.pickle', 'wb') as handle:
        #     pickle.dump(result[3], handle, protocol=pickle.HIGHEST_PROTOCOL)
