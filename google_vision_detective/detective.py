import os
import shutil
import base64
import requests

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'


class DetectiveException(Exception):
    pass


class Request(object):

    def __init__(self, detective, image):
        self.features = []
        self.image = image
        self.detective = detective

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.detective.set_request(self.image, self.features)

    def feature(self, feature):
        self.features.append(feature)


class Response(object):

    def __init__(self, image):
        self.features = []
        self.image = image

    def set_feature(self, feature):
        self.features.append(feature)


class GoogleVisionDetective(object):

    def __init__(self, credentials=None, input_dir=None):
        self.images = []
        self.requests = []
        self.input_dir = input_dir or os.getcwd()
        self.credentials = credentials

    def set_request(self, image, features):
        new_features = []
        for feature in features:
            new_features.append({
                'type': feature.META().detection_type, 
                'maxResults': feature.max_results
            })

        if image.startswith('http'):
            image = self.download(image)
            if not image:
                raise DetectiveException('Image download failed :(')

        image = open(image, 'rb')

        self.images.append({
            'image': image,
            'features': features,
        })
        
        self.requests.append({
            'image': {'content': base64.b64encode(image.read())},
            'features': new_features,
        })

    def download(self, url):
        input_path = False
        req = requests.get(url, stream=True)
        if req.status_code == 200:
            input_path = self.input_dir + url.split('/')[-1]
            with open(input_path, 'wb') as file_on_disk:
                req.raw.decode_content = True
                shutil.copyfileobj(req.raw, file_on_disk)
        return input_path

    def detect(self):
        try:
            request = self.service().images().annotate(body={'requests': self.requests})
            response = request.execute()
        except:
            raise DetectiveException('Google API Request Error. Check internet connection.')

        i = 0
        detection_responses = []
        for image in self.images:
            
            response_obj = Response(image=image['image'])
            for feature in image['features']:
                response_obj.set_feature(feature(response['responses'][i]))
                i += 1

            detection_responses.append(response_obj)

        self.remove_credentials_env()

        return detection_responses

    def service(self):
        if not 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
            try:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials
            except:
                raise DetectiveException("""Cloud Vision API credentials not set.
Check documentation for help: https://github.com/arrrlo/Google-Vision-Detective""")
        
        try:
            credentials = GoogleCredentials.get_application_default()
            return discovery.build('vision', 'v1', credentials=credentials, 
                                                   discoveryServiceUrl=DISCOVERY_URL)
        except:
            raise DetectiveException('Google API Error. Check your credentials.')
