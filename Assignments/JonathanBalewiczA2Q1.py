"""JonathanBalewiczA2Q1
COMP 1012  SECTION A01
INSTRUCTOR Bristow
ASSIGNMENT: A2 Question 1
AUTHOR    Jonathan Balewicz
VERSION   2018-02-03
PURPOSE: Calculate Statistics of the average dietary energy supply adequacy percentage
"""
mean=0
entries=0
print("Summarizing <foodData.csv>")
file=open("foodData.csv")
headers=file.readline()
rows=file.readlines()

numbers2015=[]
numbers2008=[]
numbers2000=[]

for row in rows:
    columns=row.split(",")
    if (columns[0]!="" and columns[1]!="" and columns[2]!=""):#any rows with incomplete data are excluded
        num2015=float(columns[0]) #temporary placeholders for row values
        num2008=float(columns[1])
        try: #prevents error in the case that the third row cannot be a float
            num2000=float(columns[2])
            numbers2000.append(num2000)
        except ValueError:
            c=0 #do nothing on error
        numbers2015.append(num2015) #numbers2015 is the list of numbers in 2015
        numbers2008.append(num2008)
        entries+=1 # increment the number of entries

sum2000=0
sum2008=0
sum2015=0

# adds up the numbers
for num in numbers2000:
    sum2000+=num
for num in numbers2008:
    sum2008+=num
for num in numbers2015:
    sum2015+=num
    
#mean calculation
mean2000=sum2000/entries
mean2008=sum2008/entries
mean2015=sum2015/entries

#sorts the numbers
numbers2000=sorted(numbers2000)
numbers2008=sorted(numbers2008)
numbers2015=sorted(numbers2015)


if entries%2==0:#checks if the number of entries is even
    middle1=int((entries)/2-0.5)#finds the lower middle entry
    middle2=int((entries)/2+0.5)#finds the upper middle entry
    median2000=(numbers2000[middle1]+numbers2000[middle2])/2 #calculates the median
    median2008=(numbers2008[middle1]+numbers2008[middle2])/2
    median2015=(numbers2015[middle1]+numbers2015[middle2])/2
else: #if the number of entries is odd, the middle value is used
    middle=int((entries-1)/2)
    median2000=numbers2000[middle]
    median2008=numbers2008[middle]
    median2015=numbers2015[middle]

#calculates the minimum values
min2000=min(numbers2000)
min2008=min(numbers2008)
min2015=min(numbers2015)

#calculates the maximum values
max2000=max(numbers2000)
max2008=max(numbers2008)
max2015=max(numbers2015)

#calculates the range of values
range2000=max2000-min2000
range2008=max2008-min2008
range2015=max2015-min2015

#print the results
print("2000")
print("\tMean: {:.2f}".format(mean2000))
print("\tMedian: {:.2f}".format(median2000))
print("\tMinimum: {}".format(int(min2000)))
print("\tMaximum: {}".format(int(max2000)))
print("\tRange: {}".format(int(range2000)))

print("\n2008")
print("\tMean: {:.2f}".format(mean2008))
print("\tMedian: {:.2f}".format(median2008))
print("\tMinimum: {}".format(int(min2008)))
print("\tMaximum: {}".format(int(max2008)))
print("\tRange: {}".format(int(range2008)))

print("\n2015")
print("\tMean: {:.2f}".format(mean2015))
print("\tMedian: {:.2f}".format(median2015))
print("\tMinimum: {}".format(int(min2015)))
print("\tMaximum: {}".format(int(max2015)))
print("\tRange: {}".format(int(range2015)))

import time

print("\nProgrammed by the Jonathan Balewicz")
print("Date: "+time.ctime())
print("End of processing")