import csv
import pickle
import simplejson as json

class Restaurant:

    def __init__(self, name, address, vio_status,vio_level,viodesc,comment,zipcode):
        self.name = name
        self.address = address
        self.vio_status = vio_status
        self.viol_level = vio_level
        self.viodesc = viodesc
        self.comment = comment
        self.zipcode = zipcode

    def __str__(self):
        return 'name: %s' %self.name + '\n' + 'address: %s' %self.address + '\n' +  'violation status: %s' %self.vio_status + '\n' + 'violation level: %s' %self.viol_level+ '\n'+ 'violation description: %s' %self.viodesc + '\n' + 'comment: %s' %self.comment + 'zipcode: %s' %self.zipcode

def get_restaurants_list(filename):
    restaurant_list = []
    with open(filename,encoding = "ISO-8859-1", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            restaurant = Restaurant(name = row['businessName'], address = row['Address'], vio_status = row['ViolStatus'], vio_level = row['ViolLevel'], viodesc = row['ViolDesc'], comment = row['Comments'], zipcode = row['ZIP'])
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

    def get_violation_by_zipcode(self):
        """Return the total number of fails in a zipcode region divided by total number of fails in boston"""
        fail_by_zipcode = {}
        fail = self.histogram_fail()
        total_fails_boston = sum(fail.values())
        zipcodes = self.group_by_zipcode()
        for zipcode in zipcodes:
            total_fails_zipcode = 0
            for restaurant in zipcodes[zipcode]:
                if restaurant not in fail.keys():
                    total_fails_zipcode += 0
                else:
                    total_fails_zipcode += fail[restaurant]
            fail_by_zipcode[zipcode] = total_fails_zipcode/total_fails_boston * 100
        return fail_by_zipcode



def run(filename,listname):
    name = Restaurants(listname, get_restaurants_list(filename))
    vio_percentage = name.get_violation_percentage()
    severity1 = name.get_severity_percentage('*')
    severity2 = name.get_severity_percentage('**')
    severity3 = name.get_severity_percentage('***')
    fail_percentage_zipcode = name.get_violation_by_zipcode()
    return vio_percentage, severity1, severity2, severity3, fail_percentage_zipcode


if __name__ == "__main__":
    result = run('mayorsfoodcourt.csv', 'Boston')
    # save violation percentage dictionary as a txt
    with open("analyzed_data/restaurant_violation_percentage.txt", "w") as output:
        output.write(json.dumps(result[0]))

    # save violation percentage dictionary as .pickle
    with open('analyzed_data/restaurant_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[0], handle, protocol=pickle.HIGHEST_PROTOCOL)


    # save zipcode percentage dictionary as a txt
    with open("analyzed_data/zipcode_violation_percentage.txt", "w") as output:
        output.write(json.dumps(result[-1]))

    # save zipcode percentage dictionary as .pickle
    with open('analyzed_data/zipcode_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[-1], handle, protocol=pickle.HIGHEST_PROTOCOL)


    # save severity1 percentage dictionary as a txt
    with open("analyzed_data/severity1_violation_percentage.txt", "w") as output:
        output.write(json.dumps(result[1]))

    # save severity1 percentage dictionary as .pickle
    with open('analyzed_data/severity1_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[1], handle, protocol=pickle.HIGHEST_PROTOCOL)


    # save severity2 percentage dictionary as a txt
    with open("analyzed_data/severity2_violation_percentage.txt", "w") as output:
        output.write(json.dumps(result[2]))

    # save severity2 percentage dictionary as .pickle
    with open('analyzed_data/severity2_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[2], handle, protocol=pickle.HIGHEST_PROTOCOL)


    # save severity3 percentage dictionary as a txt
    with open("analyzed_data/severity3_violation_percentage.txt", "w") as output:
        output.write(json.dumps(result[3]))

    # save severity3 percentage dictionary as .pickle
    with open('analyzed_data/severity3_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[3], handle, protocol=pickle.HIGHEST_PROTOCOL)


    print(result)

