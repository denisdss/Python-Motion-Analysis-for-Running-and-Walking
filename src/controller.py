from src.core import process_video
from src.graphs import create_graphs, save_graph, setup_graphs
from src.utils import calculate_execution_time, count_steps, display_results, save_csv_data, save_data  # Importing the library to measure time

def analyze_video(obj_video, video_capture, start_time):
    # frame_width, frame_height, fps, pixels_per_meter, HEIGHT_OFFSET_CALIBRATION
    fig, ax1, ax2 = create_graphs()
    
    velocity_line, mean_line, distance_line, jump_line, stb_velocity_line = setup_graphs(ax1, ax2)

    obj_array = process_video(
        obj_video['HEIGHT_OFFSET_CALIBRATION'], video_capture, obj_video['frame_width'], obj_video['frame_height'], obj_video['video_fps'], obj_video['pixels_per_meter'], 
        velocity_line, mean_line, distance_line, jump_line, stb_velocity_line, ax1, ax2
    )
   
    execution_time = calculate_execution_time(start_time)
    
    steps = count_steps(obj_array['parabola'])
    
    display_results(obj_array['distance_m_dx_total'], obj_array['distance_m_dy_total'], obj_array['average_velocity'], steps, execution_time)
    obj_data = {
        "Title": obj_video["video_name"],
        "Format": obj_video["video_format"],
        "Codec": obj_video["video_codec"],
        "Frames": obj_video["video_frames"],
        "Duration": round(obj_video["video_duration"]),
        "FPS": obj_video["video_fps"],
        "Width": obj_video["frame_width"],
        "Height": obj_video["frame_height"],
        "PxM": obj_video["pixels_per_meter"],
        "HOC": obj_video["HEIGHT_OFFSET_CALIBRATION"],
        "Horizontal Distance":round(obj_array['distance_m_dx_total'], 3),
        "Vertical Distance":round(obj_array['distance_m_dy_total'], 3),
        "Total Distance":round(obj_array['distance_m_dx_total'] + obj_array['distance_m_dy_total'], 3),
        "Average Velocity":round(obj_array['average_velocity'], 3),
        "Steps Taken":steps,
        "Script Execution Time (s)":round(execution_time, 2),
    }

    save_graph(fig, obj_video['video_name'])
    
    save_data(obj_video['video_name'], obj_data)

    save_csv_data(obj_video['video_name'], obj_array)
