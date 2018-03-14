import csv
import pickle
import simplejson as json

#vio_percentage, severity1, severity2, severity3, fail_percentage_zipcode
def read_json(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
    return data

if __name__ == "__main__":
    vio_percentage = read_json('analyzed_data/restaurant_violation_percentage.txt')
    print(vio_percentage)
    severity1 = read_json("analyzed_data/severity1_violation_percentage.txt")
    severity2 = read_json("analyzed_data/severity2_violation_percentage.txt")
    severity3 = read_json("analyzed_data/severity3_violation_percentage.txt")
