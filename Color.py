import matplotlib
import matplotlib.cm as cm
import simplejson as json
import pickle
from bokeh.colors import RGB

minima = 0
maxima = 100
norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
mapper = cm.ScalarMappable(norm=norm, cmap=cm.CMRmap)


def read_json(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)

def remap_interval(val,
                   input_interval_start,
                   input_interval_end):
    """Remap a value from one interval to another.

    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].

    Args:
        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values

    Returns:
        The value remapped from the input to the output interval
    """
    percentage = (val - input_interval_start)/(input_interval_end - input_interval_start)
    return percentage*255


def colormap(filename):
    data = read_json(filename)
    for restaurant in data:
        datapoint = data[restaurant]['percentage']
        R, G, B, a = mapper.to_rgba(datapoint)
        red = remap_interval(R,0,1)
        green = remap_interval(G,0,1)
        blue = remap_interval(B,0,1)
        data[restaurant]['color'] = (red, green, blue)
        #print(data[restaurant]['color'])
    return data

def run():
    violation_color = colormap('analyzed_data/restaurant_violation_percentage.txt')
    #print(violation_color)

    severity1_color = colormap('analyzed_data/severity1_violation_percentage.txt')
    severity2_color = colormap('analyzed_data/severity2_violation_percentage.txt')
    severity3_color = colormap('analyzed_data/severity3_violation_percentage.txt')
    return violation_color, severity1_color, severity2_color, severity3_color

if __name__ == "__main__":
    result = run()

    # save violation percentage dictionary as .pickle
    with open('color_data/restaurant_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[0], handle, protocol=pickle.HIGHEST_PROTOCOL)

    # save severity1 percentage dictionary as .pickle
    with open('color_data/severity1_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[1], handle, protocol=pickle.HIGHEST_PROTOCOL)

    # save severity2 percentage dictionary as .pickle
    with open('color_data/severity2_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[2], handle, protocol=pickle.HIGHEST_PROTOCOL)

    # save severity3 percentage dictionary as .pickle
    with open('color_data/severity3_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[3], handle, protocol=pickle.HIGHEST_PROTOCOL)
