def reward_function(params):
    MAX_STEPS = 150  # Adjust based on your desired race duration
    MIN_SPEED = 2.0  # Minimum speed to encourage the model to move
    SPEED_THRESHOLD = 3.7  # Threshold for considering the car at a good speed
    ABS_STEERING_THRESHOLD = 15
    CURVE_ANGLE_THRESHOLD = 15  # Adjust for your track
    TARGET_LAP_TIME = 180.0  # 3 minutes in seconds
    MAX_SPEED = 4.9  # Maximum speed allowed

    heading = abs(params['heading'])
    is_crashed = params['is_crashed']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steps = params['steps']
    progress = params['progress']
    speed = params['speed']
    all_wheels_on_track = params['all_wheels_on_track']
    is_left_of_center = params['is_left_of_center']
    is_offtrack = params['is_offtrack']
    abs_steering = abs(params['steering_angle'])

    # Penalize if the car is too far away from the center
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    if distance_from_center <= marker_1:
        center_reward = 1.0
    elif distance_from_center <= marker_2:
        center_reward = 0.5
    elif distance_from_center <= marker_3:
        center_reward = 0.1
    else:
        center_reward = 1e-3

    atrack_reward = 0

    if not all_wheels_on_track or is_offtrack:
        atrack_reward = 1e-3
    elif speed < SPEED_THRESHOLD:
        atrack_reward = 0.5
    else:
        atrack_reward = 1.0

    crash_reward = 1e-3 if is_crashed or speed < SPEED_THRESHOLD else 1.2

    off_track_reward = 1e-3 if is_offtrack or speed < SPEED_THRESHOLD else 1.3

    straight_reward = 0.0
    breward = 0.0

    if heading <= CURVE_ANGLE_THRESHOLD and speed > SPEED_THRESHOLD:
        straight_reward += 1.3

    if distance_from_center <= marker_1 and heading <= CURVE_ANGLE_THRESHOLD:
        if speed >= SPEED_THRESHOLD:
            breward += 1.3

    total_reward = (
        1.2 * center_reward
        + 1.0 * atrack_reward
        + 1.0 * crash_reward
        + 1.2 * off_track_reward
        + 1.3 * straight_reward
        + 1.3 * breward
    )

    if abs_steering > ABS_STEERING_THRESHOLD:
        total_reward *= 0.8

    return float(total_reward)
