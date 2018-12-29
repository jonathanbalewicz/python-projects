"""JonathanBalewiczA2Q1
COMP 1012  SECTION A01
INSTRUCTOR Bristow
ASSIGNMENT: A3 Question 1
AUTHOR    Jonathan Balewicz
VERSION   2018-02-24
PURPOSE: Simulate the Monty Hall Problem and report statistics
"""

import random
random.seed(10122018)

# counter in this form:
# [switch wins, switch loses, stay wins, stay loses]
count=[0,0,0,0]
door_set={1,2,3}
sim_data=[] #   stores the dictionaries of data of each simulation

trialNumber=input("Let's Make a Deal! (seed=10122018)\nHow many trials should I run? ")
while trialNumber.isnumeric()==False or int(trialNumber) <= 0:
    trialNumber=input('"{}" is not a number, please enter a number '.format(trialNumber))

for _ in range(int(trialNumber)):
    prize={random.randrange(1,4)}
    choice={random.randrange(1,4)}
    remaining=door_set.difference(prize,choice)
    reveal=random.choice([remaining]) # reveals a door that wasn't chosen and doesn't have a prize
    SwitchedDoor=door_set.difference(reveal,choice)
    switch=random.choice([0,1]) # switch = 0 to switch or 1 to not
    
    if SwitchedDoor==prize:#creates a dictionary to dicide if the contestant won in the form win[switch]
        win={0:True,1:False}
    else:
        win={1:True,0:False}
        
    #increment the count list
    if win[switch]==True and switch==0:
        count[0]+=1
    elif win[switch]==True and switch==1:
        count[2]+=1
    elif win[switch]==False and switch==0:
        count[1]+=1
    else:
        count[3]+=1
   
    sim_data.append({"switched":switch, "win":win[switch], "revealed_door":reveal, "choice":choice, "prize":prize})
    
print("Switch wins: {}, Stay wins: {}\nSwitch loses: {}, Stay loses: {}".format(count[0],count[2],count[1],count[3]))

if count[2]+count[3] == 0:
    stayWins=0.0
else:
    stayWins=count[2]*100/(count[2]+count[3])
print("Stay wins {:.2f}% of the time".format(stayWins))
if count[1]+count[0] == 0:
    switchWins=0.0
else:
    switchWins=count[0]*100/(count[1]+count[0])
print("Switch wins {:.2f}% of the time".format(switchWins))

while True:
    trial=input("There are {} simulations, which one would you like to see? (or q to quit) ".format(trialNumber))
    if trial=="q":
        break
    elif trial.isnumeric() and int(trial) < int(trialNumber):
        switched=not bool(sim_data[int(trial)]["switched"])
        print("Simulation {}".format(trial))
        print("\tSelected door: {}".format(list(sim_data[int(trial)]["choice"])[0]))
        print("\tWinning door:  {}".format(list(sim_data[int(trial)]["prize"])[0]))
        print("\tRevealed door: {}".format(list(sim_data[int(trial)]["revealed_door"])[0]))
        print("\tSwitched?      {}".format(switched))
        print("\tWin?           {}".format(sim_data[int(trial)]["win"]))
    elif not trial.isnumeric():
        print('"{}" is not a number.'.format(trial))
    else:
        print('"{}" is too large, there are only {} simulations'.format(trial,trialNumber))
        
import time
print("\nProgrammed by the Jonathan Balewicz")
print("Date: "+time.ctime())
print("End of processing")

