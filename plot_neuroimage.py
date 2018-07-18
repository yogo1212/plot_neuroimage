#!/usr/bin/python

import sys

if len(sys.argv) < 2:
	print("need at least a filename")
	sys.exit()

import nibabel as nib
import matplotlib.pyplot as plt

def pinfo(shape):
	print("these are the dimensions of the file:")
	print(shape)
	print("i can draw slices when you give me dimension and a position:")
	print(f'     {sys.argv[0]:s} [filename] [dimension+position]..')
	print(f'e.g. {sys.argv[0]:s} {sys.argv[1]:s} X{shape[0]//2:d} Y{shape[1]//2:d} Z{shape[2]//2:d}..')

def show_slices(slices):
	fig, axes = plt.subplots(1, len(slices))
	# it seems, pyplot is 'smart' and returns a single object without an array when the length is 1
	if len(slices) == 1:
		axes = [axes]
	for i, s in enumerate(slices):
		axes[i].imshow(s.T, cmap="gray", origin="lower")

n = nib.load(sys.argv[1])
fdata = n.get_fdata()

def select_slice(arg):
	p = int(arg[1:])
	return {
		'X': fdata[p, :, :],
		'Y': fdata[:, p, :],
		'Z': fdata[:, :, p],
	}.get(arg[0])

if len(sys.argv) == 2:
	pinfo(fdata.shape)
	sys.exit()
else:
	s = list(map(select_slice, sys.argv[2:]))
	show_slices(s)

plt.show()
