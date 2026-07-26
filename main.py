import cv2
import audio

from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(
    maxHands=2,
    detectionCon=0.7,
)

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:

    success, frame = cap.read()

    if not success:
        break

    hands, frame = detector.findHands(frame, draw=True)

    audio.target_volume = 0.0

    if hands:

        hands.sort(key=lambda h: h["center"][0])

        leftHand = hands[0]

        x, y, _ = leftHand["lmList"][0]

        audio.target_volume = max(0.0, min(0.3, 0.3 * (1 - y / 480)))

        cv2.putText(
            frame,
            f"Volume: {audio.target_volume:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2,
        )

        if len(hands) > 1:

            rightHand = hands[1]

            x, y, _ = rightHand["lmList"][0]

            audio.target_frequency = 220 + (1 - y / 480) * 660

            cv2.putText(
                frame,
                f"Pitch: {audio.target_frequency:.0f} Hz",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

    cv2.imshow("ThereVisual", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()