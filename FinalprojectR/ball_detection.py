import os
import pickle
import numpy as np
from ultralytics import YOLO
import supervision 
import cv2

class Ball_detection:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        
    def detect_frames(self, frames):
        batch_size = 20 
        detections = [] 
        num_frames = len(frames)
        for i in range(0, num_frames, batch_size):
            batch = frames[i:i+batch_size]
            detections_batch = self.model.predict(batch, conf=0.1)    
            detections.extend(detections_batch) 
        return detections

    def get_ball_detections(self, frames, path = None):

        if path is not None and os.path.exists(path):
            with open(path, 'rb') as f:
                detec_ball = pickle.load(f)
            return detec_ball
        
        detections = self.detect_frames(frames)

        detec_ball = {'ball':[]}

        for frame_num, detection in enumerate(detections):

            detection_supervision = supervision.Detections.from_ultralytics(detection)

            detec_ball['ball'].append([])

            for detect in detection_supervision:
                bb = detect[0].tolist()
                
                detec_ball['ball'][frame_num].append(bb)

        if path is not None:
            with open(path, 'wb') as f:
                pickle.dump(detec_ball, f)

        return detec_ball
    
    def draw_traingle(self, frame, bb):
        x1, y1, x2 = int(bb[0]), int(bb[1]), int(bb[2])
        x_center = int((x1 + x2) / 2)

        triangle_points = np.array([[x_center, y1], [x_center - 10, y1 - 20], [x_center + 10, y1 - 20],])

        cv2.drawContours(frame, [triangle_points], 0, (0,255,0), cv2.FILLED)

        return frame

    def draw_ball_detection(self,video_frames, detec_ball):
        modified_video_frames = []

        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            balls = detec_ball['ball'][frame_num]

            for bb in balls:
                frame = self.draw_traingle(frame, bb)

            modified_video_frames.append(frame)

        return modified_video_frames
    
    