import os
import mvsdk

class CamGoalSua134gc():
    def __init__(self):
        # self.client = client
        # f_name = os.path.join(os.path.dirname(__file__), 'simplegoal.urdf')
        # self.goal = p.loadURDF(fileName=f_name,
        #            basePosition=[base[0], base[1], 1],
        #            physicsClientId=client)

        #init camera sua134gc

        print("Sua134gc initing")
        if 'hcamera' in locals().keys():
            print('hcamera exist')
        else:
            DevList = mvsdk.CameraEnumerateDevice()
            nDev = len(DevList)
            if nDev < 1:
                print("No camera was found!")
                return
            
            for i, DevInfo in enumerate(DevList):
                print("{}: {} {}".format(i, DevInfo.GetFriendlyName(), DevInfo.GetPortType()))
                i = 0 if nDev == 1 else int(input("Select camera: "))
                DevInfo = DevList[i]
                print(DevInfo)

            try:
                self.hCamera = mvsdk.CameraInit(DevInfo, -1, -1)
            except mvsdk.CameraException as e:
                print("CameraInit Failed({}): {}".format(e.error_code, e.message) )
                return

        
    
    def get_observation(self):
        # Get the position and orientation of the car in the simulation
        # pos, ang = p.getBasePositionAndOrientation(self.goal, self.client)
        # pos = pos[:1]
        # # Get the velocity of the car
        # #vel = p.getBaseVelocity(self.goal, self.client)[0][0:2]

        # # Concatenate position, orientation, velocity
        # observation = pos #+ ori + vel)
        
        #get one image frame from Sua134gc

        #calc obj from the image get the bonding box

        #retrun the bonding box
        observation = 1
        return observation
