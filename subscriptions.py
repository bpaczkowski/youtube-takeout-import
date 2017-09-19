from googleapiclient.discovery import HttpError
from helpers import get, safe_json_parse, has, read_json_file, write_json_file


def import_subscriptions(service, channels: list, import_state_filename: str = 'imported_subscriptions.json'):
    import_state = read_json_file(import_state_filename) or []

    if len(import_state) > 0:
        channels = [channel for channel in channels if get(channel, 'snippet.resourceId.channelId') not in import_state]

    if len(channels) == 0:
        print('No channels left to subscribe to.')

        return

    for index, channel in enumerate(channels):
        print('#{} '.format(index), end = '')

        channel_id = get(channel, 'snippet.resourceId.channelId')
        channel_name = get(channel, 'snippet.title')

        if not channel_id or not channel_name:
            print('wrong channel format')

            if channel_id:
                import_state.append(channel_id)

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

            import_state.append(channel_id)
        except HttpError as e:
            if not has(e, 'resp.status') or e.resp.status != 400 or not e.content:
                print(e)

                import_state.append(channel_id)

                continue

            parsed_content = safe_json_parse(e.content)

            if not has(parsed_content, 'error.errors[0]'):
                print(e)

                import_state.append(channel_id)

                continue

            any_error_is_limit = any(
                e['message'] == 'Too many recent subscriptions. Please try again in a few hours.'
                for e in get(parsed_content, 'error.errors')
            )

            if not any_error_is_limit:
                print(e)

                import_state.append(channel_id)

                continue

            print('Reached subscription limit, run this script again in about 4 hours (it will remember already '
                  'subscribed channels).')

            break

    if len(import_state) > 0:
        write_json_file(import_state_filename, import_state)
