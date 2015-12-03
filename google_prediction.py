@cookery.subject('http', r'(.+)')
def remote_file(url):
    import requests

    r = requests.get(url)
    return r.text

@cookery.action()
def display(subject):
    print(repr(subject))

@cookery.action('test')
def google_prediction(subject, args):
    from oauth2client.client import SignedJwtAssertionCredentials
    import json
    from apiclient import discovery

    json_key = json.load(open("Cookery-30137725a678.json"))

    credentials = SignedJwtAssertionCredentials(
        json_key['client_email'],
        json_key['private_key'].encode(),
        'https://www.googleapis.com/auth/prediction')

    prediction = discovery.build('prediction', 'v1.6')

    models = prediction.trainedmodels()

    results = []
    for data in subject:
        r = models.predict('symbolic-button-852', 'language-detection',
                           json.dumps({"input": {"csvInstance": [d]}}))
        results.append(json.loads(r))


