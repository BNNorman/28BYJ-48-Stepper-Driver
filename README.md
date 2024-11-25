# 28BYJ-48-Stepper-Driver
RPI Python driver for the 28BYJ-48 stepper motor

Motor coils are turned off at the end of each move to reduce current used.

The 28BYJ-48 has gears which will hold the motor in a given position provided
there isn't too much turning force on the motor (e.g. when holding a weight vertically).

The 28BJY-48 MUST be provided with it's supply voltage independently of the Pi. **I.E. DO NOT POWER THE STEPPER
FROM THE PI 5V** It doesn't appear to affect the Pi but the turning torque is drastically lowered because the Pi can't supply enough current at 5v.

## API ##

from StepperLib import Stepper

### stepper=Stepper(Mode,PIN_IN1, PIN_IN2, PIN_IN3, PIN_IN4) ###

|mode| comment|
|----|------|
|StepperLib.HighTorque| Two coils are always energised |
|StepperLib.LowTorque| only one coil is energised|
|StepperLib.HalfStep | alternates two/one coils energised|

Visually there doesn't appear to be much difference between them so I stick to HighTorque

### setSpeed(percent) ###
Defaults to 100% on startup
if percent is zero the motors are turned off.
percent has a max value of 100

### oneStep(direction) ###
Used internally

### setPins([pin_numbers]) ###
Used internally

### stepN(N) ###
Turns the motor N steps clockwise. Negative values turn it anti-clockwise

### stepAng(angle) ###
Turns the motor clockwise through the given angle. A negative angle will turn anti-clockwise

### stop() ###
Used internally. Turns off all the coils to reduce the current used. 



## Example from StepperLib.py ###

```
	import StepperLib
    s=Stepper(HighTorque,2,3,4,17)

    print("Clockwise 100%")
    s.stepAng(180)

    print("Anti-clockwise 100%")
    s.stepAng(-180)

    
    print("Clockwise 25%")
    s.setSpeed(25)
    s.stepAng(360)

    
```

