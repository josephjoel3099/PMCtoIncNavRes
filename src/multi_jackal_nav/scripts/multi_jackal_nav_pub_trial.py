#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Quaternion
import time

def send_goal(client, x_values, y_values,e,cw):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.pose.position.x = x_values
    goal.target_pose.pose.position.y = y_values
    goal.target_pose.pose.orientation = Quaternion(0.0, 0.0, 0.0, 1.0)

    rospy.loginfo("Sending goal: x={}, y={}".format(x_values, y_values))
    client.send_goal(goal)

    # Pause to simulate an error (remove this in the actual implementation)
    if e == 1:  # Introduce error after the first goal is reached
        rospy.sleep(15)
        rospy.logwarn("Simulated fault: Robot failed to reach the first waypoint midway!")
        # client.cancel_goal()
    
    if cw == 1:
        client.wait_for_result()

    if client.get_state() == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("Goal reached successfully!")
    else:
        rospy.logwarn("Failed to reach the goal!")
        return False

    return True

if __name__ == "__main__":
    rospy.init_node('combined_send_client_goals')

    x_values_jackal0 = [4.0, -6.0]
    y_values_jackal0 = [2.0, 9.5]

    x_values_jackal1 = [4.0, -6.0]
    y_values_jackal1 = [2.0, 8.8]

    client_jackal0 = actionlib.SimpleActionClient('jackal0/move_base', MoveBaseAction)
    rospy.loginfo("Waiting for move_base server for Jackal0...")
    client_jackal0.wait_for_server()

    client_jackal1 = actionlib.SimpleActionClient('jackal1/move_base', MoveBaseAction)
    rospy.loginfo("Waiting for move_base server for Jackal1...")
    client_jackal1.wait_for_server()


    # Jackal0 goes to (4.0, 2.0)
    if send_goal(client_jackal0, x_values_jackal0[0], y_values_jackal0[0],1,0):
        rospy.loginfo("Jackal0 reached its job location successfully!")
    else:
        rospy.logerr("Jackal0 failed to reach its job location!")

        #Fault induced in Jackal0, returning Jackal0
        if send_goal(client_jackal0, x_values_jackal0[1], y_values_jackal0[1],0,0):
            rospy.loginfo("Jackal0 returned to its initial position successfully!")
        else:
            rospy.logerr("Jackal0 failed to return to its initial position!")
        
        # Sending Jackal1 instead
        if send_goal(client_jackal1, x_values_jackal1[0], y_values_jackal1[0],0,1):
            rospy.loginfo("Jackal1 reached its job location successfully!")
        else:
            rospy.logerr("Jackal1 failed to reach its job location!")

    # Jackal1 returns to initial position (-6.0, 8.8)
    if send_goal(client_jackal1, x_values_jackal1[1], y_values_jackal1[1],0,1):
        rospy.loginfo("Jackal1 returned to its initial position successfully!")
    else:
        rospy.logerr("Jackal1 failed to return to its initial position!")

    rospy.signal_shutdown("Finished sending goals.")
