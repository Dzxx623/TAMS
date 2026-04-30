import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String

from tams_ros2.common import allocate_bitrate


class BitrateAllocatorNode(Node):
    def __init__(self):
        super().__init__("tams_bitrate_allocator")
        self.declare_parameter("minimum_stream_mbps", 0.30)
        self.declare_parameter("default_uplink_budget_mbps", 6.0)
        self.phase = "Reach"
        self.uplink_budget_mbps = float(self.get_parameter("default_uplink_budget_mbps").value)
        self.create_subscription(String, "tams/phase", self.phase_callback, 10)
        self.create_subscription(Float32, "tams/uplink_budget_mbps", self.budget_callback, 10)
        self.publisher = self.create_publisher(String, "tams/bitrate_targets", 10)
        self.create_timer(0.10, self.publish_targets)

    def phase_callback(self, msg: String):
        self.phase = msg.data

    def budget_callback(self, msg: Float32):
        self.uplink_budget_mbps = float(msg.data)

    def publish_targets(self):
        minimum_stream_mbps = float(self.get_parameter("minimum_stream_mbps").value)
        targets = allocate_bitrate(self.phase, self.uplink_budget_mbps, minimum_stream_mbps).as_dict()
        msg = String()
        msg.data = json.dumps({"phase": self.phase, "targets_mbps": targets})
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = BitrateAllocatorNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
