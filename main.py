import time
import cv2
import mediapipe as mp
import audio

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2,
)

landmarker = HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb,
    )

    timestamp_ms = int(time.monotonic() * 1000)

    result = landmarker.detect_for_video(
        mp_image,
        timestamp_ms,
    )

    if result.hand_landmarks:

        wrist = result.hand_landmarks[0][0]

        target = 220 + (1.0 - wrist.y) * 660

        audio.target_frequency = target

        x = int(wrist.x * frame.shape[1])
        y = int(wrist.y * frame.shape[0])

        cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

        cv2.putText(
            frame,
            f"{target:.1f} Hz",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

    cv2.imshow("Visual Theremin", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()