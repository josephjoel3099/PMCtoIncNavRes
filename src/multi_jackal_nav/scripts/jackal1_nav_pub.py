#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Quaternion

rospy.init_node('send_client_goal')

x_values = [1.0, -2.0, -5.0, 0.0]
y_values = [-9.0, -3.5, 1.0, -2.0]

client = actionlib.SimpleActionClient('jackal1/move_base', MoveBaseAction)
rospy.loginfo("Waiting for move_base server...")
client.wait_for_server()

for i in range(len(x_values)):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.pose.position.x = x_values[i]
    goal.target_pose.pose.position.y = y_values[i]
    goal.target_pose.pose.orientation = Quaternion(0.0, 0.0, 0.0, 1.0)

    rospy.loginfo("Sending goal: x={}, y={}".format(x_values[i], y_values[i]))
    client.send_goal(goal)
    client.wait_for_result()

    if client.get_state() == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("Goal reached successfully!")
    else:
        rospy.logwarn("Failed to reach the goal!")

rospy.signal_shutdown("Finished sending goals.")