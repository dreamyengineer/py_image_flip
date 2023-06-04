import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
# the image input and output names should be changed if using different robot that unigo1
class ImageFlipNode(Node):
    def __init__(self):
        super().__init__('image_flip_node')
        self.bridge = CvBridge()
        self.flipped_image_pub = self.create_publisher(Image, '/camera_face_camera/flipped_image_raw', 10)#<--- CHANGE ME
        self.image_sub = self.create_subscription(
            Image,
            '/camera_face_camera/image_raw',#<--- CHANGE ME
            self.image_callback,
            10
        )

    def image_callback(self, image_msg):
        # Convert ROS image message to OpenCV format
        cv_image = self.bridge.imgmsg_to_cv2(image_msg, desired_encoding='bgr8')
        
        # Flip the image vertically
        flipped_image = cv2.flip(cv_image, 0)
        
        # Convert the flipped image back to ROS image message
        flipped_image_msg = self.bridge.cv2_to_imgmsg(flipped_image, encoding='bgr8')
        
        # Publish the flipped image
        self.flipped_image_pub.publish(flipped_image_msg)

def main(args=None):
    rclpy.init(args=args)
    image_flip_node = ImageFlipNode()
    rclpy.spin(image_flip_node)
    image_flip_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

