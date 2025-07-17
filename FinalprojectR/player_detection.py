import os
import pickle
from ultralytics import YOLO
import supervision
import cv2

class Player_detection:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect_frames(self, frames):
        batch_size = 20 
        detections = [] 
        num_frames = len(frames)
        for i in range(0, num_frames, batch_size):
            batch = frames[i:i+batch_size]
            detections_batch = self.model.predict(batch, conf=0.1)
            #print(type(detections_batch))       
            #print(len(detections_batch))       
            #print(detections_batch[0])       
            detections.extend(detections_batch)
        return detections
    
    def get_object_detection(self, frames, path = None):

        if path is not None and os.path.exists(path):
            with open(path, 'rb') as f:
                detec = pickle.load(f)
            return detec
        
        detections = self.detect_frames(frames)

        detec = {'players':[], 'referees':[], 'ball':[]}

        for frame_num, detection in enumerate(detections):
            class_names = detection.names   
            class_names_inv = {}
            for k, v in class_names.items():
                class_names_inv[v] = k 

            detection_supervision = supervision.Detections.from_ultralytics(detection)
            
            for object, class_id in enumerate(detection_supervision.class_id):
                if class_names[class_id] == 'goalkeeper':
                    detection_supervision.class_id[object] = class_names_inv['player']

            detec['players'].append([])
            detec['referees'].append([])
            detec['ball'].append([])

            for detect in detection_supervision:
                bb = detect[0].tolist()
                class_id = detect[3]
                
                if class_id == class_names_inv['player']:
                    detec['players'][frame_num].append(bb)
                
                if class_id == class_names_inv['referee']:
                    detec['referees'][frame_num].append(bb)

                if class_id == class_names_inv['ball']:
                    detec['ball'][frame_num].append(bb)
    
        if path is not None:
            with open(path, 'wb') as f:
                pickle.dump(detec, f)

        return detec
    
    def draw_rectangle(self, frame, bb, color, text):
        x1, y1, x2, y2 = int(bb[0]), int(bb[1]), int(bb[2]), int(bb[3])
        x_center = int((x1 + x2) / 2)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness = 2)

        ((text_width, text_height), baseline) = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        rectangle_width = text_width + 2 * 10
        rectangle_height = text_height + 2 * 6
        x1_rect = x_center - (rectangle_width / 2)
        x2_rect = x_center + (rectangle_width / 2)
        y1_rect = y1 - rectangle_height - 5 
        y2_rect = y1 - 5
        x1_text = x1_rect + (rectangle_width - text_width) / 2

        cv2.rectangle(frame, (int(x1_rect), int(y1_rect)), (int(x2_rect), int(y2_rect)), color, cv2.FILLED)
        
        cv2.putText(frame, text, (int(x1_text), int(y1_rect + 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        return frame

    def draw_detection(self, video_frames, detec):
        modified_video_frames = []

        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            players = detec['players'][frame_num]
            referees = detec['referees'][frame_num]
            balls = detec['ball'][frame_num]

            for bb in players:
                frame = self.draw_rectangle(frame, bb, (0,0,255), 'player')

            for bb in referees:
                frame = self.draw_rectangle(frame, bb, (0,255,255), 'referee')
            
            for bb in balls:
                frame = self.draw_rectangle(frame, bb, (0,255,0), 'ball')

            modified_video_frames.append(frame)

        return modified_video_frames
    
    