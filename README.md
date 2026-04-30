# TAMS ROS 2

This repository provides a ROS 2 reference implementation of Task-Aware Multi-View Adaptive Streaming (TAMS) for wireless telerobotic manipulation.

The implementation follows the system design described in the paper: it infers the current manipulation phase from lightweight robot-side signals and allocates bitrate across three camera streams according to phase-specific view weights.

This repository is intended as a reference implementation. Hardware-specific drivers, private calibration parameters, and experiment-specific scripts are not included.

## Nodes

- `phase_inference`: infers the current manipulation phase from end-effector velocity and gripper state.
- `bitrate_allocator`: maps the inferred phase and uplink budget to target bitrates for EIH, GT, and GS streams.
- `stream_controller`: receives target bitrates and exposes the latest encoder targets for integration with a video pipeline.

## Build

```bash
colcon build --packages-select tams_ros2
source install/setup.bash
```

## Run

```bash
ros2 run tams_ros2 phase_inference
ros2 run tams_ros2 bitrate_allocator
ros2 run tams_ros2 stream_controller
```

## Interfaces

The reference implementation uses standard ROS 2 messages only. Robot-specific adapters can publish compatible velocity, gripper, and uplink budget topics.
