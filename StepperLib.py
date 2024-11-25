"""
StepperLib.py

Driver for 28BYJ-48 stepper motor

At the end of a move the stepper coils are turned off - the gears will hold
the stepper position

Taken from micropython driver.
Modified for RasPi. Tested on RasPi4.

Author: Brian N Norman 23/11/24
"""
from gpiozero import OutputDevice # works on PI4

import time

######################################################
#
# configuration
#
HighTorque=3 # uses double phases
LowTorque=2  # uses single phase
HalfStep=1   # uses a mixture of double and single phase. Presumably gives a smoother rotation

StepDwell=0.0019 # empirically determined gives highest speed
StepsPerRevolution=2048
#
#######################################################



FORWARD = 1
REVERSE = -1

SINGLE_PHASES = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]  # low torque
DOUBLE_PHASES = [[1, 0, 0, 1], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]  # higher torque
# this doesn't, visually,appear different to other phases
HALF_STEP=[[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1]]

class Stepper():

    def __init__(self, Mode,PIN_IN1, PIN_IN2, PIN_IN3, PIN_IN4):

        self.IN1 = OutputDevice(PIN_IN1)
        self.IN2 = OutputDevice(PIN_IN2)
        self.IN3 = OutputDevice(PIN_IN3)
        self.IN4 = OutputDevice(PIN_IN4)

        self.controlPins = [self.IN1, self.IN2, self.IN3, self.IN4]

        self.lastPhase = 0
        self.stepDwell=StepDwell # default

        if Mode == HighTorque:
            self.PHASES = DOUBLE_PHASES  # set to DOUBLE_PHASES for more torque
        elif Mode == LowTorque:
            self.PHASES = SINGLE_PHASES
        elif Mode == HalfStep:
            self.PHASES = HALF_STEP
        else:
            raise("Invalid mode selected")
        self.LEN_PHASES=len(self.PHASES)

    def __del__(self):
        try:
            self.stop() # turn off motor coils
        except Exception as e:
            print("exception in __del__",e)
        
    def setSpeed(self,percent=100):
        # set the speed to % of max
        # non-linear
		
        if percent==0:
            return self.stop()

		percent=min(100,percent)
		
        self.stepDwell=StepDwell*100/percent
        
        
    def stepWait(self):
        # used to delay steps to compensate for HDW
        # sluggishness
        # avoids using 'pass' which would create a very tight loop
        # using a lot of cpu time.
        start=time.time()
        now=start
        while now<(start+self.stepDwell):
            now=time.time() # use rather than pass
            
            
    def setPins(self, pin_values):
        # pin_values is a list of 4 values
        #print(f"Stepper.setPins {pin_values}")
        for this_pin in range(len(self.controlPins)):
            self.controlPins[this_pin].value=pin_values[this_pin]

    def oneStep(self, direction=FORWARD):
        #print(f"lastPhase {self.lastPhase}")
        if direction == FORWARD:

            self.setPins(self.PHASES[self.lastPhase])  #
            self.lastPhase=(self.lastPhase+1) % self.LEN_PHASES
        else:
            self.setPins(self.PHASES[self.lastPhase])  #
            self.lastPhase=(self.lastPhase-1) % self.LEN_PHASES

        self.stepWait() # wait for motors to stop moving

    def stepN(self,N):
        # step the motor N steps
        #print("type N",type(N),int(N))
		if N<0:
			direction=REVERSE
		else direction=FORWARD
		
        for step in range(abs(int(N))):
            self.oneStep(direction)
            
    def stepAng(self,ang):
        # turn the motor by given angle
        # a negative angle sets the direction to REVERSE
        if ang<0:
            direction=REVERSE
            ang=abs(ang)
        else:
            direction=FORWARD
        self.stepN(int(ang*StepsPerRevolution/360),direction)
        self.stop()

    def stop(self):
        # turn off the coils - the 28BYJ-48 has a gearbox
        # so will cool down and not move
        self.setPins([0, 0, 0, 0])

if __name__=="__main__":
    # quick test
    s=Stepper(HighTorque,2,3,4,17)

    print("Clockwise 100%")
    s.stepAng(180)

    
    print("Anti-clockwise 100%")
    s.stepAng(-180)

    
    print("Clockwise 25%")
    s.setSpeed(25)
    s.stepAng(360)
 
    
    
    
    
    
