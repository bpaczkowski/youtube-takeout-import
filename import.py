import argparse
import json

from auth import get_authenticated_service
from subscriptions import import_subscriptions
from liked import like_videos


def wrong_operation_type(*arg):
    print('Provided import type is not supported.')
    quit(-1)


allowed_operations = {
    'SUBSCRIPTIONS': 'subscriptions',
    'PLAYLIST': 'playlist',
    'LIKED': 'liked'
}
operation_map = {
    allowed_operations['SUBSCRIPTIONS']: import_subscriptions,
    allowed_operations['LIKED']: like_videos
}

parser = argparse.ArgumentParser(
    description = 'Import YouTube Takeout data.',
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
    '-c', '--client-secrets',
    type = str,
    default = 'client_secrets.json',
    help = 'The client secrets filed used for authorizing access to your YouTube account.'
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
    type = argparse.FileType('r'),
    nargs = '?',
    default = 'takeout.json',
    help = 'The takeout file in JSON format to import.'
)

args = parser.parse_args()
parsedTakeout = json.load(args.file)

if not isinstance(parsedTakeout, list):
    print('The Takeout file must contain an array of data.')
    quit(-1)

operation = operation_map.get(args.type, wrong_operation_type)

print('Importing {}.'.format(args.type))

operation(get_authenticated_service(args.client_secrets), parsedTakeout)

print('Import complete.')
