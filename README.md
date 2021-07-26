# rl_tracking
This is a Gym like env for rl vision tracking.
Using two servos as a tracking platform.
A camera serve as a tracking sensor.
rl will try to control servos to tracking obj movement ,
try its best to keep obj in the center of  camera's view.

try to use i51080ti to edit readme

here are things to do :

1. capture image from  MV-SUA134GC-T and calculate a obj center box using opencv or halcon
2. drive robotis servo in speed mode, setting its bundary
3. use projector to produce obj to be tracked
4. train a agent 
