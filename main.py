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

    audio.target_volume = 0.2

    if hands:

        # Sort by horizontal position
        hands.sort(key=lambda h: h["center"][0])

        # ---------- Pitch ----------
        # If only one hand exists, it controls pitch.
        # If two hands exist, the rightmost controls pitch.

        pitchHand = hands[-1]

        px, py, _ = pitchHand["lmList"][8]

        audio.target_frequency = 220 + (1.0 - py / 480.0) * 660.0

        cv2.putText(
            frame,
            f"Pitch: {audio.target_frequency:.0f} Hz",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        # ---------- Cutoff ----------
        # Only active when two hands are visible.

        if len(hands) == 2:

            cutoffHand = hands[0]

            cx, cy, _ = cutoffHand["lmList"][8]

            audio.target_cutoff = cx / 640.0

            cv2.putText(
                frame,
                f"Cutoff: {audio.target_cutoff:.2f}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                2,
            )

    cv2.imshow("ThereVisual", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()