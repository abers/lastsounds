# lastsounds
Simple way to scrobble tracks from a BBC Sounds programme to Last.fm

Either use pipenv to install dependencies, or pip install pylast, bs4, and colorama.

Rename details_config and add an API key & secret along with your username. An API key & secret can be created at www.last.fm/api/account/create. 

Then run with python3 and paste url to the episode from BBC Sounds you want to scrobble.

## To do

- [ ] Add proper README
- [ ] Switch from username / password to SessionKeyGenerator
- [ ] Add command line arguments
- [ ] Add option to check / correct each track
- [ ] Refactor for proper seperation before / after if name = main
