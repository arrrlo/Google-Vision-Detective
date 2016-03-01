import click

from PIL import Image
from PIL import ImageDraw

from features import Face, Label
from detective import GoogleVisionDetective, Request, DetectiveException


@click.group()
@click.option('-c', '--credentials')
@click.option('-i', '--input_dir')
@click.pass_context
def cli(detective, credentials, input_dir):
    detective.obj = GoogleVisionDetective(credentials=credentials, input_dir=input_dir)


@cli.command()
@click.option('-i', '--input_file')
@click.option('-m', '--max_results', default=10)
@click.pass_context
def labels(detective, input_file, max_results):
    with Request(detective.obj, input_file) as request:
        request.feature(Label(max_results=max_results))
    
    responses = detective.obj.detect()
    for response in responses:
        for feature in response.features:
            for label in feature.annotations:
                print('{description} ({score})'.format(**label))


@cli.command()
@click.option('-i', '--input_file')
@click.option('-o', '--output_dir')
@click.option('-m', '--max_results', default=10)
@click.pass_context
def faces(detective, input_file, output_dir, max_results):
    with Request(detective.obj, input_file) as request:
        request.feature(Face(max_results=max_results))
    
    responses = detective.obj.detect()
    for response in responses:
        response.image.seek(0)
        
        im = Image.open(response.image)
        draw = ImageDraw.Draw(im)
        
        for feature in response.features:
            for face in feature.annotations:
                box = [(v['x'], v['y']) for v in face['fdBoundingPoly']['vertices']]
                draw.line(box + [box[0]], width=5, fill='#00ff00')

        del draw

        output_file = output_dir + response.image.name.split('/')[-1]
        im.save(output_file)

        print('Found %s face%s' % (len(feature.annotations), '' if len(feature.annotations) == 1 else 's'))
        print('Writing to file %s' % output_file)


