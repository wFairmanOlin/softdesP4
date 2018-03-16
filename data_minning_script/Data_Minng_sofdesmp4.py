from __future__ import print_function
import csv
import pickle
import simplejson as json
import argparse
import requests
import sys
import urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

# Get Rating from Yelp

# API constants.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

API_KEY = '6VjxLN9LBKQGN5ioh-Uq0xbmWEmBywgAb1C1SZDBYx0AbCRbmjymbhzgLzqaTTn3XFFyZzCDfc8q-IU_iEhJiRkDbhR32DgV0xe7k1VKvlj1GvNjhTsyd8eBwzOoWnYx'
SEARCH_LIMIT = 1


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
          'for the top result "{1}" ...'.format(
        len(businesses), business_id))
    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))
    return response


def get_restaurant_rating(restaurant, location):
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=restaurant,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=location, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        return query_api(input_values.term, input_values.location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


class Restaurant:
    def __init__(self, name, address, vio_status, vio_level, viodesc, comment, zipcode, location):
        self.name = name
        self.address = address
        self.vio_status = vio_status
        self.viol_level = vio_level
        self.viodesc = viodesc
        self.comment = comment
        self.zipcode = zipcode
        # self.rating = rating
        lon_la = []
        if location == None:
            self.location = (0, 0)
        else:
            for i in location.strip('()').split():
                lon_la.append(float(i.strip(',')))
            self.location = tuple(lon_la)

    def __str__(self):
        return (
            'name: %s' % self.name + '\n' + 'address: %s' % self.address + '\n' + 'violation status: %s' % self.vio_status + '\n'
            + 'violation level: %s' % self.viol_level + '\n' + 'violation description: %s' % self.viodesc + '\n' + 'comment: %s' % self.comment + 'zipcode: %s' % self.zipcode + '\n' + 'location: %s' % self.location)


def get_restaurants_list(filename):
    restaurant_list = []
    with open(filename, encoding="ISO-8859-1", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            restaurant = Restaurant(name=row['businessName'],
                                    address=row['Address'] + ' ' + row['CITY'] + ' ' + row['STATE'] + ' ' + row['ZIP'],
                                    vio_status=row['ViolStatus'],
                                    vio_level=row['ViolLevel'], viodesc=row['ViolDesc'], comment=row['Comments'],
                                    zipcode=row['ZIP'], location=row['Location'])
            # print(restaurant)
            restaurant_list.append(restaurant)
    return restaurant_list


class Restaurants:
    def __init__(self, name, restaurant_list=None):
        self.name = name
        if restaurant_list == None:
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
            inspection_his[restaurant.name] = inspection_his.get(restaurant.name, {})
            inspection_his[restaurant.name]['inspection'] = inspection_his[restaurant.name].get('inspection', 0) + 1
            inspection_his[restaurant.name]['address'] = inspection_his[restaurant.name].get('address',
                                                                                             restaurant.address)
            inspection_his[restaurant.name]['location'] = inspection_his[restaurant.name].get('location',
                                                                                              restaurant.location)
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
            percentage = fail[i] / num_inspection[i]['inspection'] * 100
            violation_percentage[i] = {}
            violation_percentage[i]['address'] = num_inspection[i]['address']
            violation_percentage[i]['location'] = num_inspection[i]['location']
            violation_percentage[i]['percentage'] = percentage

        # unit test to check one entry in violation percentage dictionary
        # for i in violation_percentage:
        #     print(i, violation_percentage[i], '\n')
        #     break

        return violation_percentage

    def get_severity_percentage(self, severity_level):
        """Return the percentage of * failing cases out of all inspection cases"""
        severities = {}
        num_inspection = self.histogram_inspection_times()
        severity = self.histogram_severity(severity_level)

        for i in num_inspection:
            if i not in severity.keys():
                severity[i] = 0
            percentage = severity[i] / num_inspection[i]['inspection'] * 100
            # print(percentage)
            severities[i] = {}
            severities[i]['percentage'] = percentage
            severities[i]['address'] = num_inspection[i]['address']
            severities[i]['location'] = num_inspection[i]['location']

        return severities

    def sort_all_3_severity_percentage(self):
        allseverity1 = self.get_severity_percentage('*')  # all restaurants with severity level 1

        # # unit test to check one entry in allseverity1 dictionary
        # for i in allseverity1:
        #     print(i, allseverity1[i], '\n')
        #     break

        allseverity2 = self.get_severity_percentage('**')  # all restaurants with severity level 2
        allseverity3 = self.get_severity_percentage('***')  # all restaurants with severity level 2
        severity1 = {}  # restaurants with severity level 1 as the highest percentage among 3 levels
        severity2 = {}  # restaurants with severity level 2 as the highest percentage among 3 levels
        severity3 = {}  # restaurants with severity level 3 as the highest percentage among 3 levels
        for i in allseverity3:
            if i not in allseverity2.keys():
                allseverity2[i]['percentage'] = 0
            if i not in allseverity1.keys():
                allseverity1[i]['percentage'] = 0
            if allseverity3[i]['percentage'] == max(allseverity3[i]['percentage'], allseverity2[i]['percentage'],
                                                    allseverity1[i]['percentage']):
                severity3[i] = {}
                severity3[i]['percentage'] = allseverity3[i]['percentage']
                severity3[i]['address'] = allseverity3[i]['address']
                severity3[i]['location'] = allseverity3[i]['location']
            elif allseverity2[i]['percentage'] == max(allseverity3[i]['percentage'], allseverity2[i]['percentage'],
                                                      allseverity1[i]['percentage']):
                severity2[i] = {}
                severity2[i]['percentage'] = allseverity2[i]['percentage']
                severity2[i]['address'] = allseverity2[i]['address']
                severity2[i]['location'] = allseverity2[i]['location']
            else:
                severity1[i] = {}
                severity1[i]['percentage'] = allseverity1[i]['percentage']
                severity1[i]['address'] = allseverity1[i]['address']
                severity1[i]['location'] = allseverity1[i]['location']
        return severity1, severity2, severity3

    def test_duplicate_in_severity_123(self):
        """Check whether a restaurant appears in all severity levels. Return False it does and true if none."""
        severity1, severity2, severity3 = self.sort_all_3_severity_percentage
        for i in severity1:
            if i in severity3.keys() or i in severity2.keys():
                print(i, 'False')
            else:
                print('True')

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
            fail_by_zipcode[zipcode] = total_fails_zipcode / total_fails_boston * 100
        return fail_by_zipcode

    def get_rating(self, api_key, search_limit):
        """Return a dictionary of restaurant ratings."""
        restaurant_rating = {}
        violation = self.get_violation_percentage()
        for restaurant in violation.keys():
            if restaurant_rating.get(restaurant, 'NA') == 'NA':
                yelp_rating = get_restaurant_rating(restaurant, violation[restaurant]['address'])
                if yelp_rating == None:
                    restaurant_rating[restaurant] = 'No rating'
                else:
                    restaurant_rating[restaurant] = yelp_rating['rating']
        return restaurant_rating


def run(filename, listname):
    name = Restaurants(listname, get_restaurants_list(filename))
    vio_percentage = name.get_violation_percentage()
    severity1, severity2, severity3 = name.sort_all_3_severity_percentage()
    fail_percentage_zipcode = name.get_violation_by_zipcode()
    rating = name.get_rating(API_KEY, SEARCH_LIMIT)
    return vio_percentage, severity1, severity2, severity3, rating, fail_percentage_zipcode


if __name__ == "__main__":
    result = run('mayorsfoodcourt.csv', 'Boston')
    # save violation percentage dictionary as a txt
    with open("../analyzed_data/restaurant_violation_percentage.txt", "w") as output:
        output.write(json.dumps(result[0]))

    # save violation percentage dictionary as .pickle
    with open('../analyzed_data/restaurant_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[0], handle, protocol=pickle.HIGHEST_PROTOCOL)

    # save zipcode percentage dictionary as a txt
    with open("../analyzed_data/zipcode_violation_percentage.txt", "w") as output:
        output.write(json.dumps(result[-1]))

    # save zipcode percentage dictionary as .pickle
    with open('../analyzed_data/zipcode_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[-1], handle, protocol=pickle.HIGHEST_PROTOCOL)

    # save severity1 percentage dictionary as a txt
    with open("../analyzed_data/severity1_violation_percentage.txt", "w") as output:
        output.write(json.dumps(result[1]))

    # save severity1 percentage dictionary as .pickle
    with open('../analyzed_data/severity1_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[1], handle, protocol=pickle.HIGHEST_PROTOCOL)

    # save severity2 percentage dictionary as a txt
    with open("../analyzed_data/severity2_violation_percentage.txt", "w") as output:
        output.write(json.dumps(result[2]))

    # save severity2 percentage dictionary as .pickle
    with open('../analyzed_data/severity2_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[2], handle, protocol=pickle.HIGHEST_PROTOCOL)

    # save severity3 percentage dictionary as a txt
    with open("../analyzed_data/severity3_violation_percentage.txt", "w") as output:
        output.write(json.dumps(result[3]))

    # save severity3 percentage dictionary as .pickle
    with open('../analyzed_data/severity3_violation_percentage.pickle', 'wb') as handle:
        pickle.dump(result[3], handle, protocol=pickle.HIGHEST_PROTOCOL)

    # save rating dictionary as a txt
    with open("../analyzed_data/rating.txt", "w") as output:
        output.write(json.dumps(result[4]))

    # save rating dictionary as .pickle
    with open('../analyzed_data/rating.pickle', 'wb') as handle:
        pickle.dump(result[4], handle, protocol=pickle.HIGHEST_PROTOCOL)
