#!/usr/bin/env python3

import evaluate

def stylize_frame(iframes, masks, oframes, cfg):

    evaluate.ffwd(iframes, oframes, cfg['ckpt'], batch_size=cfg.setdefault('batch_size', 4))
