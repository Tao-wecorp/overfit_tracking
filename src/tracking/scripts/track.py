#!/usr/bin/env python

import cv2
from copy import deepcopy
import getch
import numpy as np
import os
import rospy
import rospkg
rospack = rospkg.RosPack()
from std_msgs.msg import Int8, String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from tracking.msg import BBox, BBoxes

# Helpers
from helpers.cvlib import Detection
detection = Detection()

from helpers.deep_features import DeepFeatures
deep_features = DeepFeatures()


class Detect:
    def __init__(self):
        rospy.init_node('detect_node', anonymous=True)
        rate = rospy.Rate(30)
        
        self.bridge = CvBridge()
        self.frame = None

        rospy.Subscriber('/stream/image', Image, self.img_callback)
        bboxes_pub = rospy.Publisher('/detection/bboxes', BBoxes, queue_size=10)
        
        frame_count = 0
        centroids = [(872, 581), (609, 654), (424, 645)]
        bboxes = [[845, 530, 899, 632], [574, 541, 644, 767], [386, 533, 462, 757]]
        while not rospy.is_shutdown():
            if self.frame is not None:      
                frame = deepcopy(self.frame)
                centroids, bboxes = detection.detect(frame)

                if len(centroids) != 0:
                    for cent in centroids:
                        cv2.rectangle(frame, (cent[0]-20, cent[1]-40), (cent[0]+20, cent[1]+40), (255,0,0), 1)

                cv2.imshow("", frame)
                cv2.waitKey(1)
                frame_count = frame_count + 1

            rate.sleep()

    def img_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data)
        except CvBridgeError as e:
            print(e)
        self.frame = cv_image


if __name__ == '__main__':
    try:
        Detect()
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()