import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import time

firstRun = True
i = 275 #set score

time.sleep(3)
while i>0:

    img = ImageGrab.grab()
    img_numpy = np.array(img, dtype='uint8')
    if firstRun:
        print("In the next window select the block on interest from the game,please refer to image")
        r = cv2.selectROI(img_numpy)
        print("Done setting screen")
        time.sleep(3)
        firstRun = False
        print("Lets play!")
    imCrop = img_numpy[int(r[1]):int(r[1]+r[3]),  int(r[0]):int(r[0]+r[2])]
    gray = cv2.cvtColor(imCrop, cv2.COLOR_BGR2GRAY)
    if gray[1,1] < 170 and gray[1,1] > 120: #green winning screen
        print("We won!")
        break
ret, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV) #set threshold for identifying black tiles
    thresh = cv2.erode(thresh, None, iterations=5)
    im, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    num = 0
    for c in contours:
        topMost = tuple(c[c[:,:,1].argmin()][0])
        bottomMost = tuple(c[c[:,:,1].argmax()][0])

        if bottomMost[1]-topMost[1] < 50:
                continue
        pointX = int(bottomMost[0])
        pointY = int(bottomMost[1])

        realX = pointX + r[0]+50
        realY = pointY + r[1]-50
        print("[%d/%d] Tile at %d,%d" %(score,score+1-i,realX,realY))
        pyautogui.click(x=realX, y=realY)
        time.sleep(0.01)
        i=i-1


