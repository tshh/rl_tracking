import os
import mvsdk
import numpy as np
import cv2

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
            


            # 获取相机特性描述
            self.cap = mvsdk.CameraGetCapability(self.hCamera)

            #彩色输出
            mvsdk.CameraSetIspOutFormat(self.hCamera, mvsdk.CAMERA_MEDIA_TYPE_MONO8)   #CAMERA_MEDIA_TYPE_MONO8 CAMERA_MEDIA_TYPE_BGR8

            # 相机模式切换成连续采集
            mvsdk.CameraSetTriggerMode(self.hCamera, 0)

            # 手动曝光，曝光时间30ms
            mvsdk.CameraSetAeState(self.hCamera, 0)
            mvsdk.CameraSetExposureTime(self.hCamera, 5 * 1000)
            
            # 让SDK内部取图线程开始工作
            mvsdk.CameraPlay(self.hCamera)

            # # 计算RGB buffer所需的大小，这里直接按照相机的最大分辨率来分配
            self.FrameBufferSize = self.cap.sResolutionRange.iWidthMax * self.cap.sResolutionRange.iHeightMax * 3
            # 分配RGB buffer，用来存放ISP输出的图像
            # 备注：从相机传输到PC端的是RAW数据，在PC端通过软件ISP转为RGB数据（如果是黑白相机就不需要转换格式，但是ISP还有其它处理，所以也需要分配这个buffer）
            self.pFrameBuffer = mvsdk.CameraAlignMalloc(self.FrameBufferSize, 16)
        
    
    def get_observation(self):
        # Get the position and orientation of the car in the simulation
        # pos, ang = p.getBasePositionAndOrientation(self.goal, self.client)
        # pos = pos[:1]
        # # Get the velocity of the car
        # #vel = p.getBaseVelocity(self.goal, self.client)[0][0:2]

        # # Concatenate position, orientation, velocity
        # observation = pos #+ ori + vel)
        
        #get one image frame from Sua134gc
        try:
            pRawData, FrameHead = mvsdk.CameraGetImageBuffer(self.hCamera, 200)
            mvsdk.CameraImageProcess(self.hCamera, pRawData, self.pFrameBuffer, FrameHead)
            mvsdk.CameraReleaseImageBuffer(self.hCamera, pRawData)

            frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(self.pFrameBuffer)
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth, 1 if FrameHead.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3) )

        except mvsdk.CameraException as e:
            if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
                print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message) )
        #calc obj from the image get the bonding box
        #retrun the bonding box
        
        frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_LINEAR)
        retval, image_highlight_bin = cv2.threshold(frame,100,255,cv2.THRESH_BINARY)
        image_highlight_bin_moment = cv2.moments(image_highlight_bin)
        m00 = image_highlight_bin_moment['m00']
        m10 = image_highlight_bin_moment['m10']
        m01 = image_highlight_bin_moment['m01']
        image_highlight_bin_x = 320
        image_highlight_bin_y = 240
        if m00>0:
            image_highlight_bin_x = int(m10/m00)
            image_highlight_bin_y = int(m01/m00)
        cv2.circle(frame,(image_highlight_bin_x,image_highlight_bin_y),50,(255,255,255),2,8)
        cv2.imshow("Press q to end", frame)
        cv2.waitKey(1)
        observation = 1
        return observation
