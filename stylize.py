#!/usr/bin/env python3

import evaluate
from PIL import Image


def crop_frames(iframes, oframes, boxes):
	import pdb
	pdb.set_trace()
	for i, iframe in enumerate(iframes):
		iimg = Image.open(iframe)


def stylize_frames(iframes, oframes, ckpt):
    evaluate.ffwd_different_dimensions(iframes, oframes, ckpt, batch_size=1)
