import os
import pickle
from ultralytics import YOLO
import supervision
import cv2

class Tracker:
    def __init__(self, model):
        self.model = YOLO(model)
        self.tracker = supervision.ByteTrack(minimum_consecutive_frames = 3)

    def detect_frames(self, frames):
        batch_size = 20 
        detections = [] 
        num_frames = len(frames)
        for i in range(0, num_frames, batch_size):
            batch = frames[i:i+batch_size]
            detections_batch = self.model.predict(batch, conf=0.1)      
            detections.extend(detections_batch) 
        return detections
    
    def get_object_tracks(self, frames, path = None):

        if path is not None and os.path.exists(path):
            with open(path, 'rb') as f:
                tracks = pickle.load(f)
            return tracks
        
        detections = self.detect_frames(frames)

        tracks = {'players':[], 'referees':[]}

        for frame_num, detection in enumerate(detections):
            class_names = detection.names 
            class_names_inv = {}
            for k, v in class_names.items():
                class_names_inv[v] = k 

            detection_supervision = supervision.Detections.from_ultralytics(detection) 

            for object, class_id in enumerate(detection_supervision.class_id):
                if class_names[class_id] == 'goalkeeper':
                    detection_supervision.class_id[object] = class_names_inv['player']

            detection_with_tracks = self.tracker.update_with_detections(detection_supervision)

            tracks['players'].append({})
            tracks['referees'].append({})

            for track_detect in detection_with_tracks:
                bb = track_detect[0].tolist()
                class_id = track_detect[3]
                track_id = track_detect[4]

                if class_id == class_names_inv['player']:
                    tracks['players'][frame_num][track_id] = bb
                
                if class_id == class_names_inv['referee']:
                    tracks['referees'][frame_num][track_id] = bb
            
        if path is not None:
            with open(path, 'wb') as f:
                pickle.dump(tracks,f)

        return tracks
        
    def draw_ellipse(self, frame, bb, color, track_id = None):
        x1, x2, y2 = int(bb[0]), int(bb[2]), int(bb[3])
        x_center = int((x1 + x2) / 2)
        width = bb[2] - bb[0]

        cv2.ellipse(frame, center = (x_center, y2), axes = (int(width), int(0.35 * width)), angle = 0.0, startAngle = -45, endAngle = 235, color = color, thickness = 2, lineType = cv2.LINE_4)

        rectangle_width = 40
        rectangle_height = 20
        x1_rect = x_center - (rectangle_width / 2)
        x2_rect = x_center + (rectangle_width / 2)
        y1_rect = (y2 - (rectangle_height / 2)) + 15
        y2_rect = (y2 + (rectangle_height / 2)) + 15

        if track_id:
            cv2.rectangle(frame, (int(x1_rect), int(y1_rect)), (int(x2_rect), int(y2_rect)), color, cv2.FILLED)
            
            x_text = x1_rect + 12
            y_text = y1_rect + 15
            
            cv2.putText(frame, str(track_id), (int(x_text),int(y_text)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)

        return frame

    
    def draw_track_id(self, video_frames, tracks):
        modified_video_frames = []
        
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            players = tracks['players'][frame_num]
            referees = tracks['referees'][frame_num]

            for track_id, bb in players.items():
                frame = self.draw_ellipse(frame, bb, (0,0,255), track_id)

            for track_id, bb in referees.items():
                frame = self.draw_ellipse(frame, bb, (0,255,255))
            
            modified_video_frames.append(frame)

        return modified_video_frames