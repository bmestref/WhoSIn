import cv2
import csv
from datetime import datetime
from ultralytics import YOLO
import sys

def whosin_capture(video_path, log_path, crossing_line):
    log_data = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[ERROR] Could not open video: {video_path}")
        return

    model = YOLO('yolov8n.pt')  

    with open(log_path, mode='w', newline='') as f:
        csv.writer(f).writerow(['Action', 'Datetime', 'People Inside'])

    entry_line_y = crossing_line
    offset = 10
    count_inside = 0
    tracked_positions = {} 
    FRAME_SKIP = 5
    frame_index = 0

    print("[INFO] Starting processing...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[INFO] End of video.")
            break

        frame = cv2.resize(frame, (640, 360)) 
        results_list = model.track(
            source=frame,
            imgsz=160,
            verbose=False,
            tracker="bytetrack.yaml",
            classes=[0],      # Only person class
            iou=0.5
        )        
        if not results_list:
            continue  

        results = results_list[0]

        if results.boxes is not None and len(results.boxes) > 0:
            for box in results.boxes:

                if box.id is None:
                    continue  

                track_id = int(box.id.item())
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                center_x = (x1 + x2) // 2
                center_y = int(y1 + (y2 - y1) * 0.2)  

                prev_y = tracked_positions.get(track_id)

                if frame_index % FRAME_SKIP == 0 and prev_y is not None:

                    if prev_y > entry_line_y - offset and center_y <= entry_line_y + offset:
                        count_inside += 1
                        print(f"[INFO] ID {track_id} entered. Count = {count_inside}")
                        log_data.append(['Entry', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count_inside])

                    elif prev_y < entry_line_y + offset and center_y >= entry_line_y - offset:
                        count_inside = max(0, count_inside - 1)
                        print(f"[INFO] ID {track_id} exited. Count = {count_inside}")
                        log_data.append(['Entry', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count_inside])

                tracked_positions[track_id] = center_y

                cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

        cv2.line(frame, (0, entry_line_y), (frame.shape[1], entry_line_y), (255, 0, 0), 2)
        cv2.putText(frame, f"People Inside: {count_inside}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.imshow("Crossing Counter", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Quit requested.")
            with open(log_path, 'a', newline='') as f:
                writer = csv.writer(f)
                csv.writer(f).writerows(log_data)
            break

        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()

# video_path = 'test_data/sample_video2.mp4'
# whosin_capture(video_path, 'log_file.csv', 250)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python whosin_counter.py <video_path> <log_path> <crossing_line_y>")
        sys.exit(1)

    video_path = sys.argv[1]
    log_path = sys.argv[2]
    crossing_line = int(sys.argv[3])

    whosin_capture(video_path, log_path, crossing_line)
