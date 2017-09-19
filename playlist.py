from googleapiclient.discovery import HttpError

from helpers import get


def create_playlist(service, name: str):
    print('Creating a playlist with name "{}".'.format(name))

    try:
        result = service.playlists().insert(
            body = {
                'snippet': {
                    'title': name
                },
                'status': {
                    'privacyStatus': 'private'
                }
            },
            part = 'snippet,status'
        ).execute()

        print('Playlist created.')

        return get(result, 'id')
    except HttpError as e:
        print(e)

        return None


def add_videos_to_playlist(service, playlist_id: str, videos: list):
    if len(videos) == 0:
        print('No videos to add to playlist.')

        return

    print('Adding {} videos to playlist.'.format(len(videos)))

    for index, video in enumerate(videos):
        print('#{} '.format(index), end = '')

        video_id = get(video, 'snippet.resourceId.videoId')
        video_title = get(video, 'snippet.title')

        if not video_id:
            print('wrong video format.')

            continue

        print('ID: {}, title: "{}"'.format(video_id, video_title), end = '')

        try:
            service.playlistItems().insert(
                body = {
                    'snippet': {
                        'playlistId': playlist_id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                },
                part = 'snippet'
            ).execute()

            print(' added to playlist.')
        except HttpError as e:
            print(' error:')
            print(e)
