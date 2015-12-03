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
    from oauth2client.client import SignedJwtAssertionCredentials
    import json
    from apiclient import discovery
    from httplib2 import Http

    json_key = json.load(open("..."))

    credentials = SignedJwtAssertionCredentials(
        json_key['client_email'],
        json_key['private_key'].encode(),
        'https://www.googleapis.com/auth/prediction')

    http = Http()
    credentials.authorize(http)
    prediction = discovery.build('prediction', 'v1.6', http=http)
    models = prediction.trainedmodels()
    results = []
    for data in subject:
        r = models.predict(project='symbolic-button-852',
                           id='language-detection',
                           body={"input": {"csvInstance": [data]}})
        results.append(r.execute()['outputLabel'])

    return results
