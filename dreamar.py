#!/usr/bin/env python3

import os
import sys
import shutil
import argparse 

import ffmpy

import identify
import track
import stylize
import time 


__FPS__ = '1'

def video_to_frames(video_path, tmp):
  images_name = '.'.join(video_path.split('/')[-1].split('.')[:-1])

  codec = ffmpy.FFmpeg(inputs={video_path: None}, outputs={tmp+'/'+images_name+'_%04d.jpg': '-y -vf fps='+__FPS__})

  codec.run()

def frames_to_video(video_path, tmp):
  images_name = '.'.join(os.listdir(tmp)[0].split('/')[-1].split('_')[:-1])

  codec = ffmpy.FFmpeg(inputs={tmp+'/'+images_name+'_%04d.jpg': '-r '+__FPS__}, outputs={video_path: '-c:v libx264 -vf fps='+__FPS__})

  codec.run()

def main(src_path, dst_path, cfg, uuid):

  if os.path.exists(os.path.abspath('itmp')):
    shutil.rmtree(os.path.abspath('itmp'))
  os.makedirs(os.path.abspath('itmp'))

  if os.path.exists(os.path.abspath('otmp')):
    shutil.rmtree(os.path.abspath('otmp'))
  os.makedirs(os.path.abspath('otmp'))

  if os.path.exists(os.path.abspath('ctmp')):
    shutil.rmtree(os.path.abspath('ctmp'))
  os.makedirs(os.path.abspath('ctmp'))

  if os.path.exists(os.path.abspath('stmp')):
    shutil.rmtree(os.path.abspath('stmp'))
  os.makedirs(os.path.abspath('stmp'))

  if os.path.exists(os.path.abspath(dst_path)):
    os.remove(os.path.abspath(dst_path))

  video_to_frames(src_path, os.path.abspath('itmp'))

  iframes = sorted(['itmp/' + iframe for iframe in os.listdir('itmp')])
  oframes = [iframe.replace('itmp', 'otmp') for iframe in iframes]
  cframes = [iframe.replace('itmp', 'ctmp') for iframe in iframes]
  sframes = [iframe.replace('itmp', 'stmp') for iframe in iframes]

  print(iframes)

  all_detections = identify.get_detections(iframes)

  masks = []
  boxes = []

  for i, i_detections in enumerate(all_detections):
    print(i)
    if i == 0:
      mask, box = track.select_detection(i_detections, uuid)
    else:
      mask, box = track.filter_detection(i_detections, box, mask)

    masks.append(mask)
    boxes.append(box)

  start = time.time()

  if cfg["order"] == "crop-style":
    stylize.crop_frames(iframes, cframes, boxes)
    stylize.stylize_frames(cframes, sframes, cfg['ckpt'])
    stylize.blend_frames(iframes, sframes, oframes, boxes, masks)
  elif cfg["order"] == "style-crop":
    stylize.stylize_frames(iframes, sframes, cfg['ckpt'])
    stylize.crop_frames(sframes, cframes, boxes)
    stylize.blend_frames(iframes, cframes, oframes, boxes, masks)
  else:
    raise Exception("madafaka")

  frames_to_video(dst_path, os.path.abspath('otmp'))

  shutil.rmtree(os.path.abspath('itmp'))
  #shutil.rmtree(os.path.abspath('otmp'))
  shutil.rmtree(os.path.abspath('ctmp'))
  shutil.rmtree(os.path.abspath('stmp'))
  print(" the time it took was")
  print (time.time() - start)

if __name__ == "__main__":

  # git pull && python dreamar.py -s dogs.mp4 -d sdogs.mp4 -c '{"ckpt":"../fast-style-transfer/la_muse.ckpt", "order":"crop-style"}'
  
  parser = argparse.ArgumentParser(description='Stylize a video')
  
  parser.add_argument('-s', '--source',      help='video source')
  parser.add_argument('-d', '--destination', help='video destination')
  parser.add_argument('-c', '--config',      help='style config',     default='{}')
  parser.add_argument('-u', '--uuid',        help='instance uuid',    default=0)

  args = parser.parse_args()

  main(args.source, args.destination, eval(args.config), args.uuid)