from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
import os


def generate_launch_description():

    pkg_path = os.path.expanduser('~/cart_sim_ws/src/logistic_cart_sim')

    urdf_file = os.path.join(pkg_path, 'urdf/logistic_cart.urdf.xacro')
    world_file = os.path.join(pkg_path, 'worlds/warehouse.world')

    robot_description = ParameterValue(
        Command(['xacro ', urdf_file]),
        value_type=str
    )

    return LaunchDescription([

        # Start Gazebo Harmonic
        ExecuteProcess(
            cmd=['gz', 'sim', world_file],
            output='screen'
        ),

        # Publish robot model
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),

        # Spawn robot into Gazebo
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-topic', 'robot_description',
                '-name', 'logistic_cart'
            ],
            output='screen'
        ),

        # Bridge simulation clock to ROS
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
               	'/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist'
    	    ],
   	    output='screen'
	)
    ])
