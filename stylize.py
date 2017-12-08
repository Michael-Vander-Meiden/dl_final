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
    import pdb
    pdb.set_trace()
    for i in range(len(iframes)):
        iframe = np.copy(np.asarray(Image.open(iframes[i])))
        cframe = np.copy(np.asarray(Image.open(cframes[i])))
        iframe[boxes[i][0]:boxes[i][2],boxes[i][1]:boxes[i][3],:] = cframe[0:boxes[i][2]-boxes[i][0],0:boxes[i][3]-boxes[i][1],:]
        Image.fromarray(iframe).save(oframes[i])
