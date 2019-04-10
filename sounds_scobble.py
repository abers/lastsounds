import configparser
import requests
import time
import datetime
import getpass

import pylast
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init()

now = datetime.datetime.now()
unixtimenow = time.mktime(now.timetuple())

config = configparser.ConfigParser()
config.read('.details')

API_KEY = config['API']['API_KEY']
API_SECRET = config['API']['API_SECRET']
username = config['LOGIN']['username']

web_prompt = Fore.YELLOW + 'URL for BBC Sounds episode to scrobble: '
pass_prompt = Fore.RED + f'Last.fm password for {username}: '

webpage = input(web_prompt)
password_hash = pylast.md5(getpass.getpass(pass_prompt))
print(Style.RESET_ALL)

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                               username=username, password_hash=password_hash)
print(Fore.LIGHTCYAN_EX + webpage)

page = requests.get(str(webpage))
print(page)
print()

soup = BeautifulSoup(page.content, 'html.parser')

artist_class_string = "sc-u-truncate gel-pica-bold gs-u-mb-- gs-u-pr-alt@m"
artists = soup.find_all("p", {"class": artist_class_string})

track_class_string = "sc-u-truncate gel-long-primer gs-u-pr-alt@m"
tracks = soup.find_all("p", {"class": track_class_string})

for artist, track in zip(artists, tracks):
    scrobble_text = Fore.LIGHTYELLOW_EX + 'Scrobbling: '
    artist_text = Fore.LIGHTBLUE_EX + artist.get_text()
    track_text = Fore.LIGHTGREEN_EX + artist.get_text() + Style.RESET_ALL
    separator = Fore.LIGHTMAGENTA_EX + " - "
    print(scrobble_text, artist_text, separator, track_text)
    network.scrobble(artist.get_text(), track.get_text(), unixtimenow)

print()
print(Fore.LIGHTRED_EX + "Scrobbling complete")
print()
