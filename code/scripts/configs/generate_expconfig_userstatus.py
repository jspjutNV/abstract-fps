### importing libraries ###
import numpy as np

### experimentconfig ###

f_ex = open("experimentconfig.Any", "w")

refresh_rates = [360, 240, 120, 60]
latencies = [0.025, 0.05, 0.08] # sec
frame_lag_counts = [4, 3, 1, 0, 16, 10, 5, 2, 28, 18, 9, 4]
min_latency = 0.012 # sec
exp_modes = ['training', 'real']

count_static_trials = 0
count_straight_fly_trials = 20
count_stray_fly_easy_trials = 50
count_stray_fly_hard_trials = 0
count_strafe_jump_trials = 50

global_setting_txt = \
'''
// copy this file to experimentconfig.Any before first run
{
  // Information related to this file
  "settingsVersion": 1, // Used for parsing this file

  // General settings for the experiment
  "appendingDescription": "default", // Description of this file
  "sceneName": "eSports Simple Hallway", // Maybe don't need this? Or maybe this ends up belonging to individual trials
  "taskType": "target", // Task type, can be "target" or "reaction"
  "feedbackDuration": 0.0, // Time allocated for providing user feedback
  "readyDuration": 0.25, // Time allocated for preparing for trial
  "taskDuration": 6.0, // Maximum duration allowed for completion of the task
  "maxClicks": 3600,    // Maximum number of clicks to allow per trial
  "firePeriod" : 0.0, // Maximum rate of fire to allow in a trial
  "autoFire": true,  // Whether the weapon fires automatically when the left mouse is held down
  "damagePerSecond": 1,
  "sessionOrder": "random", // Session ordering, can be "Random", "Serial"

  // Create a sessions table containing information related to sessions
  // These sessions attempt to have fixed latency with variable frame rate
  // all run the same set of trial conditions
'''

session_txt = \
'''
  "sessions": [
'''

session_idx = 0
for latency in latencies:
    for refresh_rate in refresh_rates:
        session_idx += 1       
        for exp_mode in exp_modes:
          num_frame_delay = frame_lag_counts[session_idx - 1]
          session_txt +=\
'''
    {
      "id": "s%d-%s", // Session ID
      "frameDelay": %d, // Session frame delay (in frames)
      "frameRate": %d, // Session frame rate (in frames per second)
      "selectionOrder": "random", // Selection order for trials within this session
      "expMode": "%s", // Experiment mode ("real" or "training")
      "trials": [''' % (session_idx, exp_mode, num_frame_delay, refresh_rate, exp_mode)

            # num_frame_delay = np.round((latency - (min_latency + 0.5 / refresh_rate)) / (1/refresh_rate))
          if count_static_trials > 0: session_txt          += "\n        {\"id\": \"static\", \"count\": %d}," % count_static_trials
          if count_straight_fly_trials > 0: session_txt    += "\n        {\"id\": \"straight_fly\", \"count\": %d}," % count_straight_fly_trials
          if count_stray_fly_easy_trials > 0: session_txt  += "\n        {\"id\": \"stray_fly_easy\", \"count\": %d}," % count_stray_fly_easy_trials
          if count_stray_fly_hard_trials > 0: session_txt  += "\n        {\"id\": \"stray_fly_hard\", \"count\": %d}," % count_stray_fly_hard_trials
          if count_strafe_jump_trials > 0: session_txt     += "\n        {\"id\": \"strafe_jump\", \"count\": %d}," % count_strafe_jump_trials
          session_txt += "\n      ]\n    },"
session_txt += \
'''
  ],
'''

trial_txt = \
'''
  // static = stationary
  // straight_fly = fixed direction
  // stray_fly = change direction every 0.4 ~ 0.8 second
  // strafe_jump = left/right strafing and jumping as in real games
  // Trial table (contains detailed target info for each trial)
  "targets": [
    {
      "id": "static",
    "elevationLocked": false,
      "speed": [ 0, 0 ],
      "visualSize": [ 0.01, 0.01 ],
      "eccH": [ 5.0, 15.0 ],
      "eccV": [ 0.0, 1.0 ],
      "motionChangePeriod": [ 1000000, 1000000 ],
      "jumpEnabled": false
    },
    {
      "id": "straight_fly",
    "elevationLocked": false,
      "speed": [ 10, 20 ],
      "visualSize": [ 0.018, 0.018 ],
      "eccH": [ 5.0, 15.0 ],
      "eccV": [ 0.0, 1.0 ],
      "motionChangePeriod": [ 1000000, 1000000 ],
      "jumpEnabled": false
    },
    {
      "id": "stray_fly_hard",
    "elevationLocked": false,
      "speed": [ 8, 15 ],
      "visualSize": [ 0.01, 0.01 ],
      "eccH": [ 5.0, 15.0 ],
      "eccV": [ 0.0, 1.0 ],
      "motionChangePeriod": [ 0.5, 0.6 ],
      "jumpEnabled": false
    },
    {
      "id": "stray_fly_easy",
    "elevationLocked": false,
      "speed": [ 10, 20 ],
      "visualSize": [ 0.018, 0.018 ],
      "eccH": [ 5.0, 15.0 ],
      "eccV": [ 0.0, 1.0 ],
      "motionChangePeriod": [ 1.0, 1.2 ],
      "jumpEnabled": false
    },
    {
      "id": "strafe_jump",
      "elevationLocked": true,
      "speed": [ 10, 20 ],
      "visualSize": [ 0.018, 0.018 ],
      "eccH": [ 5.0, 15.0 ],
      "eccV": [ 0.0, 1.0 ],
      "motionChangePeriod": [ 1.0, 1.2 ],
      "jumpEnabled": true,
      "distance": [ 13, 15],
      "jumpPeriod": [ 0.3, 0.6 ],
      "jumpSpeed": [7, 7],
      "accelGravity": [20, 20]
    }
  ],

  // A set of controls for reaction time experiments
  "reactions": [
    {
      "id": "r1",
      "minimumForeperiod": 1.5,
      "intensities": [ 0.4, 1.0 ],
      "intensityCounts": [ 3, 10 ]
    }
  ]
}
'''

expconfig_txt = global_setting_txt + session_txt + trial_txt

#print(txt)

f_ex.write(expconfig_txt)
f_ex.close()



### userstatus.Any ###

### variables ###
# use the found ordering to generate the user status file.
f_user = open("userstatus.Any", "w")
subjects = ['JC','LN','MB','JA','DM','CM','EP','SS']
condition_count = 12

# first, generate the ordering.
ordering_mat = np.zeros([len(subjects),condition_count])

while(True):
    
    # generate an ordering.
    for i in range(len(subjects)):
        ordering_mat[i,:] = np.random.permutation(condition_count) + 1

    # check how well conditions are distributed.
    ordering_count = np.zeros([condition_count,condition_count]) # count the number of each condition appearing at each order.
    for i in range(condition_count):
        matching_mat = np.zeros([len(subjects),condition_count])
        matching_mat[ordering_mat == (i+1)] = 1
        ordering_count[i,:] = np.sum(matching_mat,0)
        #print(np.sum(matching_mat,0))
    
    if np.max(ordering_count) < 3:
        # This conditional statements accepts an ordering only if any condition appears less than 3 times at certain order.
        # NOTE: I tried an ideal case of setting the limit to exactly once. That resulted in an almost infinite loop.
        # Settling down on the practical compromise of 'less than 3' for now.
        break

print(ordering_mat)

print(ordering_count)

txt_before_user_setting = \
'''
{
    settingsVersion : 1,
  // Create a user table with information about session ordering and completed sessions
  users: [
'''

txt_user_setting = ''

for subject_i, subject in enumerate(subjects):
    txt_user_setting += \
'''    {
      "id": "%s",
      "sessions": [''' % subject
    for order_i in range(condition_count):
        condition_i = ordering_mat[subject_i, order_i]
        txt_user_setting += '"s%d-training", "s%d-real", ' % (condition_i, condition_i)
    
    txt_user_setting += \
'''],
      "completedSessions": []
    },
'''

txt_after_user_setting = \
'''
  ]
}
'''

userconfig_txt = txt_before_user_setting + txt_user_setting + txt_after_user_setting

f_user.write(userconfig_txt)
f_user.close()
