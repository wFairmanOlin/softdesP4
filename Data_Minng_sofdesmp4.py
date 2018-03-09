import csv
class Restaurant:

    def __init__(self, name, address, date,vio_status,vio_level,viodesc,comment,zipcode):
        self.name = name
        self.address = address
        self.date = date
        self.vio_status = vio_status
        self.viol_level = vio_level
        self.viodesc = viodesc
        self.comment = comment
        self.zipcode = zipcode

    def __str__(self):
        return 'name: %s' %self.name + '\n' + 'address: %s' %self.address + '\n' + 'date: %s' %self.date + '\n' + 'violation status: %s' %self.vio_status + '\n' + 'violation level: %s' %self.viol_level+ '\n'+ 'violation description: %s' %self.viodesc + '\n' + 'comment: %s' %self.comment + 'zipcode: %s' %self.zipcode

def get_restaurants_list():
    restaurant_list = []
    with open('mayorsfoodcourt.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            restaurant = Restaurant(name = row['businessName'], address = row['Address'], date = row['VIOLDTTM'], vio_status = row['ViolStatus'], vio_level = row['ViolLevel'], viodesc = row['ViolDesc'], comment = row['Comments'], zipcode = row['ZIP'])
            #print(restaurant)
            restaurant_list.append(restaurant)
    return restaurant_list

def group_by_zipcode(restaurant_list):
    """Return a zipcode dictionary for restaurants"""
    zipcode = {}
    for restaurant in restaurant_list:
        if restaurant.zipcode not in zipcode.keys():
            zipcode[restaurant.zipcode] = [restaurant.name]
        else:
            if restaurant.name not in zipcode[restaurant.zipcode]:
                zipcode[restaurant.zipcode].append(restaurant.name)
    return zipcode

def histogram_inspection_times(restaurant_list):
    """Return the number of times a restaurant get inspected"""
    inspection_his = {}
    for restaurant in restaurant_list:
        inspection_his[restaurant.name] = inspection_his.get(restaurant.name, 0) + 1
    return inspection_his


def histogram_fail(restaurant_list):
    """Return the number of times a restaurant failed the inspection"""
    fail_his = {}
    for restaurant in restaurant_list:
        if restaurant.vio_status == 'Fail':
            fail_his[restaurant.name] = fail_his.get(restaurant.name, 0) + 1
    return fail_his


def histogram_severity1(restaurant_list):
    """Return a severity1 * histogram"""
    severity1_his = {}
    for restaurant in restaurant_list:
        if restaurant.viol_level == '*':
            severity1_his[restaurant.name] = severity1_his.get(restaurant.name, 0) + 1
    return severity1_his


def histogram_severity2(restaurant_list):
    """Return a severity2 ** histogram"""
    severity2_his = {}
    for restaurant in restaurant_list:
        if restaurant.viol_level == '**':
            severity2_his[restaurant.name] = severity2_his.get(restaurant.name, 0) + 1
    return severity2_his



def histogram_severity3(restaurant_list):
    """Return a severity3 *** histogram"""
    severity3_his = {}
    for restaurant in restaurant_list:
        if restaurant.viol_level == '***':
            severity3_his[restaurant.name] = severity3_his.get(restaurant.name, 0) + 1
    return severity3_his


if __name__ == "__main__":
    restaurants = get_restaurants_list()
    #severity2 = histogram_severity2(restaurants)
    fail = histogram_fail(restaurants)
    inspection = histogram_inspection_times(restaurants)
    zipcode = group_by_zipcode(restaurants)
    print(zipcode)

