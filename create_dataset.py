import matplotlib.pyplot as plt
import cv2
import os

if not os.path.isdir("dataset"):
    os.mkdir("dataset")

path = "dataset/" + input('Enter the label: ')
if not os.path.isdir(path):
    os.mkdir(path)
num_samples = int(input("No. of samples: "))
vid = cv2.VideoCapture(0)

count = 0
capture = False

while True:
    if count == 200:
        break
    ret, frame = vid.read()
    cv2.rectangle(frame, (25, 25), (281, 281), (0, 255, 0), 1)
    if capture:
        img = frame[25:281, 25:281]
        cv2.imwrite(f"{path}/{count}.png", img)
        cv2.putText(
            frame,
            f"count: {count}",
            (15, 15),
            cv2.QT_FONT_NORMAL,
            0.5,
            (255, 0, 0),
            1,
            cv2.LINE_AA,
        )
        count += 1

    cv2.imshow("video", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    if cv2.waitKey(1) & 0xFF == ord(" "):
        capture = not capture
        if capture:
            print('started capturing')