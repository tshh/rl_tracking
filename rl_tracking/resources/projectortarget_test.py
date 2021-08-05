from rl_tracking.resources.projectortarget import projectortarget
import time

class projectortargettest():
    def __init__(self):
        print('projectortargettest init')
    
    def reset(self):
        self.target = projectortarget()
    
if __name__ == "__main__":
    test = projectortargettest()
    test.reset()
    test.target.reset()
    x=600   #600
    y=550   #550

    while 1:
        #x=x+10
        test.target.apply_target_pos([x,y])
        time.sleep(1)