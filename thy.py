import requests
import base64
# from urllib2 import Request, urlopen
# from urllib import urlencode, quote_plus
import urllib.request
from urllib.error import HTTPError


class THYAPI(object):
    """ THY API. """
    def __init__(self):
        """ Initializes the API object with URL attributes. """
        self.base_url = 'https://api.turkishairlines.com'
        self.path = ''
        self.param_str = ''

    @property
    def full_url(self):
        """ Returns the full URL for requesting the data. """
        return '{}{}{}'.format(self.base_url, self.path, self.param_str)

    def get_request(self):
        """ Requests the API endpoint and returns the response """
        url = 'https://api.turkishairlines.com/test/getAvailability'
        headers = {'apisecret':'','Content-Type':'application/json','apikey':''}
        values = '{ \
                "requestHeader": {\
                        "clientUsername": "OPENAPI",\
                        "clientTransactionId": "CLIENT_TEST_1",    \
                        "channel": "WEB"\
                },\
                "ReducedDataIndicator": false,\
                "RoutingType": "R",\
                "PassengerTypeQuantity": [{\
                        "Code": "adult",\
                        "Quantity": 1\
                },	\
                {\
                        "Code": "child",\
                        "Quantity": 1\
                }, \
                { \
                "Code": "infant",\
                "Quantity": 0\
                }],\
                "OriginDestinationInformation": [{\
                        "DepartureDateTime": {\
                                "WindowAfter": "P0D",\
                                "WindowBefore": "P0D",\
                                "Date": "14JAN"\
                        },\
                        "OriginLocation": {\
                                "LocationCode": "IST",\
                                "MultiAirportCityInd": false\
                        },\
                        "DestinationLocation": {\
                                "LocationCode": "ESB",\
                                "MultiAirportCityInd": false\
                        },\
                        "CabinPreferences": [{\
                                "Cabin": "ECONOMY"\
                        },\
                        {\
                                "Cabin": "BUSINESS"\
                        }]\
                },\
                {\
                        "DepartureDateTime": {\
                                "WindowAfter": "P0D",\
                                "WindowBefore": "P0D",\
                                "Date": "19JAN"\
                        },\
                        "OriginLocation": {\
                                "LocationCode": "ESB",\
                                "MultiAirportCityInd": false\
                        },\
                        "DestinationLocation": {\
                                "LocationCode": "IST",\
                                "MultiAirportCityInd": false\
                        },\
                        "CabinPreferences": [{\
                                "Cabin": "ECONOMY"\
                        },\
                        {\
                                "Cabin": "BUSINESS"\
                        }]\
                }]\
              }'\

        binary_data = values.encode()
        request = urllib.request.Request(url
        , data=binary_data
        , headers=headers
        , method='POST')
        # request.get_method = lambda: 'POST'
        try:
            response_body = urllib.request.urlopen(request).read()
            resp_json = response_body.decode('utf-8')
            print(resp_json)
            print(type(resp_json))

            print()
        except HTTPError as e:
            content = e.read()
            print(content)


if __name__ == '__main__':
    a = THYAPI()
    a.get_request()
