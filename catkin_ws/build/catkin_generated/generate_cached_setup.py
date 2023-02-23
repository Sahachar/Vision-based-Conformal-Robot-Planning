# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import stat
import sys

# find the import for catkin's python package - either from source space or from an installed underlay
if os.path.exists(os.path.join('/opt/ros/noetic/share/catkin/cmake', 'catkinConfig.cmake.in')):
    sys.path.insert(0, os.path.join('/opt/ros/noetic/share/catkin/cmake', '..', 'python'))
try:
    from catkin.environment_cache import generate_environment_script
except ImportError:
    # search for catkin package in all workspaces and prepend to path
    for workspace in '/home/sah/osbert/catkin_ws/devel;/home/sah/meam520_ws/devel_isolated/python_orocos_kdl;/home/sah/meam520_ws/devel_isolated/meam520_labs;/home/sah/meam520_ws/devel_isolated/panda_simulator_examples;/home/sah/meam520_ws/devel_isolated/panda_simulator;/home/sah/meam520_ws/devel_isolated/panda_sim_moveit;/home/sah/meam520_ws/devel_isolated/panda_gazebo;/home/sah/meam520_ws/devel_isolated/panda_sim_custom_action_server;/home/sah/meam520_ws/devel_isolated/panda_sim_controllers;/home/sah/meam520_ws/devel_isolated/panda_hardware_interface;/home/sah/meam520_ws/devel_isolated/orocos_kinematics_dynamics;/home/sah/meam520_ws/devel_isolated/franka_tools;/home/sah/meam520_ws/devel_isolated/franka_ros_interface;/home/sah/meam520_ws/devel_isolated/franka_ros_controllers;/home/sah/meam520_ws/devel_isolated/franka_panda_description;/home/sah/meam520_ws/devel_isolated/franka_moveit;/home/sah/meam520_ws/devel_isolated/franka_interface;/home/sah/meam520_ws/devel_isolated/franka_core_msgs;/opt/ros/noetic'.split(';'):
        python_path = os.path.join(workspace, 'lib/python3/dist-packages')
        if os.path.isdir(os.path.join(python_path, 'catkin')):
            sys.path.insert(0, python_path)
            break
    from catkin.environment_cache import generate_environment_script

code = generate_environment_script('/home/sah/osbert/catkin_ws/devel/env.sh')

output_filename = '/home/sah/osbert/catkin_ws/build/catkin_generated/setup_cached.sh'
with open(output_filename, 'w') as f:
    # print('Generate script for cached setup "%s"' % output_filename)
    f.write('\n'.join(code))

mode = os.stat(output_filename).st_mode
os.chmod(output_filename, mode | stat.S_IXUSR)
