#!/usr/bin/env python3

import os
import sys
import shutil
import argparse

import ffmpy

import identify
import track
import stylize

__FPS__ = '1/10'

def video_to_frames(video_path, tmp):
  images_name = '.'.join(video_path.split('/')[-1].split('.')[:-1])

  codec = ffmpy.FFmpeg(inputs={video_path: None}, outputs={tmp+'/'+images_name+'_%d.jpg': '-y -vf fps='+__FPS__})

  codec.run()

def frames_to_video(video_path, tmp):
  images_name = '.'.join(os.listdir(tmp)[0].split('/')[-1].split('_')[:-1])

  codec = ffmpy.FFmpeg(inputs={tmp+'/'+images_name+'_%d.jpg': '-r '+__FPS__}, outputs={video_path: '-c:v libx264 -vf fps='+__FPS__})

  codec.run()

def main(src_path, dst_path, cfg, uuid):

  if os.path.exists(os.path.abspath('itmp')):
    shutil.rmtree(os.path.abspath('itmp'))
  os.makedirs(os.path.abspath('itmp'))

  if os.path.exists(os.path.abspath('otmp')):
    shutil.rmtree(os.path.abspath('otmp'))
  os.makedirs(os.path.abspath('otmp'))

  video_to_frames(src_path, os.path.abspath('itmp'))

  iframes = ['itmp/' + iframe for iframe in os.listdir('itmp')]
  oframes = [iframe.replace('itmp', 'otmp') for iframe in iframes]

  print(iframes)

  all_detections = identify.get_detections(iframes)

  masks = []

  for i, i_detections in enumerate(all_detections):
    print
    if i == 0:
      mask, box = track.select_detection(i_detections, uuid)
    else:
      mask, box = track.filter_detection(i_detections, box)

    masks.append(mask)

  stylize.stylize_frame(iframes, masks, oframes, cfg)

  frames_to_video(dst_path, os.path.abspath('otmp'))

  shutil.rmtree(os.path.abspath('itmp'))
  shutil.rmtree(os.path.abspath('otmp'))


if __name__ == "__main__":
  
  parser = argparse.ArgumentParser(description='Stylize a video')
  
  parser.add_argument('-s', '--source',      help='video source')
  parser.add_argument('-d', '--destination', help='video destination')
  parser.add_argument('-c', '--config',      help='style config',     default='{}')
  parser.add_argument('-u', '--uuid',        help='instance uuid',    default=1)

  args = parser.parse_args()

  main(args.source, args.destination, eval(args.config), args.uuid)