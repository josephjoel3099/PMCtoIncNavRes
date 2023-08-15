#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Quaternion

rospy.init_node('send_client_goal')

x_values = [1.0, -2.0, -5.0, 0.0]
y_values = [-9.0, -3.5, 1.0, 0.0]

x_values0 = [1.0, -5.5, 3.6, 0.0]
y_values0 = [6.0, 9.2, 1.8, -1.0]

client0 = actionlib.SimpleActionClient('jackal0/move_base', MoveBaseAction)
client1 = actionlib.SimpleActionClient('jackal1/move_base', MoveBaseAction)

rospy.loginfo("Waiting for move_base server...")

client0.wait_for_server()
client1.wait_for_server()

for i in range(len(x_values)):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.pose.position.x = x_values[i]
    goal.target_pose.pose.position.y = y_values[i]
    goal.target_pose.pose.orientation = Quaternion(0.0, 0.0, 0.0, 1.0)

    goal0 = MoveBaseGoal()
    goal0.target_pose.header.frame_id = 'map'
    goal0.target_pose.pose.position.x = x_values0[i]
    goal0.target_pose.pose.position.y = y_values0[i]
    goal0.target_pose.pose.orientation = Quaternion(0.0, 0.0, 0.0, 1.0)

    rospy.loginfo("Sending goal to Jackal0: x={}, y={}".format(x_values[i], y_values[i]))
    rospy.loginfo("Sending goal to Jackal1: x={}, y={}".format(x_values0[i], y_values0[i]))
    
    client0.send_goal(goal)
    
    client1.send_goal(goal0)

    client0.wait_for_result()
    client1.wait_for_result()

    if client0.get_state() == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("Jackal0 Goal reached successfully!")
    else:
        rospy.logwarn("Jackal0 Failed to reach the goal!")

    if client1.get_state() == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("Jackal1 Goal reached successfully!")
    else:
        rospy.logwarn("Jackal1 Failed to reach the goal!")

rospy.signal_shutdown("Finished sending goals.")