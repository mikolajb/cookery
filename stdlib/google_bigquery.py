@cookery.action('JSON')
def google_bigquery(args):
    from oauth2client.client import SignedJwtAssertionCredentials
    import json
    from apiclient import discovery
    from httplib2 import Http

    json_key = json.load(open("..."))

    credentials = SignedJwtAssertionCredentials(
        json_key['client_email'],
        json_key['private_key'].encode(),
        'https://www.googleapis.com/auth/bigquery')

    http = Http()
    credentials.authorize(http)
    bigquery = discovery.build('bigquery', 'v2', http=http)

    query = args
    req = bigquery.jobs().query(projectId='...',
                                body=query)

    result = req.execute()
    print(repr(result))
    return result
