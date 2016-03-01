from setuptools import setup

setup(
    name = 'Google Vision Detective',
    description = 'Easy use of Google Vision API',
    version = "0.1",
    url = 'https://github.com/arrrlo/Google-Vision-Detective',

    author = 'Ivan Arar',
    author_email = 'ivan.arar@gmail.com',

    packages = ['google_vision_detective'],
    install_requires = [
        'google-api-python-client==1.5.0',
        'requests==2.9.1',
        'Pillow==3.1.1',
        'click==6.3',
    ],

    entry_points = {
        'console_scripts': [
            'gvdetective=google_vision_detective.cli:cli'
        ],
    },
)
