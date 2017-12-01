#!/usr/bin/env python3

import numpy as np
import numpy.linalg

def select_detection(detections, uuid):
	masks[min(uuid, len(masks)-1])

def filter_detection(detections, box):
	target = np.array([box[2]-box[0], box[3]-box[1]])

	candidates = [np.array([new_box[2]-new_box[0], new_box[3]-new_box[1]])
					for new_box in detections['boxes']]

	errors = [np.linalg.norm(target-candidate)
				for candidate in candidates]

	dx = np.argmin(errors)

	return detections['masks'][idx], detections['masks'][idx]
