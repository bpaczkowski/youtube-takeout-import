from googleapiclient.discovery import HttpError
from helpers import get, safe_json_parse, has


def import_subscriptions(service, channels):
    for index, channel in enumerate(channels):
        if index == 75:
            print('reached channel limit')
            break

        print('#{} '.format(index), end = '')

        channel_id = get(channel, 'snippet.resourceId.channelId')
        channel_name = get(channel, 'snippet.title')

        if not channel_id or not channel_name:
            print('wrong channel format')
            continue

        print('ID: {}, name: {}'.format(channel_id, channel_name))

        try:
            service.subscriptions().insert(
                body = {
                    'snippet': {
                        'resourceId': {
                            'channelId': channel_id
                        }
                    }
                },
                part = 'snippet'
            ).execute()
        except HttpError as e:
            if not has(e, 'resp.status') or e.resp.status != 400 or not e.content:
                print(e)
                continue

            parsed_content = safe_json_parse(e.content)

            if not has(parsed_content, 'error.errors') or len(parsed_content['error']['errors']) < 1:
                print(e)
                continue

            any_error_is_limit = any(
                e['message'] == 'Too many recent subscriptions. Please try again in a few hours.'
                for e in parsed_content['error']['errors']
            )

            if not any_error_is_limit:
                print(e)
                continue

            print('Reached subscription limit, run this script again in about 4 hours.')
            break
