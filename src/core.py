import cv2
import numpy as np
import mediapipe as mp

from src.graphs import update_graph



# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def process_video(HOC, cap, frame_width, frame_height, fps, pixels_per_meter, velocity_line, mean_line, distance_line, jump_line, stb_velocity_line, ax1, ax2):
    HEIGHT_OFFSET_CALIBRATION = HOC
    
    frame_count = 0
    height_offset = .0
    last_position = None
    last_velocity = 0
    velocity = 0
    distance_m_dx_total = 0
    distance_m_dy_total = 0
    total_distances_body = []
    heights = []
    parabola = []
    average_velocity = []
    velocities = []
    distances = []
    vel_array = []
    acceleration = 0
    frame_position = []
    acceleration_arr = []
    
    print("Processing video...")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  

        frame_count += 1

        # Process every 2 or 3 frames to reduce load
        if frame_count % 2 != 0:
            continue

        frame = cv2.resize(frame, (frame_width, frame_height))
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            h, w, _ = frame.shape
            landmarks = results.pose_landmarks.landmark
            
            # Define body points for chest average calculation
            body_points = [
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],  
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER], 
                landmarks[mp_pose.PoseLandmark.LEFT_HIP],  
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            ]

            # Average Y position of the chest
            y_avg = np.mean([point.y * h for point in body_points])

            # Chest height in meters (converting from pixels to meters)
            height_m = (h - y_avg) / pixels_per_meter  

            if last_position is not None:
                dx = np.mean([point.x * w for point in body_points]) - last_position[0]
                dy = y_avg - last_position[1]

                distance_px = np.sqrt(dx**2 + dy**2)  

                distance_horizontal = np.abs(dx)
                distance_vertical = np.abs(dy)

                distance_m_dx = distance_horizontal / pixels_per_meter
                distance_m_dx_total += distance_m_dx

                distance_m_dy = distance_vertical / pixels_per_meter
                distance_m_dy_total += distance_m_dy

                velocity = distance_m_dx / (1 / fps)  
                acceleration = (velocity - last_velocity)

                distances.append(distance_m_dx_total) 
                velocities.append(velocity)
                average_velocity.append((velocity + last_velocity) / 2)

                height_m -= height_offset
                parabola.append(height_m*1000)
                heights.append(height_m)
                height_offset += HEIGHT_OFFSET_CALIBRATION
                total_distances_body.append(distance_m_dy_total)

                frame_position.append(frame_count)

                acceleration_arr.append(acceleration)
                # Calculate the parabola based on chest height
                update_graph(distances, velocities, total_distances_body, heights, average_velocity, vel_array, velocity_line, mean_line, distance_line, jump_line, stb_velocity_line, ax1, ax2)  

            last_position = (np.mean([point.x * w for point in body_points]), y_avg)  
            last_velocity = velocity  

            cv2.putText(frame, f"Vel: {velocity:.2f} m/s", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"Accel: {acceleration:.2f} m/s²", (50, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        #cv2.imshow("Pose Estimation - Velocity and Height", frame)

        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break  
    obj_array = {
        "distance_m_dx_total": distance_m_dx_total,
        "distance_m_dy_total": distance_m_dy_total,
        "average_velocity": np.mean(velocities),
        "velocities": velocities,
        "parabola": parabola, # only for calculate steps
        "heights": heights,
        "total_distances_body": total_distances_body,
        "distances": distances,
        "frame_position": frame_position,
        "acceleration": acceleration_arr
    }
    return obj_array
