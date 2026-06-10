import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression
import time




def generate_launch_description():
    arg_robot_name = 'race_station'
    robot_bringup = arg_robot_name + '_bringup'

    # simulation
    simulation_drivers = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','simulation','simulation_drivers.launch.py')]),
        launch_arguments = {'arg_robot_name': arg_robot_name}.items()    
    )

    # robot localization
    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','simulation','localization_sim.launch.py')]),
        launch_arguments = {'arg_robot_name': arg_robot_name}.items()  
    )
    
    #description URDF
    description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','description.launch.py')]),
        launch_arguments = {'arg_robot_name': arg_robot_name}.items()  
    )

    # c2 topside
    mvp_c2_top = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','mvp_c2_topside.launch.py')]),
        launch_arguments = {'arg_robot_name': arg_robot_name}.items()  
    )

    return LaunchDescription([
        simulation_drivers,
        localization,
        description,
        mvp_c2_top,
    ])
