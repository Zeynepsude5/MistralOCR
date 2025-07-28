import cv2

img = cv2.imread("resized_118.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
resized = cv2.resize(gray, (0,0), fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
cv2.imwrite("resized1_118.jpg", resized)
