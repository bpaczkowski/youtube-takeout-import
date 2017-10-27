## Youtube Takeout Import

### Installation

Clone or download the repository, then in the repository directory install dependencies using pipenv:
```
pipenv install google-api-python-client oauth2client httplib2
```

### Usage

Create a Google Takeout archive [here](https://takeout.google.com/settings/takeout) for YouTube with all the required data types. Make sure to select the JSON format. Hint: likes are exported as a playlist, to import them, just use the playlist export file with `liked` as type when running import.py.

On the account you want to import to, go to [this](https://console.developers.google.com/apis/dashboard) page and follow these instructions:
1. Create a new project.
2. Go to the [credentials](https://console.developers.google.com/apis/credentials) page.
3. Create new OAuth client ID credentials selecting "other" as application type.
4. Close the popup with the credentials.
5. Download the client secrets file using the download button to the right of the created credentials.
6. Put that file in the repository directory and rename it to `client_secrets.json`.

Script usage:
```
$ pipenv run import.py -- -h
usage: import.py [-h] [-c CLIENT_SECRETS] [-t {subscriptions,liked,playlist}]
                 [-p PLAYLIST]
                 [file]

Import YouTube Takeout data.

positional arguments:
  file                  The takeout file in JSON format to import. (default:
                        takeout.json)

optional arguments:
  -h, --help            show this help message and exit
  -c CLIENT_SECRETS, --client-secrets CLIENT_SECRETS
                        The client secrets file used for authorizing access to
                        your YouTube account. (default: client_secrets.json)
  -t {subscriptions,liked,playlist}, --type {subscriptions,liked,playlist}
                        Type of the data to import. (default: subscriptions)
  -p PLAYLIST, --playlist PLAYLIST
                        When import type is a playlist, this indicates the
                        name of the playlist to create. (default: Playlist)
```
