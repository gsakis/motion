import numpy as np
import cv2
import pdb
import time

cap = cv2.VideoCapture('Highway2.m4v')
#cap = cv2.VideoCapture('footage3.mp4')

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.01,
                       minDistance = 15,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))

mog = cv2.BackgroundSubtractorMOG()

def findGoodFeatures (old_gray):
    # ret, old_frame = cap.read()
    #old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    return p0, old_gray



# Take first frame and find corners in it
p0 = None

# pdb.set_trace()

while p0 == None:
    ret, old_frame = cap.read()
    mog_image  = mog.apply(old_frame)
    p0, old_gray = findGoodFeatures (mog_image)
    # oldHist = cv2.calcHist([old_gray], [0], None,[256], [0,256])
    # print p0
    # print type(p0)



# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
# newHist = oldHist


while(1):
    
    # pdb.set_trace();
    Flag = False;
    # main_time = time.time()
    ret,frame = cap.read()
    # print time.time() - main_time
    if ret == False:
        break;
    
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame_gray  = mog.apply(frame)
    
    enter_left = frame_gray[:,0]


    # print enter_left > 0;

    # for i in enter_left:
    #     if enter_left[i] > 0:
    #         flag = 1;
    #         break;
    # pdb.set_trace()
    Flag = any(enter_left > 0)
    # oldHist = newHist
    # newHist = cv2.calcHist([frame_gray], [0], None,[256], [0,256])
    # diff = cv2.compareHist(oldHist, newHist, 3)

    # calculate optical flow
    if (p0.size < 10 or Flag):
        
        p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
        # p0 = np.concatenate((p0,temp))
        mask = np.zeros_like(old_frame)

    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # print "p0 = " + str(p0.size)
    # print "p1 = " + str(p1.size)

    # Select good points
    # pdb.set_trace();
    good_new = p1[st==1]
    good_old = p0[st==1]

    # draw the tracks
    
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        # if (abs(a-c) > 0.1 and abs(b-d) > 0.1):

        cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
    
    #print type(frame)
    #print type(mask)
    img = cv2.add(frame,mask)

    cv2.imshow('frame',img)
    # print frame_gray.shape
    
    k = cv2.waitKey(1)
    if k == 27:
        break
   
    # Now update the previous frame and previous points
    old_gray = frame_gray
    p0 = good_new.reshape(-1,1,2)
    
    
   

cv2.destroyAllWindows()
cap.release()