from tracker import Tracker
from player_detection import Player_detection
from ball_detection import Ball_detection
from team_classification import Team_classification
import cv2

def read_video(video_path):
    video = cv2.VideoCapture(video_path)
    frames = []
    while True:
        read, frame = video.read()
        if not read: 
            break
        frames.append(frame)
    return frames

def save_video(modified_video_frames, modified_video_path):
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    video_writer = cv2.VideoWriter(modified_video_path, fourcc, 24, (modified_video_frames[0].shape[1], modified_video_frames[0].shape[0]))
    for frame in modified_video_frames:
        video_writer.write(frame)
    video_writer.release()


def main():
    print('Select an option:')
    print('1. Player detection')
    print('2. Ball detection')
    print('3. Player tracking')
    print('4. Team classification')
    task = input('Enter number: ').strip()
    modified_video_name = input('Enter output video name: ').strip()
    modified_video_path = 'modified_videos/' + modified_video_name + '.avi'
    bounding_boxes_path = 'bounding_boxes/' + modified_video_name + '.pkl'

    video_frames = read_video('input_videos/08fd33_4.mp4')

    if task == '1':
        
        player_detection = Player_detection('models/best_player.pt')

        detec = player_detection.get_object_detection(video_frames, bounding_boxes_path)

        modified_video_frames = player_detection.draw_detection(video_frames, detec)

        save_video(modified_video_frames, modified_video_path)
    
    elif task == '2':
        
        ball_detection = Ball_detection('models/best_ball.pt')

        detec_ball = ball_detection.get_ball_detections(video_frames, bounding_boxes_path)

        modified_video_frames = ball_detection.draw_ball_detection(video_frames, detec_ball)

        save_video(modified_video_frames, modified_video_path)

    elif task == '3':

        tracker = Tracker('models/best_player.pt')

        tracks = tracker.get_object_tracks(video_frames, bounding_boxes_path)

        modified_video_frames = tracker.draw_track_id(video_frames, tracks)

        save_video(modified_video_frames, modified_video_path)

    elif task == '4':

        team_classification = Team_classification('models/best_player.pt')

        tracks = team_classification.get_object_detection_tracks(video_frames, bounding_boxes_path)

        team_classification.assign_team_colors(video_frames[20], tracks['players'][20])

        player_teams = team_classification.assign_teams(tracks, video_frames)

        player_teams = team_classification.assign_teams_goalkeeper(player_teams)
        
        modified_video_frames = team_classification.draw_teams(video_frames, player_teams)
        
        save_video(modified_video_frames, modified_video_path)

if __name__ == '__main__':
    main()