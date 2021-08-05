from rl_tracking.resources.robotisAX12A import robotisAX12A
import time

class test_robotisAX12A():
    def __init__(self):
        self.hcamera = 0
    
    def reset(self):
        self.servo = robotisAX12A()

if __name__ == "__main__":
    test = test_robotisAX12A()
    test.reset()
    while 1:
        test.servo.get_observation()
        test.servo.apply_action([512,512])
        time.sleep(2)