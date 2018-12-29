"""JonathanBalewiczA2Q1
COMP 1012  SECTION A01
INSTRUCTOR Bristow
ASSIGNMENT: A2 Question 1
AUTHOR    Jonathan Balewicz
VERSION   2018-02-03
PURPOSE: Calculate statistics of passwords and find the most common passwords in a file
"""


import math
file=input("Enter the name of the password file: ")
print("Password complexity")
h=-1
passwords=[]
usernames=[]
Entropy=[]
lpasswords=[]
rows=open(file, encoding="utf-8")
passdict={}
passcount={}

for row in rows:
    h+=1#h keeps track of the iteration number
    Entropy.append(0.0) #appends a 0 that will be changed later
    columns0=row.split(":")#create an array [username,password]
    columns=[columns0[0], columns0[1].replace("\n","")]# This second array gets rid of the \n
    if columns[1] in passwords:
        passdict[columns[1]].append(columns[0])#passdict is the dict of usernames from password keys
        passcount[columns[1]]+=1#passdict is the dict of the number of times a password key has been used
    else:
        passdict[columns[1]]=[columns[0]]#create dict if none exists
        passcount[columns[1]]=1
    passwords.append(columns[1])# the password gets appended to the password list
    lpasswords.append(columns[1].lower())#make the password lowercase
    usernames.append(columns[0]) # the username gets appended to the username list   
    for letter in lpasswords[h]:
        probability = lpasswords[h].count(letter) / len(lpasswords[h])
        Entropy[h]+=-(probability*(math.log((probability),2))) # each letter of the password gets added for each iteration

entries=0
sum1=0
sum2=0

#find the sum of the entropies
for number in Entropy:
    sum1+=float(number)
    entries+=1

# find and print the average, minimum, and maximum entropy
average=sum1/entries
maximum=max(Entropy)
minimum=min(Entropy)
print("\tAverage:   {:.4f} bits".format(average))
print("\tMinimum:   {:.4f} bits".format(minimum))
print("\tMaximum:   {:.4f} bits".format(maximum))

#find and print the standard deviation
for number in Entropy:
    sum2+=(float(number)-average)**2 # sum2 is the numerator under the root in the std dev calculation
stddev=math.sqrt(sum2/(entries-1))
print("\tStd Dev:   {:.4f}".format(stddev))

num=[]
leastUsed=""
mostUsed=""

for password in passwords:
    num.append(passcount[password])#appends the number of users using the password to the list
    #if the password is the most used so far
    if passcount[password] == max(num):
        mostUsed=password
    #similar method for least used password
    if passcount[password] == min(num):
        leastUsed=password

i=0
j=0
print("\tMost common: {} is used by these users:".format(mostUsed))
for users in passdict[mostUsed]:
    print("\t\t{}".format(users))
    i+=1
    if i==10:
        break
    

print("\n\tLeast common: {} is used by these users:".format(leastUsed))
for leastUsers in passdict[leastUsed]:
    print("\t\t{}".format(leastUsers))
    j+=1
    if j==10:
        break
    
import time
print("\nProgrammed by the Jonathan Balewicz")
print("Date: "+time.ctime())
print("End of processing")
















