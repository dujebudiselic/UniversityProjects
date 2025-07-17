from ultralytics import YOLO

model = YOLO('models/yolov8l.pt')

rez = model.predict('input_videos/08fd33_4.mp4', save = True)