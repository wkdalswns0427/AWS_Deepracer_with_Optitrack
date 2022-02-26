import math
def reward_function(params):
    # Example of rewarding the agent to follow center line

    # Read input parameters
    track_width = params['track_width']
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    speed = params['speed']
    angle = abs(params['steering_angle'])
    heading = params['heading']
    isLeft = params['is_left_of_center']
    
    # rewards for each cases
    reward_1 = 1.0
    reward_2 = 1.0
    reward_3 = 2.0

    # 5markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.2 * track_width
    marker_25 = 0.25 * track_width
    marker_3 = 0.3 * track_width
    marker_35 = 0.35 * track_width
    marker_4 = 0.4 * track_width
    marker_5 = 0.5 * track_width
    
    # dirextion
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    if closest_waypoints[1] == len(waypoints)-1:
        future_point = waypoints[1]
    else: 
        future_point = waypoints[closest_waypoints[1]+1] 
    direction_uno = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    direction_uno = math.degrees(direction_uno)
    direction_dos = math.atan2(future_point[1] - next_point[1], future_point[0] - next_point[0])
    direction_dos = math.degrees(direction_uno)
    
    # manage off-track
    if all_wheels_on_track:
      if distance_from_center <= marker_1:
          reward_1 = 1.4
      elif distance_from_center <= marker_2:
          reward_1 = 1.3
      elif distance_from_center <= marker_25:
          reward_1 = 1.3
      elif distance_from_center <= marker_3:
          reward_1 = 1.2
      elif distance_from_center <= marker_35:
          reward_1 = 1.2
      elif distance_from_center <= marker_4:
          reward_1 = 1.2
      elif distance_from_center <= marker_5:
          reward_1 = 0.1
      else:
          reward_1 = 1e-3
    else:
        reward_1 = 1e-3
    
     # manage speed
    dirdiff = abs(direction_uno - direction_dos)    
    if dirdiff < 2:
        if 1.0 <speed and speed <= 2.0:
            reward_2 = 1.5
        elif speed <= 1.0:
            reward_2 = 0.3
            
    # manage angle
    STEERING_THRESHOLD = 15
    if angle > STEERING_THRESHOLD:
        reward_3 *= 0.2
            
   
    reward = 0.6*reward_1 + 0.25*reward_2 + 0.15*reward_3
    
    if not isLeft:
        reward *= 0.6
    
    return float(reward)
