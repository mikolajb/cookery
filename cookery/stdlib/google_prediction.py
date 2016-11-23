@cookery.subject('http', r'(.+)')
def remote_file(url):
    import requests

    r = requests.get(url)
    return r.text

@cookery.action()
def display(subject):
    print(repr(subject))

@cookery.action()
def google_prediction(subject, args):
    from oauth2client.service_account import ServiceAccountCredentials
    from apiclient import discovery
    from httplib2 import Http

    scopes = ['https://www.googleapis.com/auth/prediction']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "...",
        scopes
    )

    http_auth = Http()
    credentials.authorize(http_auth)
    prediction = discovery.build('prediction', 'v1.6', http=http_auth)
    models = prediction.trainedmodels()
    results = []
    for data in subject:
        r = models.predict(project='symbolic-button-852',
                           id='language-detection',
                           body={"input": {"csvInstance": [data]}})
        results.append(r.execute()['outputLabel'])

    return results
