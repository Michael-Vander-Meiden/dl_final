#!/usr/bin/env python3

import os
import sys
import argparse

import ffmpy

import detect
import track
import stylize

def video_to_frames(video_path, tmp):
  images_name = '.'.join(video_path.split('/')[-1].split('.')[:-1])

  codec = ffmpy.FFmpeg(inputs={video_path: None}, outputs={tmp+'/'+images_name+'_%d.jpg': '-y -vf fps=30'})

  codec.run()

def frames_to_video(video_path, tmp):
  images_name = os.listdir(tmp)[0].split('_')[-1]

  codec = ffmpy.FFmpeg(inputs={tmp+'/'+images_name+'_%d.jpg': '-r 30'}, outputs={video_path: '-c:v libx264 -vf fps=30'})

  codec.run()

def main(src_path, dst_path, mdl, cfg, uuid):

  if os.path.exists(os.path.abspath('itmp')):
    os.rmdir(os.path.abspath('itmp'))
  os.makedirs(os.path.abspath('itmp'))

  if os.path.exists(os.path.abspath('otmp')):
    os.rmdir(os.path.abspath('otmp'))
  os.makedirs(os.path.abspath('otmp'))

  video_to_frames(src_path, os.path.abspath('itmp'))

  iframes = os.listdir('itmp')
  oframes = [iframe.replace('itmp', 'otmp') for iframe in iframes]

  all_detections = identify.get_detections(iframes)
  masks = []

  for i, i_detections in enumerate(all_detections):
    if i == 0:
      mask, box = track.select_detection(i_detections, uuid)
    else:
      mask, box = track.filter_detection(i_detections, box)

    masks.append(mask)

  stylize.stylize_frame(iframes, masks, oframes, mdl, cfg)

  frames_to_video(dst_path, os.path.abspath('otmp'))


if __name__ == "__main__":
  
  parser = argparse.ArgumentParser(description='Stylize a video')
  
  parser.add_argument('-s', '--source',      help='video source')
  parser.add_argument('-d', '--destination', help='video destination')
  parser.add_argument('-m', '--model',       help='style model',      choices=['original', 'arbitrary'])
  parser.add_argument('-c', '--config',      help='style config',     default='{}')
  parser.add_argument('-u', '--uuid',        help='instance uuid',    default=1)

  args = parser.parse_args()

  main(args.source, args.destination, args.model, eval(args.config), args.uuid)