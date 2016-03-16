class Field(object):

    def __init__(self, name):
        self.name = name


class Feature(object):
    def __init__(self, max_results=10):
        self.max_results = max_results

    def __call__(self, response):
        for method in dir(self):
            obj_param = getattr(self, method)
            if type(obj_param) is Field:
                try:
                    setattr(self, method, response[obj_param.name])
                except:
                    setattr(self, method, [])
        return self

    @classmethod
    def META(cls):
        return cls.Meta


class Label(Feature):
    annotations = Field('labelAnnotations')

    class Meta:
        name = 'labels'
        description = 'Label Detection'
        detection_type = 'LABEL_DETECTION'


class Face(Feature):
    annotations = Field('faceAnnotations')

    class Meta:
        name = 'faces'
        description = 'Face Detection'
        detection_type = 'FACE_DETECTION'


class Text(Feature):
    annotations = Field('textAnnotations')

    class Meta:
        name = 'text'
        description = 'Text Detection'
        detection_type = 'TEXT_DETECTION'


class Landmark(Feature):
    annotations = Field('landmarkAnnotations')

    class Meta:
        name = 'landmark'
        description = 'Landmark Detection'
        detection_type = 'LANDMARK_DETECTION'


class Logo(Feature):
    annotations = Field('logoAnnotations')

    class Meta:
        name = 'logo'
        description = 'Logo Detection'
        detection_type = 'LOGO_DETECTION'


class SafeSearch(Feature):
    annotations = Field('safeSearchAnnotation')

    class Meta:
        name = 'safe-search'
        description = 'Safe Search Detection'
        detection_type = 'SAFE_SEARCH_DETECTION'


class Properties(Feature):
    annotations = Field('imagePropertiesAnnotation')

    class Meta:
        name = 'properties'
        description = 'Image Properties'
        detection_type = 'IMAGE_PROPERTIES'
