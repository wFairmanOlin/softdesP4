import pickle
import os

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
    data = read_pickle('color_data/severity1_violation_percentage.pickle')
    #print(data)
    for i in data:
        print(data[i]['color'])