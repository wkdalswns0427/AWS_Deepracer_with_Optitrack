def reward_function(params):
    
    # 딥레이서 관련 파라미터 읽어오기
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    
    # 0에 가까운 기본 보상
    reward = 1e-3

    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward = 1.0
        
    return float(reward)
