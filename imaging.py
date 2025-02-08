#The hueshifting code is taken from StackOverflow user Mark Ransom
#https://stackoverflow.com/questions/7274221/changing-image-hue-with-python-pil

from math import floor

import numpy as np
from PIL import Image


def rgb_to_hsv(rgb):
    # Translated from source of colorsys.rgb_to_hsv
    # r,g,b should be a numpy arrays with values between 0 and 255
    # rgb_to_hsv returns an array of floats between 0.0 and 1.0.
    rgb = rgb.astype('float')
    hsv = np.zeros_like(rgb)
    # in case an RGBA array was passed, just copy the A channel
    hsv[..., 3:] = rgb[..., 3:]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.max(rgb[..., :3], axis=-1)
    minc = np.min(rgb[..., :3], axis=-1)
    hsv[..., 2] = maxc
    mask = maxc != minc
    hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
    rc = np.zeros_like(r)
    gc = np.zeros_like(g)
    bc = np.zeros_like(b)
    rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
    gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
    bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
    hsv[..., 0] = np.select(
        [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
    hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
    return hsv

def hsv_to_rgb(hsv):
    # Translated from source of colorsys.hsv_to_rgb
    # h,s should be a numpy arrays with values between 0.0 and 1.0
    # v should be a numpy array with values between 0.0 and 255.0
    # hsv_to_rgb returns an array of uints between 0 and 255.
    rgb = np.empty_like(hsv)
    rgb[..., 3:] = hsv[..., 3:]
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    i = (h * 6.0).astype('uint8')
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    conditions = [s == 0.0, i == 1, i == 2, i == 3, i == 4, i == 5]
    rgb[..., 0] = np.select(conditions, [v, q, p, p, t, v], default=v)
    rgb[..., 1] = np.select(conditions, [v, v, v, q, p, p], default=t)
    rgb[..., 2] = np.select(conditions, [v, p, t, v, v, q], default=p)
    return rgb.astype('uint8')

def rgb_to_hex(r,g,b):
    return f"#{r:02x}{g:02x}{b:02x}".upper()

def red_shift(hue,rgb=(255,0,0)):
    # Define base color in RGB
    red_rgb = np.array([*rgb, 255], dtype=np.uint8)  # Including alpha channel
    
    # Convert RGB to HSV
    red_hsv = rgb_to_hsv(red_rgb[np.newaxis, np.newaxis, :])  # Expand dims for compatibility
    
    # Apply the hue shift
    red_hsv[0, 0, 0] = (red_hsv[0, 0, 0] + hue / 360.0) % 1.0
    
    # Convert back to RGB
    shifted_rgb = hsv_to_rgb(red_hsv)[0, 0, :3]  # Remove alpha channel for RGB
    
    # Convert RGB to hex
    r, g, b = shifted_rgb
    return r, g, b

def shift(image,hue):
    hue = hue/360.0

    arr = np.array(image)

    hsv=rgb_to_hsv(arr)
    hsv[...,0]=hue

    rgb=hsv_to_rgb(hsv)
    new_image = Image.fromarray(rgb, 'RGBA')

    hsv[...,0]=hue

    return new_image

def scale(image:Image.Image,scale):
    width,height = image.size
    width *= scale
    height *= scale
    
    width = floor(width)
    height = floor(height)
    return image.resize((width,height),Image.Resampling.NEAREST)