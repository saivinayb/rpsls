import tensorflow as tf
import numpy as np
import cv2
from random import choice

model = tf.keras.models.load_model("models/rpsls_model")

vid = cv2.VideoCapture(0)

classes = ["rock", "paper", "scissors", "lizard", "spock", "none"]
prev = ""

rock = cv2.imread("assets/rock.png")
paper = cv2.imread("assets/paper.png")
scissor = cv2.imread("assets/scissors.png")
lizard = cv2.imread("assets/lizard.png")
spock = cv2.imread("assets/spock.png")

while True:
    ret, frame = vid.read()
    cv2.rectangle(frame, (40, 40), (296, 296), (0, 255, 0), 1)
    img = frame[40:296, 40:296]
    img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    image = np.array([img]).reshape((1, 128, 128, 3))
    image = image / 255
    p = model.predict(image)
    move = classes[np.argmax(p)]
    if move != prev:
        if move == "none":
            comp_move = 5
        else:
            comp_move = choice([0, 1, 2, 3, 4])
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
        "CPU's move: " + classes[comp_move],
        (410, 25),
        cv2.QT_FONT_NORMAL,
        0.5,
        (255, 0, 0),
        1,
        cv2.LINE_AA,
    )

    if comp_move == 0:
        frame[40:296, -296:-40] = rock
    if comp_move == 1:
        frame[40:296, -296:-40] = paper
    if comp_move == 2:
        frame[40:296, -296:-40] = scissor
    if comp_move == 3:
        frame[40:296, -296:-40] = lizard
    if comp_move == 4:
        frame[40:296, -296:-40] = spock
    prev = move
    cv2.imshow("Rock Paper Scissors Lizard Spock", frame)
vid.release()
cv2.destroyAllWindows()