import click
import logging


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@click.command()
@click.option('--interval-seconds', type=int, required=False, default=600,
              help='interval between images, in seconds')
def cli(interval_seconds):
    """Collect time-lapse images and compose time-lapse videos - results are saved to S3"""
    log.info(f'Starting time-lapse image collection with interval of {interval_seconds}s')
