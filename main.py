import math

import cv2
import audio
import music

from cvzone.HandTrackingModule import HandDetector


current_scale = "Major"

scale_buttons = [
    ("Chromatic", (10, 435, 110, 470)),
    ("Major", (130, 435, 230, 470)),
    ("Minor", (250, 435, 350, 470)),
    ("Pentatonic", (370, 435, 500, 470)),
    ("Dorian", (520, 435, 630, 470)),
]


def mouse(event, x, y, flags, param):
    global current_scale

    if event == cv2.EVENT_LBUTTONDOWN:

        for name, (x1, y1, x2, y2) in scale_buttons:

            if x1 <= x <= x2 and y1 <= y <= y2:
                current_scale = name
                print("Scale:", current_scale)
    print(event)


detector = HandDetector(
    maxHands=2,
    detectionCon=0.7,
)

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cv2.namedWindow("ThereVisual")
cv2.setMouseCallback("ThereVisual", mouse)


while True:

    success, frame = cap.read()

    if not success:
        break

    hands, frame = detector.findHands(frame, draw=True)

    audio.target_volume = 0.2

    if hands:

        # leftmost -> cutoff
        hands.sort(key=lambda h: h["center"][0])

        # ---------------- Pitch ----------------

        pitchHand = hands[-1]

        px, py, _ = pitchHand["lmList"][8]

        raw_frequency = 220 + (1.0 - py / 480.0) * 660.0

        audio.target_frequency = music.quantize(
            raw_frequency,
            current_scale,
        )

        cv2.putText(
        frame,
        f"{current_scale}   {audio.target_frequency:.1f} Hz",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2,
        )   

        # ---------------- Cutoff ----------------

        if len(hands) == 2:

            cutoffHand = hands[0]

            cx, cy, _ = cutoffHand["lmList"][8]

            norm = cx / 640.0

            audio.target_cutoff = 40.0 * math.pow(300.0, norm)

            cv2.putText(
                frame,
                f"Cutoff: {audio.target_cutoff:.0f} Hz",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                2,
            )

    # ---------------- Bottom Panel ----------------

    cv2.rectangle(
        frame,
        (0, 420),
        (640, 480),
        (35, 35, 35),
        -1,
    )

    for name, (x1, y1, x2, y2) in scale_buttons:

        if name == current_scale:
            color = (180, 120, 20)
        else:
            color = (70, 70, 70)

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            -1,
        )

        cv2.putText(
            frame,
            name,
            (x1 + 8, y1 + 23),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

    cv2.imshow("ThereVisual", frame)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()