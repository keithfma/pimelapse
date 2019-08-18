import click
import logging
import warnings
import boto3
from io import BytesIO
from time import sleep
from datetime import datetime


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


IMAGE_BUCKET = 'ma-family-homelab'
IMAGE_PREFIX = 'pimelapse'
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


@click.command()
@click.option('--interval-min', type=float, required=False, default=10,
              help='interval between images, in seconds')
def images_cli(interval_min):
    """Collect time-lapse images and save to S3"""
    import picamera  # note: only used for image collection, install is optional so only imported here
    log.info(f'Starting time-lapse image collection with interval of {interval_min} minutes')

    log.info('Initialize camera')
    camera = picamera.PiCamera()
    camera.resolution = (1920, 1080)  # 1080p, a good standard resolution
    camera.start_preview()
    sleep(3)

    log.info('Initialize S3 access')
    client = boto3.client('s3') 

    while True:  # image capture loop -- run forever
        image_stream = BytesIO()
        camera.capture(image_stream, 'png')
        image_key = f'{IMAGE_PREFIX}/{datetime.now().strftime(TIME_FORMAT)}.png'
        client.put_object(
            Bucket=IMAGE_BUCKET,
            Key=image_key,
            Body=image_stream.getvalue(),
            ContentType='image/png')
        log.info(f'uploaded image to s3://{IMAGE_BUCKET}/{image_key}')
        sleep(interval_min*60)


@click.command()
def video_cli():
    """Build video from time-lapse images on S3"""
    # TODO: initialize access to S3
    # TODO: find images in time interval
    # TODO: sync image folder
    # TODO: build video
    raise NotImplementedError()
