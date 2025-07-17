import os
import pickle
from ultralytics import YOLO
import supervision
import cv2
from sklearn.cluster import KMeans
import numpy as np

class Team_classification:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.tracker = supervision.ByteTrack(minimum_consecutive_frames = 3)
        self.kmeans = None
        self.team_colors = {}
        self.player_team_assigned = {}

    def detect_frames(self, frames):
        batch_size = 20 
        detections = [] 
        num_frames = len(frames)
        for i in range(0, num_frames, batch_size):
            batch = frames[i:i+batch_size]
            detections_batch = self.model.predict(batch, conf=0.1)
            detections.extend(detections_batch) 
        return detections
    
    def get_object_detection_tracks(self, frames, path = None):

        if path is not None and os.path.exists(path):
            with open(path, 'rb') as f:
                tracks = pickle.load(f)
            return tracks
        
        detections = self.detect_frames(frames)

        tracks = {'players':[], 'goalkeepers':[], 'referees':[]}

        for frame_num, detection in enumerate(detections):
            class_names = detection.names 
            class_names_inv = {}
            for k, v in class_names.items():
                class_names_inv[v] = k

            detection_supervision = supervision.Detections.from_ultralytics(detection)

            detection_with_tracks = self.tracker.update_with_detections(detection_supervision)

            tracks['players'].append({})
            tracks['goalkeepers'].append({})
            tracks['referees'].append({})

            for track_detect in detection_with_tracks:
                bb = track_detect[0].tolist()
                class_id = track_detect[3]
                track_id = track_detect[4]

                if class_id == class_names_inv['player']:
                    tracks['players'][frame_num][track_id] = {'bb':bb}
                
                if class_id == class_names_inv['referee']:
                    tracks['referees'][frame_num][track_id] = bb

                if class_id == class_names_inv['goalkeeper']:
                    tracks['goalkeepers'][frame_num][track_id] = {'bb':bb}
                
        if path is not None:
            with open(path, 'wb') as f:
                pickle.dump(tracks, f)

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

    
    def draw_teams(self, video_frames, tracks):
        modified_video_frames = []
        
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            players = tracks['players'][frame_num]
            goalkeepers = tracks['goalkeepers'][frame_num]
            referees = tracks['referees'][frame_num]

            for track_id, player in players.items():
                team = player['team']
                if team == 0:
                    frame = self.draw_ellipse(frame, player['bb'], (0,0,255), track_id)
                elif team == 1:
                    frame = self.draw_ellipse(frame, player['bb'], (255,0,0), track_id)

            for track_id, goalkeeper in goalkeepers.items():
                team = goalkeeper['team']
                if team == 0:
                    frame = self.draw_ellipse(frame, goalkeeper['bb'], (0,0,255), track_id)
                elif team == 1:
                    frame = self.draw_ellipse(frame, goalkeeper['bb'], (255,0,0), track_id)

            for track_id, bb in referees.items():
                frame = self.draw_ellipse(frame, bb, (0,255,255))
            
            modified_video_frames.append(frame)

        return modified_video_frames
    

    def get_player_jersey_color(self, frame, bb):
        x1, y1, x2, y2 = int(bb[0]), int(bb[1]), int(bb[2]), int(bb[3])
        image = frame[y1:y2, x1:x2]
        top_half_image = image[0:int(image.shape[0]/2), :]

        image_2d = top_half_image.reshape(-1,3)

        kmeans_background_jersey = KMeans(n_clusters = 2, init = 'k-means++', n_init = 10)
        kmeans_background_jersey.fit(image_2d)

        labels = kmeans_background_jersey.labels_

        clustered_image = labels.reshape(top_half_image.shape[0], top_half_image.shape[1])

        corner_clusters = [clustered_image[0,0],clustered_image[0,-1],clustered_image[-1,0],clustered_image[-1,-1]]
        non_player_cluster = max(corner_clusters, key = corner_clusters.count)
        player_cluster = 1 - non_player_cluster

        player_jersey_color = kmeans_background_jersey.cluster_centers_[player_cluster]

        return player_jersey_color


    def assign_team_colors(self, frame, player_detections):
        player_colors = []

        for track_id, player_detection in player_detections.items():
            bb = player_detection['bb']
            player_color = self.get_player_jersey_color(frame, bb)
            player_colors.append(player_color) 

        
        kmeans_team_colors = KMeans(n_clusters = 2, init = 'k-means++', n_init = 10)
        kmeans_team_colors.fit(player_colors)

        self.kmeans = kmeans_team_colors

        self.team_colors[0] = kmeans_team_colors.cluster_centers_[0]
        self.team_colors[1] = kmeans_team_colors.cluster_centers_[1]


    def get_player_team(self, frame, player_bb, player_id):

        if player_id in self.player_team_assigned:
            return self.player_team_assigned[player_id]

        player_jersey_color = self.get_player_jersey_color(frame, player_bb)

        team_id = self.kmeans.predict(player_jersey_color.reshape(1,-1))[0]
        
        self.player_team_assigned[player_id] = team_id

        return team_id

    def get_goalkeeper_team(self, goalkeeper_bb, players_bboxes_playerid):
        gk_x_center = (goalkeeper_bb[0] + goalkeeper_bb[2]) / 2
        gk_y_center = (goalkeeper_bb[1] + goalkeeper_bb[3]) / 2
        
        team0_positions = []
        team1_positions = []
        
        for player_id, track in players_bboxes_playerid.items():
            if player_id in self.player_team_assigned:
                team_id = self.player_team_assigned[player_id]
                bb = track['bb']
                x_center = (bb[0] + bb[2]) / 2
                y_center = (bb[1] + bb[3]) / 2
                
                if team_id == 0:
                    team0_positions.append([x_center, y_center])
                else:
                    team1_positions.append([x_center, y_center])

        team0_centroid = np.mean(team0_positions, axis = 0)
        team1_centroid = np.mean(team1_positions, axis = 0)
            
        dist_to_team0 = np.linalg.norm([gk_x_center, gk_y_center] - team0_centroid)
        dist_to_team1 = np.linalg.norm([gk_x_center, gk_y_center] - team1_centroid)
            
        if dist_to_team0 < dist_to_team1:
            return 0
        else:
            return 1
    
    def assign_teams(self, tracks, video_frames):

        for frame_num, player_track in enumerate(tracks['players']):
            for player_id, track in player_track.items():
                team = self.get_player_team(video_frames[frame_num], track['bb'], player_id)
                tracks['players'][frame_num][player_id]['team'] = team

        return tracks
    
    def assign_teams_goalkeeper(self, tracks):

        for frame_num, goalkeeper_track in enumerate(tracks['goalkeepers']):
            for goalkeeper_id, track in goalkeeper_track.items():
                team = self.get_goalkeeper_team(track['bb'], tracks['players'][frame_num])
                tracks['goalkeepers'][frame_num][goalkeeper_id]['team'] = team

        return tracks