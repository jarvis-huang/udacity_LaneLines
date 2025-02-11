#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
#matplotlib inline

#reading in an image
image = mpimg.imread('test_images/solidWhiteRight.jpg')

#printing out some stats and plotting
print('This image is:', type(image), 'with dimensions:', image.shape)
plt.imshow(image)  # if you wanted to show a single color channel image called 'gray', for example, call as plt.imshow(gray, cmap='gray')

import math

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def color_select(img, color):
    mask = (img[:,:,0] < color[0]) & (img[:,:,1] < color[1]) & (img[:,:,2] < color[2])
    img_out = np.copy(img)
    img_out[mask] = [0,0,0]
    return img_out
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    NOTE: this is the function you might want to use as a starting point once you want to 
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).  
    
    Think about things like separating line segments by their 
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of 
    the lines and extrapolate to the top and bottom of the lane.
    
    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, a=0.8, b=1., c=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * a + img * b + c
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, a, img, b, c)
    
import os
os.listdir("test_images/")

# for color select
color_sel = [200,200,200]
# for Gaussian blur
kernel_size = 3
# for canny
low_threshold = 50
high_threshold = 100
# for ROI
roi_vertices = np.array([[[460,310],[500,310],[959,539],[0,539]]])
# for Hough Transform
rho = 1 # if set to 1, reflectors will be detected
theta = math.radians(1) # if set to 2, too many broken lines
threshold = 10
min_line_len = 10
max_line_gap = 15
# for weighted image
a = 0.8
b = 1.0

f = os.listdir("test_images/")[0]
print(f)
img = mpimg.imread(os.path.join("test_images",f))
img_color_sel = color_select(img, color_sel)
img_gray = grayscale(img_color_sel)
img_gaussian = gaussian_blur(img_gray, kernel_size)
img_canny = canny(img_gaussian, low_threshold, high_threshold)
img_canny_filtered = region_of_interest(img_canny, roi_vertices)
img_canny_roi = cv2.polylines(cv2.cvtColor(img_canny, cv2.COLOR_GRAY2RGB), roi_vertices, isClosed=True, color=[0, 255, 0], thickness=2)
img_line = hough_lines(img_canny_filtered, rho, theta, threshold, min_line_len, max_line_gap)
img_final = weighted_img(img_line, img, a, b, 0)

'''
ax = plt.subplot(2, 2, 1)
plt.imshow(img)
ax.set_title("original")
ax = plt.subplot(2, 2, 2)
plt.imshow(img_canny, cmap='gray')
ax.set_title("Canny Edges")
ax = plt.subplot(2, 2, 3)
plt.imshow(img_canny_roi)
ax.set_title("Region of Interest")
ax = plt.subplot(2, 2, 4)
plt.imshow(img_line)
ax.set_title("Hough Transform")
'''

plt.imshow(img_final)
plt.show()
