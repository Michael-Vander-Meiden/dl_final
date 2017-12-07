#!/usr/bin/env python3

import evaluate

import numpy as np
from PIL import Image


def crop_frames(iframes, cframes, boxes):
    [Image.fromarray(np.asarray(Image.open(iframes[i]))[boxes[i][0]:boxes[i][2],boxes[i][1]:boxes[i][3],:]).save(cframes[i])
        for i in range(len(iframes))]

def stylize_frames(iframes, sframes, ckpt):
    evaluate.ffwd_different_dimensions(iframes, sframes, ckpt, batch_size=1)

def blend_frames(iframes, cframes, oframes, boxes, masks):
    for i in range(len(iframes)):
        sframe = np.zeros_like(iframes[i])
        sframe[boxes[i][0]:boxes[i][2],boxes[i][1]:boxes[i][3],:] = cframes[i]
        Image.composite(iframes[i], sframe, masks[i]).save(oframes[i])
