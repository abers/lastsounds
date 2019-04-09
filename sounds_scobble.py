import configparser
import requests
from bs4 import BeautifulSoup
import pylast
import time
import datetime

now = datetime.datetime.now()
unixtimenow = time.mktime(now.timetuple())

config = configparser.ConfigParser()
config.read('.details')

API_KEY = config['API']['API_KEY']
API_SECRET = config['API']['API_SECRET']
username = config['LOGIN']['username']
password_hash = pylast.md5(config['LOGIN']['password'])

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                               username=username, password_hash=password_hash)
webpage = input("Webpage: ")
print(webpage)

page = requests.get(str(webpage))
print(page)

soup = BeautifulSoup(page.content, 'html.parser')

artist_class_string = "sc-u-truncate gel-pica-bold gs-u-mb-- gs-u-pr-alt@m"
artists = soup.find_all("p", {"class": artist_class_string})

track_class_string = "sc-u-truncate gel-long-primer gs-u-pr-alt@m"
tracks = soup.find_all("p", {"class": track_class_string})

for artist, track in zip(artists, tracks):
    print("Scrobbling: ", artist.get_text(), " - ", track.get_text())
    network.scrobble(artist.get_text(), track.get_text(), unixtimenow)




