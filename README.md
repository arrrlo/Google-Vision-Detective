<h1>Google Vision Detective</h1>

A wrapper for Google Vision API. It eases all the preparations that needs to be done prior to sending a request to Google Vision API, which is image downloading (if it is taken from certain URL) and base64 encoding, API parameters preparation, credentials file invocation, etc.<br /><br />

It can be used as python package and CLI (command line interface). CLI is rather for demonstration purposes.<br /><br />

<h3>Instalation</h3>

<p>Install using pip:</p>
```
pip install git+git://github.com/arrrlo/Google-Vision-Detective@master
```

<h3>Get Google Vision API credentials</h3>

<p>In order to use Google Vision API you must get credentials in form of json file. To do that go to <a href="https://cloud.google.com/vision/">Google Cloud Vision Homepage</a>, enable Cloud Vision API in your Google API Manager and issue a credentials json file.<br/>
<h href="https://cloud.google.com/vision/docs/getting-started">Google Cloud Vision API: Getting Started</a></p>

<h3>Use it as python package</h3>

```python
import os

from google_vision_detective import GoogleVisionDetective, Request
from google_vision_detective.features import Face, Label

credentials = os.path.join('__path_to_your_credentials_json_file__')
input_dir = os.path.join('__path_to_dir_where_image_from_url_is_saved__')

detective = GoogleVisionDetective(credentials=credentials, input_dir=input_dir)

images = [
  '__image1_url__',
  '__image2_url__',
  .
  .
  .
]

for image in images:
  with Request(detective, image) as request:
    request.feature(Label(max_results=10))
    request.feature(Face(max_results=10))

responses = detective.obj.detect()
```

