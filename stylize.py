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
        cframe = np.zeros_like(iframe, dtype=np.uint8)
        oframe = np.zeros_like(iframe, dtype=np.uint8)
        cframe[boxes[i][0]:boxes[i][2],boxes[i][1]:boxes[i][3],:] = np.copy(np.asarray(Image.open(cframes[i])))[0:boxes[i][2]-boxes[i][0],0:boxes[i][3]-boxes[i][1],:]
        for jj in range(3):
            oframe[:,:,jj] = iframe[:,:,jj] * (masks[i] <= 0) + cframe[:,:,jj] * (masks[i] > 0)
            #oframe[:,:,jj] = cframe[:,:,jj] * (masks[i] > 0)
        Image.fromarray(oframe).save(oframes[i])
