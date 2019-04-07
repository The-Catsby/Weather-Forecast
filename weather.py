import sys
import urllib2
import json

"""
    Command Line Weather Forecast
    Uses the National Weather Service's API
        https://www.weather.gov/documentation/services-web-api#/
"""

def main(argv):
    # input validation
    if len(argv) == 1:
        # No arguments passed in
        print("ERROR: enter a zipcode")
    elif len(argv) > 2:
        # More than one argument passed in
        print("ERROR: Too many arguments")
    else:
        # Valid Input
        zipcode = argv[1]

        # Create dict from the zipcode data file
        dict = {}
        with open('zipcodes') as file:
            for line in file:
                (key, sep, val) = line.partition(',')
                dict[key] = val[:-1] # don't include \n character

        # Verify zipcode exists
        if zipcode not in dict:
            print("ERROR: Invalid zipcode")
            return

        # Get lat/long from zipcode
        (lat, sep, long) = dict[zipcode].partition(',')
        # NWS precision to 4 decimal places; separate by a comma
        lat_long = lat[:-2] + ',' + long[:-2]

        # Get forecast from the National Weather Service
        base_url = 'https://api.weather.gov/points/'
        url = base_url + lat_long
        req = json.load( urllib2.urlopen(url) )

        # get the forecast url
        forecast_url = req['properties']['forecast']

        # Send GET request for today's forecast (response includes 14 days of data)
        req = json.load( urllib2.urlopen(forecast_url) )
        data = req['properties']['periods'][0]

        # Output data
        print('{} will be {}'.format(data['name'], data['detailedForecast']))

if __name__ == '__main__':
    main(sys.argv)
