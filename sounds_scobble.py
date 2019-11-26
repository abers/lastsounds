import configparser
import datetime
import getpass
import json
import time

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

import pylast

init()


now = datetime.datetime.now()
unixtimenow = time.mktime(now.timetuple())

config = configparser.ConfigParser()
web_prompt = Fore.YELLOW + 'URL for BBC Sounds episode to scrobble: '
pass_prompt = Fore.RED + 'Last.fm password: '


def find_tracklist(scripts):
    for script in soup("script"):
        text = script.text
        if 'window.__PRELOADED_STATE__'.lower() in text.lower():
            return text


def find_artists_and_tracks(tracklist_list):
    artists = []
    tracks = []
    for item in tracklist_list:
        artists.append(item["titles"]["primary"])
        tracks.append(item["titles"]["secondary"])
    return artists, tracks


if __name__ == "__main__":

    config.read('.details')

    API_KEY = config['API']['API_KEY']
    API_SECRET = config['API']['API_SECRET']
    username = " "
    username = config['LOGIN']['username']

    webpage = input(web_prompt)
    password_hash = pylast.md5(getpass.getpass(pass_prompt))
    print(Style.RESET_ALL)

    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                                   username=username,
                                   password_hash=password_hash)
    print(Fore.LIGHTCYAN_EX + webpage)

    page = requests.get(str(webpage))
    print(page)
    print()

    soup = BeautifulSoup(page.content, 'html.parser')

    tracklist = find_tracklist(soup)
    tracklist = tracklist.strip('window.__PRELOADED_STATE__ = ')
    tracklist_json = json.loads(tracklist[:-1])
    tracklist_list = tracklist_json["tracklist"]["tracks"]

    artists, tracks = find_artists_and_tracks(tracklist_list)

    # artist_class_string = "sc-u-truncate gel-pica-bold gs-u-mb-- gs-u-pr-alt@m"
    # artists = soup.find_all("p", {"class": artist_class_string})

    # track_class_string = "sc-u-truncate gel-long-primer gs-u-pr-alt@m"
    # tracks = soup.find_all("p", {"class": track_class_string})

    for artist, track in zip(artists, tracks):
        scrobble_text = Fore.LIGHTYELLOW_EX + 'Scrobbling: '
        artist_text = Fore.LIGHTBLUE_EX + artist
        track_text = Fore.LIGHTGREEN_EX + track + Style.RESET_ALL
        separator = Fore.LIGHTMAGENTA_EX + " - "
        print(scrobble_text, artist_text, separator, track_text)
        network.scrobble(artist, track, unixtimenow)

    print()
    print(Fore.LIGHTRED_EX + "Scrobbling complete")
    print()
