#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
from pynput.keyboard import Listener, Key

class ArmController:
    def __init__(self):
        # Khởi tạo ROS node
        rospy.init_node('arm_keyboard_controller', anonymous=True)

        # Tạo publisher cho mỗi khớp
        self.prismatic_pub = rospy.Publisher('/prismatic_controller/command', Float64, queue_size=10)
        self.rotation_pub = rospy.Publisher('/rotation_controller/command', Float64, queue_size=10)

        # Thiết lập vận tốc ban đầu
        self.linear_vel = 0.05  # m/s cho khớp tịnh tiến
        self.angular_vel = 1.0  # rad/s cho khớp xoay

        # Vận tốc ban đầu
        self.prismatic_vel = 0.0
        self.rotation_vel = 0.0

        # Tần số vòng lặp
        self.rate = rospy.Rate(10)  # 10 Hz

        # Khởi động listener cho bàn phím
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        """Xử lý khi nhấn phím"""
        try:
            if key.char == 'w':  # Di chuyển lên
                self.prismatic_vel = self.linear_vel
            elif key.char == 's':  # Di chuyển xuống
                self.prismatic_vel = -self.linear_vel
            elif key.char == 'a':  # Xoay trái
                self.rotation_vel = self.angular_vel
            elif key.char == 'd':  # Xoay phải
                self.rotation_vel = -self.angular_vel
            elif key.char == 'q':  # Tăng tốc độ lên/xuống
                self.linear_vel += 0.01
                print(f"Tốc độ tịnh tiến: {self.linear_vel}")
            elif key.char == 'z':  # Giảm tốc độ lên/xuống
                self.linear_vel = max(0.01, self.linear_vel - 0.01)
                print(f"Tốc độ tịnh tiến: {self.linear_vel}")
            elif key.char == 'e':  # Tăng tốc độ xoay
                self.angular_vel += 0.1
                print(f"Tốc độ xoay: {self.angular_vel}")
            elif key.char == 'c':  # Giảm tốc độ xoay
                self.angular_vel = max(0.1, self.angular_vel - 0.1)
                print(f"Tốc độ xoay: {self.angular_vel}")
            elif key.char == 'f':  # Thoát chương trình
                rospy.signal_shutdown("User requested shutdown")
        except AttributeError:
            pass

    def on_release(self, key):
        """Xử lý khi nhả phím"""
        try:
            if key.char in ['w', 's']:
                self.prismatic_vel = 0.0
            elif key.char in ['a', 'd']:
                self.rotation_vel = 0.0
        except AttributeError:
            pass

    def control_loop(self):
        """Vòng lặp chính điều khiển cánh tay robot"""
        print("Keyboard Control for Robotic Arm")
        print("W: Lên, S: Xuống, A: Quay trái, D: Quay phải")
        print("Q/Z: Tăng/Giảm tốc độ tịnh tiến, E/C: Tăng/Giảm tốc độ xoay")
        print("F: Thoát chương trình")

        while not rospy.is_shutdown():
            # Gửi lệnh vận tốc
            self.prismatic_pub.publish(self.prismatic_vel)
            self.rotation_pub.publish(self.rotation_vel)
            self.rate.sleep()

if __name__ == '__main__':
    try:
        controller = ArmController()
        controller.control_loop()
    except rospy.ROSInterruptException:
        pass
