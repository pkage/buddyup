import urllib.request
import json

API_KEY = "AIzaSyCY5GQokqJksx1TgkVIcMPC9kL5tR9W0CI"

# get dictionary of places near specified location,
# types may also be specified, i.e. 'gym'
# location specified as a string of "lat, lng" coordinates
def getPlaces(location, radius, keyword, type):
    url = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=%s&type=%s&keyword=%s&key=%s') % (location, radius, type, keyword, API_KEY)
    with urllib.request.urlopen(url) as response:
        jsonRaw = response.read()
    places = json.loads(jsonRaw)
    return places

def getCityLocation(keyword):
    url = ('https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s') % (keyword, API_KEY)
    with urllib.request.urlopen(url) as response:
        jsonRaw = response.read()
    place = json.loads(jsonRaw)
    lat = place['results'][0]['geometry']['location']['lat']
    lng = place['results'][0]['geometry']['location']['lng']
    return str(lat) + ',' + str(lng)

# search for nearby gyms
def getGymsNearby(location, radius):
    return getPlaces(location, radius, 'gym', 'gym')

# search for nearby universities
def getUnisNearby(location, radius):
    return getPlaces(location, radius, 'university', 'school')

# returns location of a specified place ID in
# format of "lat, lng" coordinates
def getPlaceIDLocation(place_id):
    url = ('https://maps.googleapis.com/maps/api/geocode/json?place_id=%s&key=%s') % (place_id, API_KEY)
    with urllib.request.urlopen(url) as response:
        jsonRaw = response.read()
    place = json.loads(jsonRaw)
    lat = place['results'][0]['geometry']['location']['lat']
    lng = place['results'][0]['geometry']['location']['lng']
    return str(lat) + ',' + str(lng)
