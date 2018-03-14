import csv
import pickle
import simplejson as json

#vio_percentage, severity1, severity2, severity3, fail_percentage_zipcode
def read_json(filename):
    print('opening file...')
    with open(filename, 'r') as fp:
        print('file read...')
        return json.load(fp)

def read_pickle(filename):
    """
    open and converts a pickled file into a variable
    """
    print('opening file...')
    f = open(filename, 'rb')
    retVal = pickle.load(f)
    ('file loaded...')
    f.close
    return retVal


if __name__ == '__main__':
    violation = read_json("analyzed_data/restaurant_violation_percentage.txt")
    print(len(violation))
