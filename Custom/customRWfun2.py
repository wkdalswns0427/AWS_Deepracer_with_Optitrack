def reward_function(params):
    # Example of rewarding the agent to follow center line

    # Read input parameters
    track_width = params['track_width']
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.2 * track_width
    marker_25 = 0.25 * track_width
    marker_3 = 0.3 * track_width
    marker_35 = 0.35 * track_width
    marker_4 = 0.4 * track_width
    marker_5 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if all_wheels_on_track:
      if distance_from_center <= marker_1:
          reward = 1.4
      elif distance_from_center <= marker_2:
          reward = 1.3
      elif distance_from_center <= marker_25:
          reward = 1.25
      elif distance_from_center <= marker_3:
          reward = 1.2
      elif distance_from_center <= marker_35:
          reward = 1.15
      elif distance_from_center <= marker_4:
          reward = 0.5
      elif distance_from_center <= marker_5:
          reward = 0.1
      else:
          reward = 1e-3
    else:
      reward = 1e-3

    return float(reward)
