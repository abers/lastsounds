import requests
from bs4 import BeautifulSoup

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
    print(artist.get_text(), " - ", track.get_text())
