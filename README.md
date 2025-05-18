# WhoSIn

This project uses [YOLOv8](https://github.com/ultralytics/ultralytics) and ByteTrack to count the number of people crossing a defined line in a video. It's designed for monitoring entrances and exits in real time from a fixed camera.


---

## ✅ Features

- Counts number of people entering and exiting a store based on a horizontal line.
- Tracks each person using unique IDs.
- Logs actions (`Entry` or `Exit`) and timestamps to a CSV file.
- Displays annotated video with real-time count.
---

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

bash
Copiar
Editar
python whosin_counter.py
You can customize the input video and detection line in the script:

python
Copiar
Editar
video_path = 'test_data/sample_video2.mp4'
whosin_capture(video_path, 'log_file.csv', 250)  # 250 is the y-position of the detection line
