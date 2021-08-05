import cv2 as cv
import screeninfo
import numpy as np

class projectortarget():
    def __init__(self):
        print('initing projectortarget ')
    
    def reset(self):
        if 'screen' in locals().keys():
            print('screen exist')
        else:
            self.wndname = "projectortarget"
            self.window_name = self.wndname
            screen_id= 0
            self.screen= screeninfo.get_monitors()[screen_id]
            self.width, self.height = self.screen.width, self.screen.height  # 1000, 700 
            cv.namedWindow(self.window_name, cv.WND_PROP_FULLSCREEN)
            cv.moveWindow(self.window_name, self.screen.x- 1, self.screen.y- 1)
            cv.setWindowProperty(self.window_name, cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
            self.image = np.zeros((self.height, self.width, 3), dtype = np.uint8)

    
    def apply_target_pos(self,pos):
        self.image = np.zeros((self.height, self.width, 3), dtype = np.uint8)
        cv.circle(self.image,(pos[0],pos[1]),10,(255,255,255),-1,8)
        cv.imshow(self.wndname,self.image)
        cv.waitKey(1)