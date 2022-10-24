import sys
import numpy as np
import cv2
import datetime as dt
from playsound import playsound


def return_today():
    year = dt.datetime.now().year
    month = dt.datetime.now().month
    day = dt.datetime.now().day
    hour = dt.datetime.now().hour
    minute = dt.datetime.now().minute
    second = dt.datetime.now().second
        
    return str(year) + "_"  + str(month) + "_" +\
           str(day) + "_"  + str(hour) + "_"  +\
           str(minute) + "_"  + str(second)


def pencil_sketch(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
    blr = cv2.GaussianBlur(gray, (0, 0), 3)
    dst = cv2.divide(gray, blr, scale=255)
    return dst


def canny(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
    dst = cv2.Canny(gray, 50, 150)
    return dst


def sobel(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
    dx = cv2.Sobel(gray, ddepth=cv2.CV_64F , dx= 1, dy= 0)
    dy = cv2.Sobel(gray, ddepth=cv2.CV_64F , dx= 0, dy= 1)
    dst = cv2.addWeighted(src1 = dx, alpha = 0.5, src2 = dy, beta = 0.5, gamma=5)
    return dst



def wear_hat(img, file):
    img2 = cv2.imread(file)
    img2 = cv2.resize(img2, (200, 100))

    #x_offset = img.shape[1] - img2.shape[1]
    #y_offset = img.shape[0] - img2.shape[0]

    x_offset = 200
    y_offset = 100

    roi = img[y_offset:(img.shape[0]-280), x_offset:(img.shape[1]-240)]

    img2_gray = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    img2_mask = cv2.bitwise_not(img2_gray)

    fg = cv2.bitwise_or(img2, img2, mask=img2_mask)

    #print(roi.shape, fg.shape, img2.shape, img.shape)

    final_roi = cv2.bitwise_or(roi, fg)

    img[y_offset:y_offset + img2.shape[0], x_offset:x_offset + img2.shape[1]] = final_roi
    return img



def cam_filter(cam_mode, frame):
    if cam_mode == 1:
        frame = pencil_sketch(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    if cam_mode == 2:
        frame = canny(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    
    if cam_mode == 3:
        frame = sobel(frame)
        #frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    if cam_mode == 4:
        frame = wear_hat(frame, './santa.png')

    if cam_mode == 5:
        frame = wear_hat(frame, './red_hat.jpg')

    if cam_mode == 6:
        frame = wear_hat(frame, './pig.png')

    if cam_mode == 7:
        frame = wear_hat(frame, './crawn.png')

    if cam_mode == 8:
        frame = wear_hat(frame, './megame.jpg')

    if cam_mode == 9:
        frame = wear_hat(frame, './mask.jpeg')

    if cam_mode == 10:
        frame = wear_hat(frame, './아이유.jpg')

    if cam_mode == 11:
        frame = wear_hat(frame, './copy.png')
    return frame



# main
cap = cv2.VideoCapture(0)
cam_mode = 0

if not cap.isOpened():
    print("video open failed!")
    sys.exit()

if cap.isOpened():
    #https://koreapy.tistory.com/1186
    fps = 30.0 # FPS, 초당 프레임 수
    fourcc = cv2.VideoWriter_fourcc(*'DIVX') # 인코딩 포맷 문자
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size = (int(width), int(height))


while True:
    ret, frame = cap.read()
    frame = cam_filter(cam_mode, frame)

    if not ret:
        break


    cv2.imshow('frame', frame)

    key=cv2.waitKey(1)

    if key == 27:
        break


    if key == ord('s'):
        file_path_pic = './picture/' + return_today() + '.jpg'
        img_captured = cv2.imwrite(file_path_pic, frame)
        camera_on = 0
        print("캡처를 완료했습니다.")
        playsound("./iphone.mp3")
        cv2.waitKey(200)
       
    if key == ord('k'):
        playsound("./video_start.mp3")
        file_path_avi = './picture/' + return_today() + '.avi'
        
        out = cv2.VideoWriter(file_path_avi, fourcc, fps, size) # VideoWriter 객체 생성
        while True:
            ret_reco, frame_reco = cap.read()
            frame_reco = cam_filter(cam_mode, frame_reco)
           
            print("녹화중입니다.")
            if ret_reco:
                out.write(frame_reco)

                if cv2.waitKey(int(1000/fps)) == ord('k'):
                    playsound("./video_end.wav")
                    print("녹화를 중지합니다.")
                    break

            else: 
                print("no frame!")
                break

            cv2.putText(frame_reco,"Recoding..",(0, 30),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255))
            cv2.imshow('frame', frame_reco)

        out.release()
        cv2.waitKey(300)


    if key == ord(' '):
        print(cam_mode)
        cam_mode += 1
        if cam_mode == 12:
            cam_mode = 0


cap.release()
cv2.destroyAllWindows()
