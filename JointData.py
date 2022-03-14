class JOINTS:

    def __init__(self, data, joints_description):
        self.data = data
        self.joints_description = joints_description


    def joint_data(self): # , data, joints_description):

     import pandas as pd

     for skeleton in self.data.skeletons:
         data = pd.DataFrame(skeleton.head.projection)

     return data
