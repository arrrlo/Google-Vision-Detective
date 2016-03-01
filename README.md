<h1>Google Vision Detective</h1>

A wrapper for Google Vision API. It eases all the preparations that needs to be done prior to sending a request to Google Vision API, which is image downloading (if it is taken from certain URL) and base64 encoding, API parameters preparation, credentials file invocation, etc.<br /><br />

It can be used as python package and CLI (command line interface). CLI is rather for demonstration purposes.<br /><br />

<h3>Instalation</h3>

<p>Install using pip:</p>
```
pip install git+git://github.com/arrrlo/Google-Vision-Detective@master
```

<h3>Get Google Vision API credentials</h3>

<p>In order to use Google Vision API you must get credentials in form of json file. To do that go to <a href="https://cloud.google.com/vision/">Google Cloud Vision Homepage</a>, enable Cloud Vision API in your Google API Manager and issue a credentials json file.<br/><br/>

Detailed help: <a href="https://cloud.google.com/vision/docs/getting-started">Google Cloud Vision API: Getting Started</a></p>

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

<h3>Use it as CLI (command line interface)</h3>

<p>Fetch a photo from URL and detect what is on that image:</p>

```
gvdetective -c path/to/your/credentials/file.json -i ~/input_dir/ labels -i http://www.domain.com/image.jpg
```

<p>Fetch a photo from URL, detect faces and save new image with faces in sqares:</p>

```
gvdetective -c path/to/your/credentials/file.json -i ~/img/input faces -i http://www.domain.com/image.jpg -o ~/img/output
```

<h3>Path to credentials file in environment variables</h3>

<p>Google Cloud Vision API python package needs to have GOOGLE_APPLICATION_CREDENTIALS environment variable set in order to work.</p>

You can set it using this three different ways:<br /><br />

In Linux: 
```
$ export GOOGLE_APPLICATION_CREDENTIALS=__path_to_your_credentials_jon_file__
```
In code:
```python
credentials = os.path.join('__path_to_your_credentials_json_file__')
detective = GoogleVisionDetective(credentials=credentials)
```
In code:
```python
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join('__path_to_your_credentials_json_file__')
detective = GoogleVisionDetective()
```
In CLI:
```
gvdetective -c path/to/your/credentials/file.json ...
```

<p>Once the environment variable is set, it doesn't needs to be set again, meaning you can use this code without explicitly inserting credentials file path into GoogleVisionDetective class.</p>
