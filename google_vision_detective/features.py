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
                setattr(self, method, response[obj_param.name])
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