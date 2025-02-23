from . import Obstacle, StationaryObstacle, RotatingObstacle, InvisibleObstacle, ObstacleGroup, HorizontalMovingObstacle

def get_obstacle_list(player_center: tuple[int, int], player_normal_distance: int, player_angular_speed: float, height: int, speed: int, color: tuple[int, int, int]) -> list[Obstacle]: 
    return [
        StationaryObstacle(player_center[0] + player_normal_distance, 0, player_normal_distance * 2, height, speed, 2, color),
        StationaryObstacle(player_center[0] - player_normal_distance, 0, player_normal_distance * 2, height, speed, 2, color),
        StationaryObstacle(player_center[0], 0, player_normal_distance, height, speed, 2, color),
        StationaryObstacle(player_center[0] + player_normal_distance / 2 + 20, 0, player_normal_distance - 20, player_normal_distance * 0.8, speed, 2, color),
        StationaryObstacle(player_center[0] - player_normal_distance / 2 - 20, 0, player_normal_distance - 20, player_normal_distance * 0.8, speed, 2, color),
        RotatingObstacle(player_center[0], 0, player_normal_distance * 2, height, speed, 3, color, player_angular_speed, True),
        RotatingObstacle(player_center[0], 0, player_normal_distance * 2, height, speed, 3, color, player_angular_speed, False),
        RotatingObstacle(player_center[0] - player_normal_distance, 0, player_normal_distance * 2, height, speed, 3, color, player_angular_speed, True),
        RotatingObstacle(player_center[0] + player_normal_distance, 0, player_normal_distance * 2, height, speed, 3, color, player_angular_speed, False),
        ObstacleGroup([
                StationaryObstacle(player_center[0] + player_normal_distance * 2, 0, player_normal_distance * 2, height, speed, 3, color), 
                StationaryObstacle(player_center[0] - player_normal_distance * 2, 0, player_normal_distance * 2, height, speed, 3, color)
            ]),
        ObstacleGroup([
                StationaryObstacle(player_center[0] + player_normal_distance, -player_normal_distance, player_normal_distance, height, speed, 3, color), 
                StationaryObstacle(player_center[0] - player_normal_distance, 0, player_normal_distance * 2, height, speed, 3, color)
            ]),
        ObstacleGroup([
                StationaryObstacle(player_center[0] - player_normal_distance, -player_normal_distance, player_normal_distance, height, speed, 3, color), 
                StationaryObstacle(player_center[0] + player_normal_distance, 0, player_normal_distance * 2, height, speed, 3, color)
            ]),
        InvisibleObstacle(player_center[0] + player_normal_distance, 0, player_normal_distance * 2, height, speed, 2, color),
        InvisibleObstacle(player_center[0] - player_normal_distance, 0, player_normal_distance * 2, height, speed, 2, color),
        HorizontalMovingObstacle(player_center[0] + player_normal_distance, player_center[0] - player_normal_distance, 0, player_normal_distance * 2, height, speed, 2, color, player_center, player_normal_distance)
    ]
