import sys
import numpy as np
import cv2



def pencil_sketch(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
    blr = cv2.GaussianBlur(gray, (0, 0), 3)
    dst = cv2.divide(gray, blr, scale=255)
    return dst

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("열리지 않아요")
    sys.exit()

cam_mode = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    elif cam_mode == 2:
        frame = pencil_sketch(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)

    if key == 27:
        break

    elif key == ord(' '):
        cam_mode += 1
        if cam_mode == 3:
            cam_mode = 0

cap.release()
cv2.destroyAllWindows()