import cv2
import mediapipe as mp
import audio

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=2,
)

landmarker = HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = landmarker.detect(mp_image)

    if len(result.hand_landmarks) > 0:
        print("Hands detected:", len(result.hand_landmarks))

        for hand in result.hand_landmarks:
            wrist = result.hand_landmarks[0][0]


            audio.target_frequency = 220 + (1.0 - wrist.y) * 660

            print(
                f"x={wrist.x:.2f}  y={wrist.y:.2f}"
            )

    cv2.imshow("Visual Theremin", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()