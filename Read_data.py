import csv
import pickle
import simplejson as json

#vio_percentage, severity1, severity2, severity3, fail_percentage_zipcode
def read_json(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)

if __name__ == '__main__':
    violation = read_json("analyzed_data/restaurant_violation_percentage.txt")
    print(violation)
    print(len(violation))