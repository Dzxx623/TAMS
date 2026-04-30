from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package="tams_ros2", executable="phase_inference", name="tams_phase_inference"),
        Node(package="tams_ros2", executable="bitrate_allocator", name="tams_bitrate_allocator"),
        Node(package="tams_ros2", executable="stream_controller", name="tams_stream_controller"),
    ])
