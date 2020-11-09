import tensorflow as tf
import numpy as np
import cv2
from random import choice

model = tf.keras.models.load_model("models/rps_model")

vid = cv2.VideoCapture(0)

classes = ["rock", "paper", "scissors"]
prev = ""

rock = cv2.imread("assets/rock.png")
paper = cv2.imread("assets/paper.png")
scissor = cv2.imread("assets/scissors.png")

while True:
    ret, frame = vid.read()
    cv2.rectangle(frame, (40, 40), (296, 296), (0, 255, 0), 2)
    img = frame[40:296, 40:296]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (100, 100))
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    image = np.array([img]).reshape((1, 100, 100, 1))
    image = image / 255
    p = model.predict(image)
    move = classes[np.argmax(p)].upper()
    if move != prev:
        comp_move = choice([0, 1, 2])
    cv2.putText(
        frame,
        "prediction: " + move,
        (85, 25),
        cv2.QT_FONT_NORMAL,
        0.5,
        (255, 0, 0),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "CPU move: " + classes[comp_move],
        (410, 25),
        cv2.QT_FONT_NORMAL,
        0.5,
        (255, 0, 0),
        1,
        cv2.LINE_AA,
    )
    frame[40:296, -296:-40] = (
        rock if comp_move == 0 else paper if comp_move == 1 else scissor
    )
    prev = move
    cv2.imshow("Rock Paper Scissors", frame)
vid.release()
cv2.destroyAllWindows()