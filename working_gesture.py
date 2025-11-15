import cv2
import mediapipe as mp
import numpy as np
import time
import json

mp_pose = mp.solutions.pose.Pose()

cap = cv2.VideoCapture(0)

gesture_name = "wave"  # change for each gesture
data = []

print("Collecting data for:", gesture_name)
time.sleep(3)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_pose.process(rgb)
    
    if result.pose_landmarks:
        lm = result.pose_landmarks.landmark
        row = []
        for p in lm:
            row += [p.x, p.y, p.z]
        
        data.append(row)
    
    cv2.imshow("pose", frame)
    k = cv2.waitKey(1)
    if k == ord('q'):   # press q to stop
        break

cap.release()
cv2.destroyAllWindows()

with open(f"{gesture_name}.json","w") as f:
    json.dump(data, f)

print("Saved", gesture_name)
