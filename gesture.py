#gesturez
from cvzone.HandTrackingModule import HandDetector
import math 

def detect(detector, hand):

    fingers = detector.fingersUp(hand)

    count = sum(fingers)

    if count == 0:
        return "fist"

    if count == 1:
        return "one"

    if count == 2:
        return "two"

    if count == 3:
        return "three"

    if count == 4:
        return "four"

    return None


import math


def detect(detector, hand):

    if pinch(hand):
        return "pinch"

    fingers = detector.fingersUp(hand)

    count = sum(fingers)

    if count == 0:
        return "fist"
    elif count == 1:
        return "one"
    elif count == 2:
        return "two"
    elif count == 3:
        return "three"
    elif count == 4:
        return "four"

    return None


def pinch(hand):

    thumb = hand["lmList"][4]
    index = hand["lmList"][8]

    distance = math.hypot(
        thumb[0] - index[0],
        thumb[1] - index[1],
    )

    return distance < 30