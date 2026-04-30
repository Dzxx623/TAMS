import math

import rclpy
from geometry_msgs.msg import TwistStamped
from rclpy.node import Node
from std_msgs.msg import Bool, String


class PhaseInferenceNode(Node):
    def __init__(self):
        super().__init__("tams_phase_inference")
        self.declare_parameter("speed_threshold", 0.01)
        self.declare_parameter("descending_speed_threshold", 0.01)
        self.declare_parameter("align_dwell_time", 0.20)
        self.declare_parameter("pre_release_dwell_time", 0.20)
        self.phase = "Reach"
        self.gripper_closed = False
        self.previous_gripper_closed = False
        self.speed = 0.0
        self.vertical_speed = 0.0
        self.descending_time = 0.0
        self.previous_time = self.get_clock().now()
        self.create_subscription(TwistStamped, "tams/end_effector_velocity", self.velocity_callback, 10)
        self.create_subscription(Bool, "tams/gripper_closed", self.gripper_callback, 10)
        self.publisher = self.create_publisher(String, "tams/phase", 10)
        self.create_timer(0.02, self.update_phase)

    def velocity_callback(self, msg: TwistStamped):
        vx = msg.twist.linear.x
        vy = msg.twist.linear.y
        vz = msg.twist.linear.z
        self.speed = math.sqrt(vx * vx + vy * vy + vz * vz)
        self.vertical_speed = vz

    def gripper_callback(self, msg: Bool):
        self.gripper_closed = bool(msg.data)

    def update_phase(self):
        now = self.get_clock().now()
        dt = max((now - self.previous_time).nanoseconds * 1e-9, 0.0)
        self.previous_time = now
        speed_threshold = float(self.get_parameter("speed_threshold").value)
        descending_speed_threshold = float(self.get_parameter("descending_speed_threshold").value)
        align_dwell_time = float(self.get_parameter("align_dwell_time").value)
        pre_release_dwell_time = float(self.get_parameter("pre_release_dwell_time").value)
        if self.gripper_closed and not self.previous_gripper_closed:
            self.phase = "Grasp"
        elif not self.gripper_closed and self.previous_gripper_closed:
            self.phase = "Release"
        elif self.speed <= speed_threshold:
            self.phase = self.phase
        else:
            if self.vertical_speed < -descending_speed_threshold:
                self.descending_time += dt
            else:
                self.descending_time = 0.0
            if not self.gripper_closed:
                self.phase = "Align" if self.descending_time >= align_dwell_time else "Reach"
            else:
                self.phase = "Pre-release" if self.descending_time >= pre_release_dwell_time else "Transport"
        self.previous_gripper_closed = self.gripper_closed
        msg = String()
        msg.data = self.phase
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PhaseInferenceNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
