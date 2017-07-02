import base64
import json
import pprint
import requests
from flask_ask import statement

# def make_call_to_myalfred_api(json_data):
#     # call to rest api myalfred
#     url = 'https://staging.myalfred.io/api/schedule/google'
#     header_authentication_base64 = 'Basic QW1hem9uQWxleGFDbGllbnQ6N20zM1AySzd0WWhjZ0tOdk5wZDc0N3BSRmZvOUg4'
#     data = json.dumps([1, 2, 3])
#     req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
#     req.add_header('Authentication', header_authentication_base64)
#     try:
#         f = urllib2.urlopen(req)
#         response = f.read()
#         f.close()
#     except urllib2.HTTPError, error:
#         response = error.read()
#         print response
#     return response
from requests.auth import HTTPBasicAuth


def make_call_to_myalfred_api_2(json_data):
    """
    Makes a POST-request to the myAlfred Scheduling API using a JSON object
    containing Google Calendar token & desired scheduling setup and returns the response body.

    :param json_data: the json request containing all relevant information about a desired event
    :return: The response body of the scheduling api
    """
    url = 'https://staging.myalfred.io/api/schedule/google'
    try:
        r = requests.post(url, auth=HTTPBasicAuth('AmazonAlexaClient', '7m33P2K7tYhcgKNvNpd747pRFfo9H8'), json=json_data)
        #data = json.loads(r.text)
        pprint.pprint(r.text)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print err
        return "shit"
    # except requests.exceptions.Timeout:
    #     pprint.pprint("try again")
    #     make_call_to_myalfred_api_2(json_data)
    # except requests.exceptions.TooManyRedirects:
    #     pprint.pprint("bad url")
    #     return "sdfa"
    # except requests.exceptions.RequestException as e:
    #     pprint.pprint("really bad error..")
    #     print e
    #     return "dfa"

    pprint.pprint("geklappt..")
    return statement("geklappt")