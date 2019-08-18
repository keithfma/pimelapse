import click
import logging
import warnings
import boto3
from io import BytesIO
from time import sleep
from datetime import datetime, timedelta
from tempfile import TemporaryDirectory
import os
import subprocess


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
@click.option('-d', '--days', type=float, required=False, help='days to include in video interval')
@click.option('-h', '--hours', type=float, required=False, help='hours to include in video interval')
@click.option('-m', '--minutes', type=float, required=False, help='minutes to include in video interval')
@click.option('-f', '--framerate', type=int, required=False, default=30,
              help='output video framerate, in images per second')
@click.option('-o', '--output', type=str, required=False, default='video',
              help='Name (without extension) for video file to create')
def video_cli(days, hours, minutes, framerate, output):
    """Build video from time-lapse images on S3"""
    if not days and not hours and not minutes:
        raise ValueError('0 duration specified, aborting')
    duration = timedelta(seconds=0)
    if days:
        duration += timedelta(days=days)
    if hours:
        duration += timedelta(hours=hours)
    if minutes:
        duration += timedelta(minutes=minutes)
    start_time = datetime.now() - duration
    log.info(f'Creating video from images starting at {start_time} with total duration of {duration}')

    log.info('Initialize S3 access')
    client = boto3.client('s3') 

    # find images
    image_keys = []
    response = client.list_objects_v2(Bucket=IMAGE_BUCKET, Prefix=f'{IMAGE_PREFIX}/')
    image_keys.extend(c['Key'] for c in response['Contents'])
    while response['IsTruncated']:
        response = client.list_objects_v2(
            Bucket=IMAGE_BUCKET, Prefix=IMAGE_PREFIX, ContinuationToken=response['NextContinuationToken'])
        image_keys.extend(c['Key'] for c in response['Contents'])

    # find subset in time interval
    image_keys = sorted(image_keys)
    valid_image_keys = []
    for image_key in image_keys:
        try:
            image_date_str = os.path.splitext(os.path.basename(image_key))[0]
            image_date = datetime.strptime(image_date_str, TIME_FORMAT)
        except ValueError:
            log.warning(f'Skipped key: {image_key}')
            continue
        if image_date >= start_time:
            valid_image_keys.append(image_key)
    log.info(f'Found {len(valid_image_keys)} images in time window')

    with TemporaryDirectory() as tmp_dir:
        # download image
        for ii, image_key in enumerate(valid_image_keys):
            image_path = os.path.join(tmp_dir, os.path.basename(image_key))
            log.info(f'Downloading {ii+1}/{len(valid_image_keys)}: {image_path}') 
            response = client.get_object(Bucket=IMAGE_BUCKET, Key=image_key)
            with open(image_path, 'wb') as fp:
                fp.write(response['Body'].read())
        
        # generate video
        output_file = f'{output}.mp4'
        cmd = ['ffmpeg', '-y', '-framerate', f'{framerate}', '-i', f'{tmp_dir}/%*.png', output_file]
        subprocess.run(cmd, check=True)
        log.info(f'Output video created at {output_file}')

