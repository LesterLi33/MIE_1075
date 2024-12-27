# MIE_1075
Project Name:
Shopping Assistant Robot:

#### Autonomous Navigation
Simulation is performed using ROS Noetic (http://wiki.ros.org/noetic/Installation/Ubuntu).
This folder is the workspace folder. Within this folder please run `catkin_make` or `catkin build` using the terminal.

#####  Running the simulation
- Start gazebo
```
roslaunch turtlebot3_gazebo turtlebot3_store.launch
```

- Start rviz
```
roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=<location of the map>
```

Before providing a goal pose, a rough estimate of the inital state must be given using the `2D Pose Estimate` button on rviz. Then the goal pose can be provided using `2D Nav Goal` button.
