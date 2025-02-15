# Description: This file contains the functions to set up and update the graphs for the simulation.

import numpy as np
import matplotlib.pyplot as plt

from src.utils import create_folder



# Create figures for graphs
def create_graphs():
    #plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    #plt.show()
    return fig, ax1, ax2


# Set up the graphs
def setup_graphs(ax1, ax2):
    # Set up the velocity graph
    velocity_line, = ax1.plot([], [], 'c-', label="Velocity (m/s)")
    stb_velocity_line, = ax1.plot([], [], 'b-', label="Stabilized Vel (m/s)")
    mean_line, = ax1.plot([], [], 'r--', label="Average Velocity (m/s)")
    ax1.set_xlabel("Distance (m)")
    ax1.set_ylabel("Velocity (m/s)")
    ax1.set_title("Velocity Evolution")
    ax1.legend()

    # Set up the distance and jump graph
    distance_line, = ax2.plot([], [], 'y-', label="Distance (m)")
    jump_line, = ax2.plot([], [], 'g-', label="Jump (m)")
    ax2.set_xlabel("Distance (m)")
    ax2.set_ylabel("Height and Distance")
    ax2.set_title("Distance and Jump Evolution")
    ax2.legend()

    return velocity_line, mean_line, distance_line, jump_line, stb_velocity_line

# Update the graphs
def update_graph(distances, velocities, total_distances_body, heights, average_velocity, vel_array, velocity_line, mean_line, distance_line, jump_line, stb_velocity_line, ax1, ax2):
    if distances:
        mean_velocity = np.mean(velocities) if velocities else 0
        vel_array.append(mean_velocity)

        velocity_line.set_data(distances, velocities)
        stb_velocity_line.set_data(distances, average_velocity)
        mean_line.set_data(distances, vel_array)

        distance_line.set_data(distances, total_distances_body)
        jump_line.set_data(distances, [h - min(heights) for h in heights])

        max_velocity = max(velocities) if velocities else 25
        max_height = max(total_distances_body) if total_distances_body else 10

        ax1.set_ylim(0, max_velocity + 2.5)  
        ax1.set_xlim(0, max(distances) + 2)  

        ax2.set_ylim(0, max_height + .5)  
        ax2.set_xlim(0, max(distances) + 2)

    plt.draw()
    #plt.pause(0.001)

# save graph in file
def save_graph(fig, video_name):
    create_folder(video_name)
    fig.savefig(f"data/output/{video_name}/graph.png")
    print("Graph saved successfully!")

# hide graph
def hide_graph():
    plt.close()
    print("Graph closed successfully!")

# minimize graph
def minimize_graph():
    plt.show(block=False)
    plt.pause(0.001)
    plt.close()
    print("Graph minimized successfully!")