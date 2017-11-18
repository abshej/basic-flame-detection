#author: Avadhoot S
"""
program for detecting flames in image frames
using three colorspace thresholding
threshold values obtained using experimentation and are not universal
adaptive thresholding is suggested for eliminating false positives
"""
import cv2 #opencv2
import numpy as np
import matplotlib.pyplot as plt
import sys 

frame = cv2.cvtColor(cv2.imread(str(sys.argv[1]), -1), cv2.COLOR_BGR2RGB) #standard bgr converted to rgb beforehand
#framegr = cv2.imread(str(sys.argv[1]), 0) #grayscale frame

#median blurring frame
#frame = cv2.medianBlur(frame, 3)
    
#ycbcr thresholding
framey = cv2.cvtColor(frame, cv2.COLOR_RGB2YCR_CB) #rgb to ycbcr conversion

lower_y = np.array([230,120,60])
upper_y = np.array([300,300,150])
thres_mask_y = cv2.inRange(framey, lower_y, upper_y) #obtaining binary
bit_mask_y = cv2.bitwise_and(framey, framey, mask= thres_mask_y) #obtaining masked image

#rgb thresholding
lower_red = np.array([230,200,40])
upper_red = np.array([300,300,150])
thres_mask_red = cv2.inRange(frame, lower_red, upper_red)
bit_mask_rgb = cv2.bitwise_and(frame, frame, mask= thres_mask_red)


#hsv thresholding
hsv_edit = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.uint8) 

lower_blue = np.array([4,100,255])
upper_blue = np.array([70,300,300])
thres_mask = cv2.inRange(hsv_edit, lower_blue, upper_blue)
bit_mask_hsv = cv2.bitwise_and(frame,frame, mask= thres_mask)
bit_mask_hsvnrgb = cv2.bitwise_or(thres_mask, thres_mask_red)
bit_mask_three = cv2.bitwise_and(bit_mask_hsvnrgb, thres_mask_y)

plt.subplot(121), plt.imshow(frame)
plt.title('frame'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(bit_mask_three)
plt.title('res_mix'), plt.xticks([]), plt.yticks([])
plt.show()

#decision making regarding detection
n = cv2.countNonZero(bit_mask_three)
print n
print frame.size
if float(n)/float(frame.size) > 0.0005: #need to change
   print "flame detected"
else:
   print "no flame"    

#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break

#feed_cap.release()