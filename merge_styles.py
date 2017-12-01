from PIL import Image
import numpy as np
import numpy.matlib as mtl
import pdb
import sys

if len(sys.argv) == 2:
	idx = int(sys.argv[1])
else:
	idx = 0

print(idx)

results = np.load('results.npz')

masks = results['masks']

image = Image.open('doggies.jpg')
style_image = Image.open('output_images/shutterstock_51472228-760x432.jpg')

image = np.array(image)
style_image = np.array(style_image)

mask = masks[:,:,idx][:,:,np.newaxis]

masked_image = np.zeros(image.shape)
masked_image += image*(1-mask)
masked_image += style_image*mask
masked_image = masked_image.astype(np.uint8)

test = Image.fromarray(masked_image,'RGB')

test.show()