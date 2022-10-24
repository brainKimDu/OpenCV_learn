import cv2
import numpy as np
import sys

# 좌표값
oldx = oldy = -1
color = (0, 0, 255)


# 마우스 이벤트에 관한 함수의 집합
def on_mouse(event, x, y, flags, param):
    global oldx, oldy, color

	# 왼쪽버튼이 눌리는 동안
	if event == cv2.EVENT_LBUTTONDOWN:
		# 눌린좌표값을 저장합니다.
		oldx, oldy = x, y
		print('EVENT_LBUTTONDOWN: %d, %d' % (x, y))


	
		# 왼쪽버튼이 때인 순간
		elif event == cv2.EVENT_LBUTTONUP:
		#좌표값을 프린트합니다.
			print('EVENT_LBUTTONUP: %d, %d' % (x, y))

		if flags & cv2.EVENT_FLAG_SHIFTKEY:
			cv2.circle(img, (oldx, oldy), oldx-x, color , -1)
			cv2.imshow('image', img)

		# 눌리고 마우스가 움직이는 동안
		elif event == cv2.EVENT_MOUSEMOVE:
			# flag의 값과 L버튼이 눌려져 있는 상태의 값의 and연산을 실행합니다.

			# 조건문이 없다면 왼쪽 버튼을 누르지 않아도 그림이 그려진다 -> 내 추측으로는 마우스가 눌려져 있는 상황인지 판단을 해야한다.
		if (flags & cv2.EVENT_FLAG_LBUTTON):
			if not (flags & cv2.EVENT_FLAG_SHIFTKEY):
			# 직선을 그리는 것으로 그림을 그릴 수 있게 만든다.
				cv2.line(img, (oldx, oldy), (x, y), color , 4, cv2.LINE_AA)
				cv2.imshow('image', img)
				oldx, oldy = x, y


img = cv2.imread("./사진", cv2.IMREAD_COLOR)

cv2.namedWindow('image')


while True:
cv2.setMouseCallback('image', on_mouse)
cv2.imshow('image', img)

if cv2.waitKey() == ord('b'):
color = (255, 0, 0)
if cv2.waitKey() == ord('r'):
color = (0, 0, 255)
if cv2.waitKey() == ord('g'):
color = (0, 255, 0)

if cv2.waitKey() == 27:
break

cv2.destroyAllWindows()