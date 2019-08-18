import click
import logging


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@click.command()
@click.option('--interval-min', type=int, required=False, default=10,
              help='interval between images, in seconds')
def images_cli(interval_min):
    """Collect time-lapse images and save to S3"""
    log.info(f'Starting time-lapse image collection with interval of {interval_min} minutes')
    # TODO: initialize access to S3
    # TODO: enter image capture loop -- run forever
    # TODO: capture image
    # TODO: write to S3


@click.command()
def video_cli():
    """Build video from time-lapse images on S3"""
    # TODO: initialize access to S3
    # TODO: find images in time interval
    # TODO: sync image folder
    # TODO: build video
    raise NotImplementedError()
