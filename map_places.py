import urllib
import urllib2
import json


GEOCODE_URL_FMT = (
    "http://maps.googleapis.com/maps/api/geocode/json?%(address)s&sensor=true"
)

def get_places(repo):
    """
    Scrape an `underground` repo for bars, restaurants, cafes, etc.
    Each place should be defined by a whatever.md file.

    :param str repo:
        URL of the `underground` repo or any fork.
        For example, https://github.com/OpenTechSchool/underground.
    """
    # TODO: use github api


def get_place_tokens(file_url):
    """
    Get the file at ``file_url`` and attempt to scrape the following
    information from it::

        * name (of the location)
        * address
        * website

    :returns:
        A dict with the keys `name`, `address`, and `website`.
        Values are strings. Not all values are guaranteed to populated.
    """
    fh = None  # TODO: filelike to read from

    name = None
    address = None
    website = None

    for line in fh:
        line = line.lower().strip()
        if line.startswith('address:') and not address:
            _, address = line.split(':')
        # TODO: can also try to get name from the header of the file
        elif line.startswith('name:') and not name:
            _, name = line.split(':')
        elif line.startswith('website:') and not website:
            _, website = line.split(':')

    result = dict(name=name, address=address, website=website)


def get_lon_lat(address):
    """
    Use the google geocode API (http://maps.googleapis.com/maps/api/geocode)
    to try and get the coordinates for a location given a complete or partial
    address.

    :returns:
        A dict with the keys `lon` and `lat`. Values are floats.
    """
    url = GEOCODE_URL_FMT % urllib.urlencode(dict(address=address))
    resp = urllib2.urlopen(url)
    json_data = json.loads(resp.read())

    # TODO: handle errors
    # TODO: can that even happen???
    loc = json_data['results'][0]['geometry']['location']
    return dict(lon=loc['lng'], lat=loc['lat']


if __name__ == "__main__":
    base_url = "http://maps.googleapis.com/maps/api/geocode/json?%s&sensor=true"

    the_file = 'Colab.md'
    text = [line for line in open(the_file)]

    addy = [x for x in text if x.lower().startswith('address:')]

    if addy:
        addy = addy[0]
        _, addy = addy.split(':')

    # TODO: make name and website parsing smarter
    params = urllib.urlencode(dict(address=addy))
    url = base_url % params
    resp = urllib2.urlopen(url)

    data = resp.read()
    print data

    json_data = json.loads(data)
    loc = json_data['results'][0]['geometry']['location']
    lat = loc['lat']
    lng = loc['lng']

    print 'Lon: %s, Lat: %s' % (lng, lat)
