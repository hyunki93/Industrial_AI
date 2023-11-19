import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2


# 영상 불러오기
#src1 = cv2.imread('graf1.png', cv2.IMREAD_GRAYSCALE)
#src2 = cv2.imread('graf3.png', cv2.IMREAD_GRAYSCALE)
src1 = cv2.imread('./origin.png',cv2.IMREAD_GRAYSCALE)
src2 = cv2.imread('./target.png',cv2.IMREAD_GRAYSCALE)

if src1 is None or src2 is None:
    sys.exit()

feature = cv2.KAZE_create()

# 특징점 검출 및 기술자 계산
kp1, desc1 = feature.detectAndCompute(src1, None)
kp2, desc2 = feature.detectAndCompute(src2, None)

# 특징점 매칭
matcher=cv2.BFMatcher_create()
# matcher=cv2.BFMatcher_create(cv2.NORM_HAMMING)
matches=matcher.match(desc1,desc2)

matches=sorted(matches,key=lambda x: x.distance)
good_matches=matches[:80]


pts1=np.array([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2).astype(np.float32)    #(80,2)
pts2=np.array([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2).astype(np.float32)

H,_=cv2.findHomography(pts1,pts2,cv2.RANSAC)

# 호모그래피를 이용하여 기준 영상 영역 표시
dst=cv2.drawMatches(src1,kp1,src2,kp2,good_matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

(h,w)=src1.shape[:2]
corners1=np.array([[0,0],[0,h-1],[w-1,h-1],[w-1,0]]).reshape(-1,1,2).astype(np.float32)
corners2=cv2.perspectiveTransform(corners1,H)

corners2=corners2 + np.float32([w,0])

cv2.polylines(dst,[np.int32(corners2)],True,(0,255,0),2,cv2.LINE_AA)

cv2.namedWindow('result')
cv2.imshow('result',dst)
cv2.waitKey()
cv2.destroyAllWindows()

# plt.figure(figsize=(5, 5))
#
# plt.subplot(222)
# plt.title('right')
# plt.imshow(dst)
#
#
# plt.show()