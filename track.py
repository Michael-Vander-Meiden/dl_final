#!/usr/bin/env python3

import numpy as np
import numpy.linalg
def select_detection(detections, uuid):
    idx = min(uuid, len(detections['masks'])-1)
    return detections['masks'][:,:,idx], detections['rois'][idx]

def filter_detection(detections, box, mask):
    target = np.array([box[2]-box[0], box[3]-box[1]])

    candidates = [np.array([new_box[2]-new_box[0], new_box[3]-new_box[1]])
                    for new_box in detections['rois']]

    errors = [np.linalg.norm(target-candidate)
                for candidate in candidates]

    if len(errors) > 0:
        idx = np.argmin(errors)

        return detections['masks'][:,:,idx], detections['rois'][idx]
    else:
        return mask, box
