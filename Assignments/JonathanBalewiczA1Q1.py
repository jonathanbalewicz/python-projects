"""JonathanBalewiczA1Q1
COMP 1012  SECTION A01
INSTRUCTOR Bristow
ASSIGNMENT: A1 Question 1
AUTHOR    Jonathan Balewicz
VERSION   2018-01-24
PURPOSE: Calculate bike speed
"""
import time
import math
mmToM=0.001# mm to metres conversion factor
mToKm=0.001# metres to km conversion factor
kpmToKph=60# kpm to kph conversion factor
mmToIn=0.0393701# mm to inches conversion factor

#asks for the number of teeth on the chainring
chainRingSize=float(input("How many teeth does your chainring have? "))
#asks how many teeth there are on the cog
cogSize=int(input("How many teeth does your cog have? "))
#asks for the diameter of the wheel in mm
wheelSize=float(input("What is the diameter of your wheel (in mm)? "))

#prints the data the user put in
print("\nChainring size: {} teeth".format(chainRingSize))
print("Cog size: {} teeth".format(cogSize))
print("Wheel size: {}mm\n".format(int(wheelSize)))

gearRatio=(chainRingSize)/cogSize#calculates the gear ratio

#calculates the distance covered per wheel turn in metres, from the distance of a wheel turn in mm
wheelTurn=wheelSize*math.pi*mmToM

#calculates the gear development in metres
gearDev=gearRatio*wheelTurn

#calculates the gear inches, from the gear ratio and wheel size in mm
gearInches=gearRatio*wheelSize*mmToIn

#calculates the speed from the gear development in metres and the gear ratio in kph at 90 rpm
speed=90*gearDev*kpmToKph*mToKm

#prints the gear ratio, wheel turn distance, gear development, and gear inches in 4 decimal places
print("Gear ratio: {0:.4f}".format(gearRatio))
print("Distance covered per wheel turn: {0:.4f}m".format(wheelTurn))
print("Gear development: {0:.4f}m".format(gearDev))
print("Gear inches: {0:.4f}in".format(gearInches))

#prints the speed in kph to 2 decimal places
print("At 90rpm, you'd be traveling {0:.2f}km/h".format(speed))

print("\nProgrammed by the Jonathan Balewicz")
print("Date: "+time.ctime())
print("End of processing")