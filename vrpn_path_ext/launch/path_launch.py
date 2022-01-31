from pathlib import Path

from ament_index_python.packages import get_package_share_directory
import launch
import launch.actions
import launch.substitutions
import launch_ros.actions


parameters_file_path = Path(
    get_package_share_directory('vrpn_path_ext'),
    'config',
    'sample.params.yaml',
)


def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='vrpn_path_ext',
            node_executable='vrpn_client_node',
            output='screen',
            #emulate_tty=False,
            parameters=[parameters_file_path],
        ),
        launch_ros.actions.Node(
            package='vrpn_path_ext',
            node_executable='pathExtRos_new.py',
            output='screen',
            #emulate_tty=False,
            #parameters=[parameters_file_path],
        ),
    ])
