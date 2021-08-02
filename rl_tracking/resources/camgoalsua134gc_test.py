from rl_tracking.resources.camgoalsua134gc import CamGoalSua134gc


class test_camgoalsua134gc():
    def __init__(self):
        self.hcamera = 0
    
    def reset(self):
        self.camgoal = CamGoalSua134gc()



if __name__ == "__main__":
    test = test_camgoalsua134gc()
    test.reset()
    while 1:
        test.camgoal.get_observation()