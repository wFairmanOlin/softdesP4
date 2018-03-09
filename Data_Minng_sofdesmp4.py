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

def get_restaurants_list(filename):
    restaurant_list = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            restaurant = Restaurant(name = row['businessName'], address = row['Address'], date = row['VIOLDTTM'], vio_status = row['ViolStatus'], vio_level = row['ViolLevel'], viodesc = row['ViolDesc'], comment = row['Comments'], zipcode = row['ZIP'])
            #print(restaurant)
            restaurant_list.append(restaurant)
    return restaurant_list

class Restaurants:
    def __init__(self, name, restaurant_list = None):
        self.name = name
        if restaurant_list  == None:
            restaurant_list = []
        self.restaurants = restaurant_list

    def group_by_zipcode(self):
        """Return a zipcode dictionary for restaurants"""
        zipcode = {}
        for restaurant in self.restaurants:
            if restaurant.zipcode not in zipcode.keys():
                zipcode[restaurant.zipcode] = [restaurant.name]
            else:
                if restaurant.name not in zipcode[restaurant.zipcode]:
                    zipcode[restaurant.zipcode].append(restaurant.name)
        return zipcode

    def histogram_inspection_times(self):
        """Return the number of times a restaurant get inspected"""
        inspection_his = {}
        for restaurant in self.restaurants:
            inspection_his[restaurant.name] = inspection_his.get(restaurant.name, 0) + 1
        return inspection_his


    def histogram_fail(self):
        """Return the number of times a restaurant failed the inspection"""
        fail_his = {}
        for restaurant in self.restaurants:
            if restaurant.vio_status == 'Fail':
                fail_his[restaurant.name] = fail_his.get(restaurant.name, 0) + 1
        return fail_his


    def histogram_severity(self, severity):
        """Return a severity histogram"""
        severity_his = {}
        for restaurant in self.restaurants:
            if restaurant.viol_level == severity:
                severity_his[restaurant.name] = severity_his.get(restaurant.name, 0) + 1
        return severity_his

    def get_violation_percentage(self):
        """Return the percentage of failing cases out of the total number of inspection time for each restaurant."""
        violation_percentage = {}
        num_inspection = self.histogram_inspection_times()
        fail = self.histogram_fail()
        for i in num_inspection:
            if i not in fail.keys():
                fail[i] = 0
            percentage = fail[i]/num_inspection[i]*100
            violation_percentage[i] = percentage
        return violation_percentage

    def get_severity_percentage(self,severity_level):
        """Return the percentage of * failing cases out of all failing cases"""
        severities = {}
        fail = self.histogram_fail()
        severity = self.histogram_severity(severity_level)
        for i in fail:
            if i not in severity.keys():
                severity[i] = 0
            percentage = severity[i] / fail[i] * 100
            severities[i] = percentage
        return severities

    











if __name__ == "__main__":
    Boston = Restaurants('boston', get_restaurants_list('test2.csv'))
    #severity2 = Boston.histogram_severity('**')
    #fail = Boston.histogram_fail()
    #inspection = Boston.histogram_inspection_times()
    #zipcode = Boston.group_by_zipcode()
    vio_percentage = Boston.get_violation_percentage()
    print(vio_percentage)

