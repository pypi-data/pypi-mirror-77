import numpy as np
import scipy
from scipy import ndimage
from PIL import Image
import matplotlib.pyplot as plt

def add_countor(In, Seg, Color=(0, 255, 0)):
    Out = In.copy()
    [H, W] = In.size
    for i in range(H):
        for j in range(W):
            if(i==0 or i==H-1 or j==0 or j == W-1):
                if(Seg.getpixel((i,j))!=0):
                    Out.putpixel((i,j), Color)
            elif(Seg.getpixel((i,j))!=0 and  \
                 not(Seg.getpixel((i-1,j))!=0 and \
                     Seg.getpixel((i+1,j))!=0 and \
                     Seg.getpixel((i,j-1))!=0 and \
                     Seg.getpixel((i,j+1))!=0)):
                     Out.putpixel((i,j), Color)
    return Out

def add_segmentation(image, seg_name, Color=(0, 255, 0)):
    seg = Image.open(seg_name).convert('L')
    seg = np.asarray(seg)
    if(image.size[1] != seg.shape[0] or image.size[0] != seg.shape[1]):
        print('segmentation has been resized')
        seg = scipy.misc.imresize(seg, (image.size[1], image.size[0]), interp='nearest')
    strt = ndimage.generate_binary_structure(2, 1)
    seg = np.asarray(ndimage.morphology.binary_opening(seg, strt), np.uint8)
    seg = np.asarray(ndimage.morphology.binary_closing(seg, strt), np.uint8)
    img_show = add_countor(image, Image.fromarray(seg), Color)
    strt = ndimage.generate_binary_structure(2, 1)
    seg = np.asarray(ndimage.morphology.binary_dilation(seg, strt), np.uint8)
    img_show = add_countor(img_show, Image.fromarray(seg), Color)
    return img_show