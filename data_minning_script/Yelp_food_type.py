from __future__ import print_function
import argparse
import requests
import sys
import pickle
import urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode
from Read_data import read_pickle

# Get Food Type from Yelp

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


def get_restaurant_food_type(restaurant, location):
    """Return query result for each restaurant from Yelp Fusion."""
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=restaurant,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=location, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        #print(query_api(input_values.term, input_values.location))
        return query_api(input_values.term, input_values.location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


def get_food_type(api_key, search_limit, filename):
    """Return the food type for each restaurant and store it in a dictionary."""
    data = read_pickle(filename)
    for restaurant in data:
        yelp_foodtype = get_restaurant_food_type(restaurant, data[restaurant]['address'])
        #print(yelp_foodtype)
        if yelp_foodtype == None:
            data[restaurant]['foodtype'] = 'None'
        else:
            if yelp_foodtype['categories'] == []:
                data[restaurant]['foodtype'] = 'None'
            else:
                data[restaurant]['foodtype'] = yelp_foodtype['categories'][0]['title']
                print(data[restaurant]['foodtype'])
            #print(data[restaurant]['foodtype'])
    return data


def run():
    violation = get_food_type(API_KEY, SEARCH_LIMIT, '../color_data/restaurant_violation_percentage.pickle')
    return violation



if __name__ == '__main__':
    result = run()

    # save violation percentage dictionary as .pickle
    with open('../foodtype_data/foodtype.pickle', 'wb') as handle:
        pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

