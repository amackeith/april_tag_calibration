#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import AprilTagDetectionArray, AprilTagDetection
print("HELLO arthur")
import pickle 


class gather_data():

    def __init__(self):
        self.list_of_positions = []
        self._tag_sub = rospy.Subscriber(
            'apriltag_detector_node/detections',
            AprilTagDetectionArray,
            self._tag_cb,
            queue_size=1
        )        
    
    def _tag_cb(self, msg):
        print(len(msg.detections), len(self.list_of_positions))
        for det in msg.detections:
            
            pose = {}
            pose['transformation'] = [det.transform.translation.x, det.transform.translation.y,det.transform.translation.z]
            pose['center'] = det.center
            pose['corners'] = det.corners
            pose['error'] = det.pose_error
            pose['decision_margin'] = det.decision_margin
            pose['tag_id']  = det.tag_id
            self.list_of_positions.append(pose)

        if len(self.list_of_positions) > 1000:
            self.save_images()
            exit()

    def save_images(self):
        f = open("/data/pose_info.obj", "wb")
        pickle.dump(self.list_of_positions, f)
        exit()


if __name__ == "__main__":
    rospy.init_node("tag_collector")
    node = gather_data()
    rospy.spin()
