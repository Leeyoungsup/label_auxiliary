import cv2
import numpy as np

# 콜백 함수: 마우스로 드래그하여 박스를 설정


def draw_rectangle(event, x, y, flags, param):
    global x_init, y_init, drawing, top_left_pt, bottom_right_pt

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_init, y_init = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            top_left_pt, bottom_right_pt = (x_init, y_init), (x, y)
            img_copy = img.copy()
            cv2.rectangle(img_copy, top_left_pt,
                          bottom_right_pt, (0, 255, 0), 2)
            cv2.imshow('image', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        top_left_pt, bottom_right_pt = (x_init, y_init), (x, y)
        img_copy = img.copy()
        cv2.rectangle(img_copy, top_left_pt, bottom_right_pt, (0, 255, 0), 2)
        cv2.imshow('image', img_copy)


# 이미지 불러오기
img = cv2.imread('../../data/aaa.png')
img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_AREA)
img_copy = img.copy()
cv2.imshow('image', img)

# 변수 초기화
drawing = False
top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)

# 마우스 이벤트 설정
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rectangle)

cv2.waitKey(0)
cv2.destroyAllWindows()

# 선택한 영역 추출
roi = img[top_left_pt[1]:bottom_right_pt[1], top_left_pt[0]:bottom_right_pt[0]]

# 그레이스케일 변환 및 블러 적용
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Canny Edge Detection 적용
edges = cv2.Canny(blurred, 50, 150)

# 윤곽선 검출
contours, _ = cv2.findContours(
    edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 원본 이미지에 윤곽선 그리기
cv2.drawContours(roi, contours, -1, (0, 255, 0), 2)

# 결과 이미지 출력
cv2.imshow('Contours', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
