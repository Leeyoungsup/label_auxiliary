import cv2
import sys
import numpy as np

src = cv2.imread('../../data/1.png')
src = cv2.resize(src, (640, 400))

if src is None:
    print('Image load failed!')
    sys.exit()

mask = np.zeros(src.shape[:2], np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
iterCount = 1
mode = cv2.GC_INIT_WITH_RECT
rc = cv2.selectROI(src)
cv2.grabCut(src, mask, rc, bgdModel, fgdModel, iterCount, mode)

mask2 = np.where((mask == cv2.GC_BGD) | (
    mask == cv2.GC_PR_BGD), 0, 1).astype(np.uint8)
print(mask)
dst = src*mask2[:, :, np.newaxis]

cv2.imshow('dst', dst)


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(dst, (x, y), 3, (255, 0, 0), -1)
        cv2.circle(mask, (x, y), 3, cv2.GC_FGD, -1)
        cv2.imshow('dst', dst)
    elif event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(dst, (x, y), 3, (0, 0, 255), -1)
        cv2.circle(mask, (x, y), 3, cv2.GC_BGD, -1)
        cv2.imshow('dst', dst)
    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:
            cv2.circle(dst, (x, y), 3, (255, 0, 0), -1)
            cv2.circle(mask, (x, y), 3, cv2.GC_FGD, -1)
            cv2.imshow('dst', dst)
        elif flags & cv2.EVENT_FLAG_RBUTTON:
            cv2.circle(dst, (x, y), 3, (0, 0, 255), -1)
            cv2.circle(mask, (x, y), 3, cv2.GC_BGD, -1)
            cv2.imshow('dst', dst)


cv2.setMouseCallback('dst', on_mouse)

while True:
    key = cv2.waitKey()

    if key == 13:  # ENTER

        cv2.grabCut(src, mask, rc, bgdModel, fgdModel,
                    1, cv2.GC_INIT_WITH_MASK)
        mask2 = np.where((mask == cv2.GC_BGD) | (
            mask == cv2.GC_PR_BGD), 0, 1).astype(np.uint8)
        dst = src * mask2[:, :, np.newaxis]
        cv2.imshow('dst', dst)

    elif key == 27:  # ESC
        break

cv2.destroyAllWindows()
