import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class StreamControllerNode(Node):
    def __init__(self):
        super().__init__("tams_stream_controller")
        self.targets = {"EIH": 0.0, "GT": 0.0, "GS": 0.0}
        self.create_subscription(String, "tams/bitrate_targets", self.targets_callback, 10)
        self.publisher = self.create_publisher(String, "tams/encoder_state", 10)
        self.create_timer(0.20, self.publish_state)

    def targets_callback(self, msg: String):
        try:
            payload = json.loads(msg.data)
            targets = payload.get("targets_mbps", {})
            self.targets = {
                "EIH": float(targets.get("EIH", self.targets["EIH"])),
                "GT": float(targets.get("GT", self.targets["GT"])),
                "GS": float(targets.get("GS", self.targets["GS"])),
            }
        except (json.JSONDecodeError, TypeError, ValueError):
            return

    def publish_state(self):
        msg = String()
        msg.data = json.dumps({"encoder_target_mbps": self.targets})
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = StreamControllerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
