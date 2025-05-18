# WhoSIn

This project uses [YOLOv8](https://github.com/ultralytics/ultralytics) and ByteTrack to count the number of people crossing a defined line in a video. It's designed for monitoring entrances and exits in real time from a fixed camera.

## ✅ Features

- Counts number of people entering and exiting a store based on a horizontal line.
- Tracks each person using unique IDs.
- Logs actions (`Entry` or `Exit`) and timestamps to a CSV file.
- Displays annotated video with real-time count.

## 🛠️ Requirements

- Python 3.8+
- [Ultralytics YOLOv8](https://docs.ultralytics.com/)
- OpenCV
- NumPy

Install dependencies:

```bash
pip install ultralytics opencv-python
```

Run the main script with your video:
```bash
python whosin_counter.py <video.mp4> <directory_where_to_save_logs> <altitude_of_the_crossing_line>
```
## 📌 How It Works
Detection: YOLOv8 is used to detect objects (restricted to person class via classes=[0]).

- Tracking: ByteTrack maintains track IDs of individuals.

- Line Crossing Logic:

Each person is tracked based on the vertical position of their head (20% from top of bounding box).
When their tracked y-coordinate crosses a fixed horizontal line (crossing_line), it logs an entry or exit.

## 📈 Output Example
CSV Log:

```bash
Action,Datetime,People Inside
Entry,2025-05-18 10:33:15,1
Exit,2025-05-18 10:33:35,0
```

## ⚠️ Notes
Currently supports horizontal line detection only.
Works best on top-down or frontal camera angles.
Accuracy may vary with occlusions or poor lighting.

## 📷 Sample Video
A demo video is included in test_data/sample_video2.mp4.
