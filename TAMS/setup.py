from setuptools import find_packages, setup

package_name = "tams_ros2"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Zexin Deng",
    maintainer_email="zexin.deng@warwick.ac.uk",
    description="ROS 2 reference implementation of Task-Aware Multi-View Adaptive Streaming for wireless telerobotic manipulation.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "phase_inference = tams_ros2.phase_inference_node:main",
            "bitrate_allocator = tams_ros2.bitrate_allocator_node:main",
            "stream_controller = tams_ros2.stream_controller_node:main",
        ],
    },
)
