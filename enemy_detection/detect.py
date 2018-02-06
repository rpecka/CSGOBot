
import cv2


def detect_person(image):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    resized_image = cv2.resize(image, (480, 270))
    rects, weights = hog.detectMultiScale(resized_image, winStride=(4, 4), padding=(8, 8), scale=1.05)
    return rects, weights

def draw_boxes(image):
    rects, weights = detect_person(image)
    orig = image.copy()
    for x, y, h, w in rects:
        cv2.rectangle(orig, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv2.imshow('neat', orig)
    cv2.waitKey(0)