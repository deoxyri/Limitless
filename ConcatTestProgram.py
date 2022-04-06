import pandas as pd

a = [0, 0, 0]
a = pd.DataFrame(a)

a = a+1
print(a)

var_joints_recorded_data = {}

joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                      'left_hand', 'right_collar', 'right_shoulder',
                      'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                      'right_hip', 'right_knee', 'right_ankle']
i = 0
while i < len(joints_description):
    var_joints_recorded_data[joints_description[i] + '_df'] = pd.read_excel(
        'X:\Limitless\A - Skeletal Tracking\Tracking Programs\{}_Data_Variable.xlsx'.format(joints_description[i]))
    i += 1

head_data = var_joints_recorded_data['head_df']
print(head_data)
print(head_data[0][0])
print(head_data.size/3)