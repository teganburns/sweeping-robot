#!/usr/bin/env python  
import numpy as np

import collections
from threading import Lock

import rospy
from sensor_msgs.msg import Imu
#from sensehat_ros.msg import Environmental, IMU, Stick
#from sensehat_ros.srv import *

import tf2_ros

try:
    from sense_hat import SenseHat
except:
    # Fallback to sense-emu if sense-hat is not available (can be used both on x86 and ARM)
    from sense_emu import SenseHat

IMU_FRAME="imu_frame"

class Host(object):

    def __init__(self,
        rotation = 0,
        low_light = False,
        calibration = {},
        smoothing = 0,
        register_services = True,
        environmental_publishing = False,
        environmental_publishing_rate = 1,
        imu_publishing = True,
        #imu_publishing_mode = "get_gyroscope_rpy",
        imu_publishing_mode = "get_sensor_msg",
        imu_publishing_config = "1|1|1",
        imu_publishing_rate = 0.01,
        stick_publishing = False,
        stick_sampling = 0.2):
        """Constructor method"""

        #IMU_FRAME = rospy.get_param('~imu_frame', 'imu_link')
        IMU_FRAME="imu_frame"

        # Init sensor
        self.sense = SenseHat()
        self.sense.clear(0,0,0)
        self.sense.set_rotation(rotation)
        self.sense.low_light = low_light
        self.measures = {
            'humidity': self.sense.get_humidity,
            'temperature_from_humidity': self.sense.get_temperature_from_humidity,
            'temperature_from_pressure': self.sense.get_temperature_from_pressure,
            'pressure': self.sense.get_pressure,
            'compass': self.sense.get_compass,
        }


        # Init parameters
        self.imu_publishing = imu_publishing
        self.imu_publishing_mode = imu_publishing_mode
        self.imu_publishing_rate = imu_publishing_rate
        self.history = {}
        for measure in self.measures:
            self.history[measure] = collections.deque([], maxlen = smoothing if smoothing > 0 else None) if smoothing >= 0 else None

        # Init Lock to serialize access to the LED Matrix
        self.display_lock = Lock()

        # Register publishers
        if self.imu_publishing:
                self.sense.set_imu_config(*[i=="1" for i in imu_publishing_config.split("|")])
                self.imu_pub = rospy.Publisher("imu", Imu, queue_size=10)

        rospy.loginfo("sensehat_ros initialized")



    def __del__(self):
        if self.sense:
            self.sense.clear(0,0,0)

        rospy.loginfo("sensehat_ros destroyed")


##############################################################################
# Private methods
##############################################################################


    def _get_sensor_msg_imu(self, timestamp):
        # 1 g-unit is equal to 9.80665 meter/square second. # Linear Acceleration 
        # 1° × pi/180 = 0.01745rad # Angular velocity # Gyro
        
        gunit_to_mps_squ = 9.80665

        msg = Imu()
        msg.header.stamp = timestamp
        msg.header.frame_id = IMU_FRAME

        gyr = self.sense.get_gyroscope_raw()
        acc = self.sense.get_accelerometer_raw()

        msg.orientation.x = 0.0
        msg.orientation.y = 0.0
        msg.orientation.z = 0.0
        msg.orientation.w = 1.0
        msg.orientation_covariance = [99999.9, 0.0, 0.0, 0.0, 99999.9, 0.0, 0.0, 0.0, 99999.9]
        #msg.angular_velocity.x = gyr['x'] * np.pi
        msg.angular_velocity.x = round( gyr['x'] * ( np.pi / 180 ), 4 )
        msg.angular_velocity.y = round( gyr['y'] * ( np.pi / 180 ), 4 )
        msg.angular_velocity.z = round( gyr['z'] * ( np.pi / 180 ), 4 )
        msg.angular_velocity_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        msg.linear_acceleration.x = round((acc['x'] * gunit_to_mps_squ), 6 )
        msg.linear_acceleration.y = round((acc['y'] * gunit_to_mps_squ), 6 )
        msg.linear_acceleration.z = round((acc['z'] * gunit_to_mps_squ), 6 )
        
        #msg.linear_acceleration.x = np.radians( acc['x'] ) 
        #msg.linear_acceleration.y = np.radians( acc['y'] ) 
        #msg.linear_acceleration.z = np.radians( acc['z'] ) 

        msg.linear_acceleration_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


        return msg

    def _publish_sensor_msg_imu(self, event):
        imu = self._get_sensor_msg_imu(rospy.Time.now())
        rospy.logdebug( "Publishing IMU" )
        br = tf2_ros.TransformBroadcaster()
        self.imu_pub.publish(imu)



##############################################################################
# Run
##############################################################################

    def run(self):

        if self.imu_publishing:
            # Start publishing events
            rospy.Timer(rospy.Duration(self.imu_publishing_rate), self._publish_sensor_msg_imu)
            rospy.loginfo("sensehat_ros publishing Imu")

        rospy.spin()


if __name__ == '__main__':

    # Init node
    node = 'sensehat_ros'
    rospy.init_node(node, anonymous=True)

    s = Host()

    # Start publishing
    try:
        s.run()
    except rospy.ROSInterruptException:
        pass

