import httplib2

from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

storage_file = 'oauth.json'
scope = 'https://www.googleapis.com/auth/youtube'
secrets_file_missing_message = ' file is missing'


def get_authenticated_service(secrets_file):
    flow = flow_from_clientsecrets(
        secrets_file,
        scope = scope,
        message = secrets_file + secrets_file_missing_message
    )
    storage = Storage(storage_file)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    return build("youtube", "v3", http = credentials.authorize(httplib2.Http()))
