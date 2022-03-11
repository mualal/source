import cv2
import os
# import dlib

cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
face_cascade = cv2.CascadeClassifier(os.path.join(cv2_base_dir, 'data', 'haarcascade_frontalface_default.xml'))
eye_cascade = cv2.CascadeClassifier(os.path.join(cv2_base_dir, 'data', 'haarcascade_eye.xml'))

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while capture.isOpened():
    success, frame = capture.read()
    frame = cv2.flip(frame, 1)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    """
    faces = face_cascade.detectMultiScale(frame_gray, 1.3, 5)
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = frame[y:y+h, x:x+h]
        face_gray = frame_gray[y:y+h, x:x+h]
        eyes = eye_cascade.detectMultiScale(face_gray)
        for (x2, y2, w2, h2) in eyes:
            cv2.rectangle(face, (x2, y2), (x2+w2, y2+h2), (0, 255, 0), 2)

    cv2.imshow('Обнаружение лица и глаз', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # cv2.imshow('frame_gray', frame_gray)
    """
    _, threshold = cv2.threshold(frame_gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        cv2.drawContours(frame, [contour], 0, (255, 0, 0), 1)

        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])

    cv2.imshow('shapes', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
