# Given an SRT, find any unmarked silent intervals and add them to the SRT
# It also does some other preprocessing steps:
#     * cleaning up quotation symbols because those cause trouble for Praat
#     * remove consecutive blank lines
#     * make the interval numbers incremently increase from 1
# Made by Hossep Dolatian (github.com/jhdeov/)

import codecs
import sys
import re

# Input and output files as arguments
inFile= sys.argv[1] # "srtInput.srt"
outFile = sys.argv[2] # "srtOutput.srt"

print("Useful debugging info is printed into the message.log")
# The printing code was taken from https://stackoverflow.com/a/2513511
old_stdout = sys.stdout
log_file = open("message.log","w")
sys.stdout = log_file



# define a class for intervals based on the basic template for an SRT interval
class srtInterval:
    def __init__(self,number,range,content):
        self.number= number[:]
        self.range = range[:]
        self.startTime, self.endTime = range[:].split(" --> ")

        # If the content of the SRT has a quotation symbol ", then that is changed to ""
        # This is because Praat TextGrids are sensitive to such symbols
        self.content= content.replace('"', '""')
    def __str__(self):
        return "index: "+str(self.number) + "\ntimes: " + str(self.range) +"\ncontent: " + self.content

# creates an interval between two pre-existing SRT intervals
def createMissingInterval(currentInterval,nextInterval):
    newNumber= currentInterval.number + ".5"
    newRange = currentInterval.endTime + " --> " + nextInterval.startTime
    newContent = "[Silence]"
    newInterval = srtInterval(newNumber,newRange,newContent)
    return newInterval

# updates the number indexes the SRT intervals in the list. This is needed if we had to insert an interval
# note that the list is forced to start with an index 1. I don't know if this is bad
def updateIntervals(srtintervals):
    for i in range(len(srtintervals)):
        srtintervals[i].number= str(i+1)
    return srtintervals
# create a silent interval at the beginning of the file, if needed
def createInitialSilence(endTime):
    newRange = "00:00:00,000 --> " + endTime
    newInterval = srtInterval("0", newRange, "[Silence]")
    return newInterval

# with codecs.open(inFile, 'r', 'utf-8') as i:
#     with codecs.open(outFile, 'w', 'utf-8') as o:


##################################
# Will now read the SRT input file and start to cleanup

# this boolean will be used to check if we had to insert silence intervals
insertedSilences= False

srtintervals = []

# First we read the file and turn it into a list of SRTs
with codecs.open(inFile, 'r', 'utf-8') as iFile:
    lines = iFile.read().splitlines()
    # the input file must end in an empty new line. we add it in case it's absent
    if lines[-1] is not "":
        lines.append("")

    # Will remove any consecutive blank lines, if present
    linesTemp = []
    for i in range(len(lines) - 1):
        if lines[i] == '' and lines[i + 1] == '':
            print(f'There was a blank line at index {i} before another blank line. It was removed ')
        else:
            linesTemp.append(lines[i])
    linesTemp.append(lines[-1])
    lines = linesTemp

    lines[0] = lines[0].replace('\ufeff', "")
    lineCounter = 0
    while lineCounter < len(lines):
        print(f"Currently working on line number {lineCounter} with content {lines[lineCounter]}")
        tempIndex = lines[lineCounter]
        lineCounter+=1
        tempTime = lines[lineCounter]
        lineCounter += 1
        tempContent = lines[lineCounter]
        lineCounter += 1
        print("\tCurrently on line ",lines[lineCounter])
        seeNewLine= len(lines[lineCounter])<1
        print("\tLength of this line: ", len(lines[lineCounter]))
        print("\tIs the line empty?: ",seeNewLine)
        while not seeNewLine:
            tempContent = tempContent + "\n" + lines[lineCounter]
            print("\tContent of the current line:", tempContent)
            lineCounter += 1
            print("\tLineCounter:",lineCounter)
            seeNewLine= len(lines[lineCounter])<1
        lineCounter += 1

        currentInterval = srtInterval(tempIndex,tempTime,tempContent)
        print("Created the following interval",currentInterval)
        srtintervals.append(currentInterval)
        print("The list currently has the following intervals:")
        for i in srtintervals:
            print(i)

        print("Done with creating the list")

print("")

# Now we clean up the file by adding silences
# Because the list of intervals will grow as we add silences, we have to continously
# check the list length
strIntervalsCounter = 0
while strIntervalsCounter < len(srtintervals)-1:
    i = strIntervalsCounter
    currentInterval = srtintervals[i]
    nextInterval = srtintervals[i+1]
    if currentInterval.endTime == nextInterval.startTime:
        print("There is no missing interval between the following two intervals")
        print(currentInterval)
        print(nextInterval)
    else:
        insertedSilences = True
        print("There is a missing interval between the following two intervals")
        print(currentInterval)
        print(nextInterval)
        newInterval = createMissingInterval(currentInterval,nextInterval)
        print("We created a silence new interval")
        print(newInterval)
        srtintervals.insert(i+1, newInterval)

    strIntervalsCounter+= 1

print("")

print("The list currently:")
for i in srtintervals:
    print(i)

print("")

# check if need to add an initial silence
print("Check if need to add initial silence")
needInitialSilence= False
if srtintervals[0].startTime is not "00:00:00,000":
    print("There is a missing initial silence:",srtintervals[0].startTime)
    newInterval = createInitialSilence(srtintervals[0].startTime)
    print("here's new interval")
    print(newInterval)
    srtintervals.insert(0, newInterval)
else:
    print("There is no missing initial silence:",srtintervals[0].startTime)

print("")

print("The list currently:")
for i in srtintervals:
    print(i)

# updates the interval indexes in the list, if needed
print("We will update the list with new indexes")
srtintervals = updateIntervals(srtintervals)

print("")

print("The list currently:")
for i in srtintervals:
    print(i)

with codecs.open(outFile, 'w', 'utf-8') as o:
    for line in srtintervals:
        o.writelines(line.number + '\n')
        o.writelines(line.range + '\n')
        o.writelines(line.content + '\n\n')


sys.stdout = old_stdout
log_file.close()