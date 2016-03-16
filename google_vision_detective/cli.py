import os
import click

from PIL import Image
from PIL import ImageDraw

from features import Face, Label, Text, Landmark, Logo, SafeSearch, Properties
from detective import GoogleVisionDetective, Request, DetectiveException


@click.group(help='Detective is a wrapper for Google Vision API')
@click.option('-c', '--credentials', type=click.STRING, 
                                     help='Path to your credentials json file')
@click.option('-i', '--input_dir', type=click.STRING, 
                                   help='Path to directory where input images will be stored')
@click.pass_context
def cli(detective, credentials, input_dir):
    detective.obj = GoogleVisionDetective(credentials=credentials, input_dir=input_dir)


@cli.command(help='Execute Image Content Analysis on the entire image and return')
@click.option('-i', '--input_file', type=click.STRING, 
                                    help='Path to image on the disk or URL')
@click.option('-m', '--max_results', default=10,
                                     help='Maximum results per request')
@click.pass_context
def labels(detective, input_file, max_results):
    with Request(detective.obj, input_file) as request:
        request.feature(Label(max_results=max_results))
    
    responses = detective.obj.detect()
    for response in responses:
        for feature in response.features:
            for label in feature.annotations:
                click.echo('{description} ({score})'.format(**label))


@cli.command(help='Detect faces within the image')
@click.option('-i', '--input_file', type=click.STRING,
                                    help='Path to image on the disk or URL')
@click.option('-o', '--output_dir', type=click.STRING,
                                    help='Path to directory where the image\
                                          with detected faces will be stored')
@click.option('-m', '--max_results', default=10,
                                     help='Maximum results per request')
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

        click.echo('Found %s face%s' % (len(feature.annotations), '' if len(feature.annotations) == 1 else 's'))
        click.echo('Writing to file %s' % output_file)


@cli.command(help='Perform Optical Character Recognition (OCR) on text within the image')
@click.option('-i', '--input_file', type=click.STRING, 
                                    help='Path to image on the disk or URL')
@click.option('-m', '--max_results', default=10,
                                     help='Maximum results per request')
@click.pass_context
def text(detective, input_file, max_results):
    with Request(detective.obj, input_file) as request:
        request.feature(Text(max_results=max_results))
    
    responses = detective.obj.detect()
    for response in responses:
        for feature in response.features:
            for label in feature.annotations:
                click.echo('{description} ({locale})'.format(**label))


@cli.command(help='Detect geographic landmarks within the image')
@click.option('-i', '--input_file', type=click.STRING, 
                                    help='Path to image on the disk or URL')
@click.option('-m', '--max_results', default=10,
                                     help='Maximum results per request')
@click.pass_context
def landmark(detective, input_file, max_results):
    with Request(detective.obj, input_file) as request:
        request.feature(Landmark(max_results=max_results))
    
    responses = detective.obj.detect()
    for response in responses:
        for feature in response.features:
            for label in feature.annotations:
                click.echo(label)


@cli.command(help='Detect company logos within the image')
@click.option('-i', '--input_file', type=click.STRING, 
                                    help='Path to image on the disk or URL')
@click.option('-m', '--max_results', default=10,
                                     help='Maximum results per request')
@click.pass_context
def logo(detective, input_file, max_results):
    with Request(detective.obj, input_file) as request:
        request.feature(Logo(max_results=max_results))
    
    responses = detective.obj.detect()
    for response in responses:
        for feature in response.features:
            for label in feature.annotations:
                click.echo(label)


@cli.command(help='Determine image safe search properties on the image')
@click.option('-i', '--input_file', type=click.STRING, 
                                    help='Path to image on the disk or URL')
@click.option('-m', '--max_results', default=10,
                                     help='Maximum results per request')
@click.pass_context
def safe_search(detective, input_file, max_results):
    with Request(detective.obj, input_file) as request:
        request.feature(SafeSearch(max_results=max_results))
    
    responses = detective.obj.detect()
    for response in responses:
        for feature in response.features:
            for key, val in feature.annotations.items():
                click.echo('{}: {})'.format(key, val))


@cli.command(help='Compute a set of properties about the image (such as the image\'s dominant colors)')
@click.option('-i', '--input_file', type=click.STRING, 
                                    help='Path to image on the disk or URL')
@click.option('-m', '--max_results', default=10,
                                     help='Maximum results per request')
@click.pass_context
def properties(detective, input_file, max_results):
    with Request(detective.obj, input_file) as request:
        request.feature(Properties(max_results=max_results))
    
    responses = detective.obj.detect()
    for response in responses:
        for feature in response.features:
            click.echo(feature.annotations)
