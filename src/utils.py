import time
import cv2
import numpy as np

def count_steps(sequence):
    integer_sequence = [round(num) for num in sequence]
    sequence_without_duplicates = []
    for num in integer_sequence:
        if not sequence_without_duplicates or sequence_without_duplicates[-1] != num:
            sequence_without_duplicates.append(num)
    counter = 0
    for i in range(1, len(sequence_without_duplicates) - 1):
        if sequence_without_duplicates[i] < sequence_without_duplicates[i - 1] and sequence_without_duplicates[i] < sequence_without_duplicates[i + 1]:
            counter += 1
    return counter

def calculate_execution_time(start_time):
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time

def display_results(distance_m_dx_total, distance_m_dy_total, average_vel, steps, execution_time):
    print("")
    print("Computer Vision System for Running Analysis")
    print("")
    print(f"Total Distance (H): {distance_m_dx_total:.2f} m")
    print(f"Total Distance (V): {distance_m_dy_total:.2f} m")
    print(f"Average Velocity: {round(average_vel, 3)} m")
    print("Steps Taken:", steps)
    print("")
    print(f"Execution Time: {execution_time:.2f} seconds")
    print("")


# mkdir folder if no exist
def create_folder(video_name):
    import os
    if not os.path.exists(f"data/output/{video_name}"):
        os.makedirs(f"data/output/{video_name}")

# Function: save data in file
def save_data(video_name, obj_data):
    
    create_folder(video_name)

    headers = ','.join(list(obj_data.keys())) + "\n"
    values = ','.join(map(str, list(obj_data.values())))
    
    with open(f"data/output/{video_name}/info.csv", "w") as file:
        # write object data {} in dat file
        file.write(headers)
        file.write(values)
        print("Data saved in file")



# Function: save csv data in file
def save_csv_data(video_name, video_array):
    
    create_folder(video_name)

    array = []
    for i in range(len(video_array['frame_position'])):
        array.append([
                i, 
                video_array['frame_position'][i],
                round(video_array['distances'][i]+video_array['total_distances_body'][i], 3),
                round(video_array['distances'][i], 3),
                round(video_array['total_distances_body'][i], 3),
                round(video_array['heights'][i], 3),
                round(video_array['velocities'][i], 3),
                round(video_array['acceleration'][i], 3),
            ])
    with open(f"data/output/{video_name}/specs.csv", "w") as file:
        # write array in csv file
        file.write("Id,Frame,Distance,Horizontal Distance,Vertical Distance,Height,Velocity,Acceleration\n")
        for i in range(len(array)):
            file.write(','.join(map(str, array[i])) + "\n")
        print("CSV data saved in file")



def extract_video_metadata(video_path, cap, fps):
    # video name
    video_name = video_path.split("/")[-1].split(".")[0]
    # video length
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # video duration
    video_duration = video_length / fps
    # video format
    video_format = video_path.split(".")[-1]
    # video codec
    video_codec = int(cap.get(cv2.CAP_PROP_FOURCC))
    video_codec = "".join([chr((video_codec >> 8 * i) & 0xFF) for i in range(4)])
    
    return video_name, video_length, video_duration, video_format, video_codec