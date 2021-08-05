import os
import mvsdk
import numpy as np

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

class robotisAX12A():
    def __init__(self):
        print('robotis AX12A serial initing')
        # Control table address
        self.ADDR_AX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model  64
        self.ADDR_AX_GOAL_POSITION      = 30     # 116
        self.ADDR_AX_PRESENT_POSITION   = 36  #  132
        self.ADDR_AX_MOVING_SPEED = 32

        # Protocol version
        self.PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel
        # Default setting
        self.DXL_ID                      = 2                 # Dynamixel ID : 1
        self.BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
        self.DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller 

        self.TORQUE_ENABLE               = 1                 # Value for enabling the torque
        self.TORQUE_DISABLE              = 0                 # Value for disabling the torque
        self.DXL_MINIMUM_POSITION_VALUE  = 400           # Dynamixel will rotate between this value
        self.DXL_MAXIMUM_POSITION_VALUE  = 600            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
        self.DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold 

        if 'portHandler' in locals().keys():
            print('portHandler exist')
        else:
            self.portHandler = PortHandler(self.DEVICENAME)
            # Open port
            if self.portHandler.openPort():
                print("Succeeded to open the AX-12A serial port")
            else:
                print("Failed to open the AX-12A serial port")
            # Set port baudrate
            if self.portHandler.setBaudRate(self.BAUDRATE):
                print("Succeeded to change the baudrate")
            else:
                print("Failed to change the baudrate")

        if 'packetHandler' in locals().keys():
            print('packetHandler exist')
        else:
            self.packetHandler = PacketHandler(self.PROTOCOL_VERSION)

    
    def get_observation(self):
        print('AX-12A reading')
        # Read present position
        self.DXL_ID = 1
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_AX_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        # print("[ID:%03d]  PresPos:%03d" % (self.DXL_ID, dxl_present_position))
        observation = [dxl_present_position]

        self.DXL_ID =2
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_AX_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        # clprint("[ID:%03d]  PresPos:%03d" % (self.DXL_ID, dxl_present_position))
        observation.append(dxl_present_position)

        return observation

    def apply_action(self, action):
        print('apply action to AX-12A')
        # Write goal position
        self.DXL_ID =1
        gola_position= action[0]
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_AX_GOAL_POSITION, gola_position)   #dxl_goal_position[index]
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        
        self.DXL_ID =2
        gola_position= action[1]
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_AX_GOAL_POSITION, gola_position)   #dxl_goal_position[index]
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))