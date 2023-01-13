"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import socket
import time
import cv2
from gaze_tracking import GazeTracking


def connect_bt(mac_address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((mac_address, port))
    return s


def get_eye_pos(gaze):
    webcam = cv2.VideoCapture(0)

    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_right():
            text = "Looking right"
            yield 'R'
        elif gaze.is_left():
            text = "Looking left"
            yield 'L'
        elif gaze.is_up():
            text = "Looking up"
            yield 'U'
        elif gaze.is_down():
            text = "Looking down"
            yield 'D'
        elif gaze.is_center():
            text = "Looking center"
            yield 'C'

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()

        cv2.imshow("Demo", frame)

        if cv2.waitKey(1) == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()


def main():
    mac_address = '00:00:00:00:00:00'
    port = 1
    s = connect_bt(mac_address, port)
    for eye_pos in get_eye_pos(GazeTracking()):
        s.send(eye_pos.encode())
        print(eye_pos)
        time.sleep(1)

    s.close()


if __name__ == '__main__':
    main()
