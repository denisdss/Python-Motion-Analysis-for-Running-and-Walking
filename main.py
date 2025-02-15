import cv2
import matplotlib.pyplot as plt
import time

from src.controller import analyze_video
from src.utils import extract_video_metadata

# Start time measurement
start_time = time.time()

# Load the video
video_path = "assets/run.mp4"  
cap = cv2.VideoCapture(video_path)

# Set output resolution
frame_width, frame_height = 320, 240  

# Get video FPS and calculate frame time
fps = cap.get(cv2.CAP_PROP_FPS)
frame_time_ms = int(1000 / fps)

# Pixel-to-meter conversion factor
pixels_per_meter = 100  

# Process each frame
frame_count = 0

# Height offset for the jump calculation
HEIGHT_OFFSET_CALIBRATION = 0.0005 # Affect graph in the jump line (Green line)

video_name, video_length, video_duration, video_format, video_codec = extract_video_metadata(video_path, cap, fps)

obj_video = {
    "video_name": video_name,
    "video_format": video_format,
    "video_codec": video_codec,
    "video_frames": video_length,
    "video_duration": video_duration,
    "video_fps": fps,
    "frame_width": frame_width,
    "frame_height": frame_height,
    "pixels_per_meter": pixels_per_meter,
    "HEIGHT_OFFSET_CALIBRATION": HEIGHT_OFFSET_CALIBRATION,
}
# Call the function
analyze_video(obj_video, cap, start_time)

cap.release()
cv2.destroyAllWindows()
#plt.ioff()
#plt.show()
