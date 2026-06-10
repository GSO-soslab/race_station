import os
from launch import LaunchDescription
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


# from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    robot_name = 'race_station'
    robot_bringup = 'race_auv' + '_bringup'
    topside_setting_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'c2', 'mvp_c2.yaml') 
    usbl_traffic_manager_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'evologics', 'mvp_c2_usbl_commander_traffic.yaml')

    # commander node
    commander_node =  Node(
                            package='mvp_c2',
                            namespace=robot_name,
                            executable='mvp_c2_commander_ros',
                            name='mvp_c2_commander',
                            output='screen',
                            prefix=['stdbuf -o L'],
                            parameters=[topside_setting_file],
                            remappings=[
                                ('mvp_c2/commander/dccl_msg_tx', 'mvp_c2/traffic_control/dccl_msg_tx'),
                                ('mvp_c2/commander/dccl_msg_rx', 'mvp_c2/traffic_control/dccl_msg_controlled_rx'),
                            ]
                        )
    
    # traffic manager for usbl
    usbl_traffic_manager =  Node(
                                package='mvp_c2',
                                namespace=robot_name,
                                executable='mvp_c2_traffic_control_ros',
                                name='mvp_c2_usbl_traffic_control',
                                output='screen',
                                prefix=['stdbuf -o L'],
                                parameters=[usbl_traffic_manager_file],
                                remappings=[
                                    ('mvp_c2/traffic_control/dccl_msg_controlled_tx', 'acomms/data_to_send_bytes'),
                                    ('mvp_c2/traffic_control/dccl_msg_rx', 'acomms/received_data_bytes'),
                                ]
                            )
    
    return LaunchDescription([
        usbl_traffic_manager,
        commander_node,   
    ])
