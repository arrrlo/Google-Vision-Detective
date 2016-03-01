<h1>Google Vision Detective</h1>

A wrapper for Google Vision API. It eases all the preparations that needs to be done prior to sending a request to Google Vision API, which is image downloading (if it is taken from certain URL) and base64 encoding, API parameters preparation, credentials file invocation, etc.<br /><br />

It can be used as python package and CLI (command line interface). CLI is rather for demonstration purposes.<br /><br />

<h3>Instalation</h3>

<p>Install using pip:</p>
```
pip install git+git://github.com/arrrlo/Google-Vision-Detective@master
```

<h3>Use it as python package</h3>

```python
import os

from google_vision_detective import GoogleVisionDetective, Request
from google_vision_detective.features import Fase, Label

images = [
  '__image1_url__',
  '__image2_url__',
  .
  .
  .
]

credentials = os.path.join('__path_to_your_credentials_json_file__')
input_dir = os.path.join('__path_to_dir_where_image_from_url_is_saved__')

detective = GoogleVisionDetective(credentials=credentials, input_dir=input_dir)

for image in images:
  with Request(detective, image) as request:
    request.feature(Label(max_results=10))
    request.feature(Face(max_results=10))

responses = detective.obj.detect()
```
