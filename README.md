# Pimelapse 

A simple program for time lapse imagery with a Raspberry Pi

## Setup

Setting up your Raspberry Pi and its camera is not covered here, there are a wealth of tutorials
out there on the web for you.

The output images are written to a bucket on S3. The paths are currently hard-coded in `pimelapse.py`.
You may need to edit these paths, and will certainly need to set up your pi so that it can has
the right AWS credentials to access them (read and write). I won'y repeat all this here.

Install using pip. The pi-specific dependencies (e.g. `picamera`) are optional
```bash
pip install pimelapse  # without pi-specific dependencies
pip install pimelapse[camera]  # with pi-specific dependencies
```

## Usage

The installed package provides two CLIs;

+ `pimelapse-images`: takes images at regular intervals and writes them to S3
+ `pimelapse-video`: downloads these images and composes a video from them

You can see details for either CLI with the `--help` flag.

To configure your Pi to run `pimelapse-images` on startup (which you will want for a headless
setup), you can edit the paths in `pimelapse.service` and then configure it to run automatically
with `systemd`. There is a tutorial on this at: https://www.raspberrypi.org/documentation/linux/usage/systemd.md

