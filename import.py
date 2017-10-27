import argparse
import json

from auth import get_authenticated_service
from subscriptions import import_subscriptions
from liked import like_videos
from playlist import create_playlist, add_videos_to_playlist


def wrong_operation_type(*arg):
    print('Provided import type is not supported.')
    quit(-1)


def import_playlist(service, videos, playlist):
    playlist_id = create_playlist(service, playlist)

    if not playlist_id:
        return

    add_videos_to_playlist(service, playlist_id, videos)


allowed_operations = {
    'SUBSCRIPTIONS': 'subscriptions',
    'LIKED': 'liked',
    'PLAYLIST': 'playlist'
}
operation_map = {
    allowed_operations['SUBSCRIPTIONS']: lambda service, channels, *arg: import_subscriptions(service, channels),
    allowed_operations['LIKED']: lambda service, videos, *arg: like_videos(service, videos),
    allowed_operations['PLAYLIST']: import_playlist
}

parser = argparse.ArgumentParser(
    description = 'Import YouTube Takeout data.',
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
    '-c', '--client-secrets',
    type = str,
    default = 'client_secrets.json',
    help = 'The client secrets file used for authorizing access to your YouTube account.'
)

parser.add_argument(
    '-t', '--type',
    choices = list(allowed_operations.values()),
    default = allowed_operations['SUBSCRIPTIONS'],
    help = 'Type of the data to import.'
)

parser.add_argument(
    '-p', '--playlist',
    type = str,
    default = 'Playlist',
    help = 'When import type is a playlist, this indicates the name of the playlist to create.'
)

parser.add_argument(
    'file',
    type = str,
    nargs = '?',
    default = 'takeout.json',
    help = 'The takeout file in JSON format to import.'
)

args = parser.parse_args()
with open(args.file, encoding = 'utf-8', mode = 'r') as takeout_file:
    parsed_takeout = json.load(takeout_file)

if not isinstance(parsed_takeout, list):
    print('The Takeout file must contain an array of data.')
    quit(-1)

operation = operation_map.get(args.type, wrong_operation_type)

print('Importing {}.'.format(args.type))

operation(get_authenticated_service(args.client_secrets), parsed_takeout, args.playlist)

print('Import complete.')
