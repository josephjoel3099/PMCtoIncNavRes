#!/usr/bin/env python

import rospy
import numpy as np
import random as rm

#battery states
states = ["High", "Medium", "Low"]

#possible sequence of events
transitionName = [["HH", "HM", "HL"], ["MH", "MM", "ML"], ["LH", "LM", "LL"]]

#transition probabilities
transitionMatrix = [[0.8,0.1,0.1],[0,0.7,0.3],[0,0,1]]

def battery_forecast(steps, starting_state, final_state):
    # Choose the starting state
    list_activity = []
    count = 0
    
    for iterations in range(1,10000):
        batteryState = starting_state
        batteryStateList = [batteryState]
        i = 0
        # To calculate the probability of the batteryStateList
        prob = 1
        while i != steps:
            if batteryState == "High":
                change = np.random.choice(transitionName[0],replace=True,p=transitionMatrix[0])
                if change == "HH":
                    prob = prob * 0.7
                    batteryStateList.append("High")
                    pass
                elif change == "HM":
                    prob = prob * 0.2
                    batteryState = "Medium"
                    batteryStateList.append("Medium")
                else:
                    prob = prob * 0.1
                    batteryState = "Low"
                    batteryStateList.append("Low")
            elif batteryState == "Medium":
                change = np.random.choice(transitionName[1],replace=True,p=transitionMatrix[1])
                if change == "MH":
                    prob = prob * 0
                    batteryStateList.append("High")
                    pass
                elif change == "MM":
                    prob = prob * 0.7
                    batteryState = "Medium"
                    batteryStateList.append("Medium")
                else:
                    prob = prob * 0.3
                    batteryState = "Low"
                    batteryStateList.append("Low")
            elif batteryState == "Low":
                change = np.random.choice(transitionName[2],replace=True,p=transitionMatrix[2])
                if change == "LH":
                    prob = prob * 0
                    batteryStateList.append("High")
                    pass
                elif change == "LM":
                    prob = prob * 0
                    batteryState = "Medium"
                    batteryStateList.append("Medium")
                else:
                    prob = prob * 1
                    batteryState = "Low"
                    batteryStateList.append("Low")
            i += 1  
        list_activity.append(batteryStateList)

    # Iterate through the list to get a count of all activities ending in state:'Run'
    for smaller_list in list_activity:
        if(smaller_list[2] == final_state):
            count += 1

    # Calculate the probability of starting from state:'Sleep' and ending at state:'Run'
    return (count/10000) * 100

print(battery_forecast(5,"High","High"))