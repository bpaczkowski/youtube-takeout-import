from googleapiclient.discovery import HttpError

from helpers import get


def like_videos(service, videos: list):
    if len(videos) == 0:
        print('No videos to like.')

        return

    print('Liking {} videos.'.format(len(videos)))

    for index, video in enumerate(videos):
        print('#{} '.format(index), end = '')

        video_id = get(video, 'snippet.resourceId.videoId')
        video_title = get(video, 'snippet.title')

        if not video_id:
            print('wrong video format.')

            continue

        print('ID: {}, title: "{}"'.format(video_id, video_title), end = '')

        try:
            service.videos().rate(
                id = video_id,
                rating = 'like'
            ).execute()

            print(' liked.')
        except HttpError as e:
            print(' error:')
            print(e)
