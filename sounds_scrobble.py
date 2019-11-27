"""TODO."""
import configparser
import datetime
import getpass
import json
import time

import click
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

import pylast


def get_password_hash():
    """TODO."""
    pass_prompt = Fore.RED + "Last.fm password: "
    password_hash = pylast.md5(getpass.getpass(pass_prompt))
    print()
    return password_hash


def get_url():
    """TODO."""
    url_prompt = Fore.YELLOW + "URL for BBC Sounds episode to scrobble: "
    url = input(url_prompt)
    return url


def get_range():
    """TODO."""
    first_prompt = Fore.YELLOW + "First track to scrobble: "
    last_prompt = Fore.YELLOW + "Last track to scrobble: "
    while True:
        try:
            first = int(input(first_prompt))
        except ValueError:
            print("Value must be an integer.")
            continue
        else:
            break
    while True:
        try:
            last = int(input(last_prompt))
        except ValueError:
            print("Value must be an integer.")
        else:
            break
    print()
    return first, last


def find_tracklist(scripts):
    """TODO.
    May need to split into check_tracklist and find_tracklist."""
    for script in scripts("script"):
        text = script.text
        if "window.__PRELOADED_STATE__".lower() in text.lower():
            text = text.strip("window.__PRELOADED_STATE__ = ")
            tracklist_json = json.loads(text[:-1])
            tracklist = tracklist_json["tracklist"]["tracks"]
    return tracklist


def find_artists_tracks_lengths(tracklist_list):
    """TODO."""
    artists = []
    tracks = []
    lengths = []
    for item in tracklist_list:
        artists.append(item["titles"]["primary"])
        tracks.append(item["titles"]["secondary"])
        lengths.append(item["offset"]["end"] - item["offset"]["start"])
    return artists, tracks, lengths


def scrobble_tracklist(artists, tracks, lengths, network):
    """TODO."""
    now = datetime.datetime.now()
    unixtime = time.mktime(now.timetuple())

    scrobble_text = Fore.LIGHTYELLOW_EX + "Scrobbling: "
    separator = Fore.LIGHTMAGENTA_EX + " - "

    def artist_text(artist):
        return Fore.LIGHTBLUE_EX + artist

    def track_text(track):
        return Fore.LIGHTGREEN_EX + track + Style.RESET_ALL

    for artist, track, length in zip(artists, tracks, lengths):
        print(scrobble_text, artist_text(artist), separator, track_text(track))
        unixtime -= length
        network.scrobble(artist, track, unixtime)
    print()
    print(Fore.LIGHTRED_EX + "Scrobbling complete")
    print()


@click.command()
# TODO: make optional
@click.argument("url", default=None, required=False)
@click.option(
    "--all-tracks/--partial",
    "-a/-p",
    default=True,
    help="Scrobble all tracks or part of an episode.",
)
def main(url, all_tracks):
    """Scrobble tracks from a BBC Sounds episode to Last.fm."""
    config = configparser.ConfigParser()
    config.read(".details")
    api_key = config["API"]["api_key"]
    api_secret = config["API"]["api_secret"]
    username = config["LOGIN"]["username"]

    if url is None:
        url = get_url()

    # TODO: Check URL - including if None input then quit application
    # TODO: If succesful print Scrobbling programme_title

    if not all:
        first, last = get_range()

    # TODO: Move below chunk into a function
    print(Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + url)
    page = requests.get(str(url))
    print(page)
    print()

    soup = BeautifulSoup(page.content, "html.parser")

    tracklist = find_tracklist(soup)

    if not all_tracks:
        first, last = get_range()
        tracklist = tracklist[first - 1 : last]

    # TODO: Sort tracklist
    tracklist = tracklist[::-1]

    artists, tracks, lengths = find_artists_tracks_lengths(tracklist)

    # TODO: Replace with pylast authentication class.
    password_hash = get_password_hash()
    network = pylast.LastFMNetwork(
        api_key=api_key,
        api_secret=api_secret,
        username=username,
        password_hash=password_hash,
    )

    scrobble_tracklist(artists, tracks, lengths, network)


if __name__ == "__main__":

    init()
    main()
