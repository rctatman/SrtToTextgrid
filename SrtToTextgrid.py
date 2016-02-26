# this Python script takes a .srt file (common sub title formant) and converts it to a Praat .textgrid file
# it's general enough that it *may* work on other types of files like .sub, .sbv, but please be cautious 
#
# written by Rachael Tatman, please rctatman@uw.edu with any problems

# import
import datetime
import re
import numpy
import string
from string import digits

# it would be nice to ask user for file name and name for converted file from command line
inputFile = "keynote-katie-bell-how-python-works-as-a-teaching-language_en.srt" # put the name of the file you'd like converted here
outputFile = "output_katie.textgrid" # put what you'd like your output file to be called here

# open .srt file
file = open(inputFile, 'rw')
with open(inputFile, 'r') as f:
	read_data = f.read().replace('\n', ' ')
	read_data += "0" #add a numeric character at the end for our regex to work

# create (or overwrite) new file for our output
file1 = open(outputFile,'w')

# first, though, we need to find out how long our file is in miliseconds,  
pattern = re.compile("[0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]") # look for time-like things (09:08:00)
listOfTimes = [] 

# grab all the times in the file
for i, line in enumerate(file):
    for match in re.findall(pattern, line):
	listOfTimes.append(match)

# strip the date information from them
mydates = [ datetime.datetime.strptime(listOfTimes[x], "%H:%M:%S").time() for x in range(len(listOfTimes)) ]
# convert minutes/seconds to only seconds 
seconds = numpy.array([x.second for x in mydates])
minutes = numpy.array([x.minute for x in mydates]) * 60
times = seconds + minutes # this is a list of all times in seconds 
numberOfIntervals = times.size/2

#ok, now that we have a list of times, we can figure out the max time and start by creating the preamble for our .textgrid
maxTime = max(times)

# now let's extract the text
# will this split when someone says a number, too?
pattern2 = re.compile("\:\d\d([a-zA-Z\d\'.,%\&;/\$# ]+)[\d\s]*") # this matches any alphabetic characters, white spaces and assorted puncutuation between numeric characters 
text = [] 

for match in re.findall(pattern2, read_data): # find all text between numeric characters
	text.append(match)

text = [x.rstrip('1234567890 ') for x in text] #get rid of extra numbers at end of line
text = [x.strip(' ') for x in text] #strip extra white spaces
text = [x for x in text if x]  # remove empty items

# write textgrid preamble
file1.write("File type = \"ooTextFile\"" + '\n')
file1.write("Object class = \"TextGrid\""+ '\n')
file1.write('\n')
file1.write("xmin = 0"+ '\n')
file1.write("xmax = " + str(maxTime)+ '\n') 
file1.write("tiers? <exists>"+ '\n')
file1.write("size = 1"+ '\n')
file1.write("item []: "+ '\n')
file1.write("    item [1]:"+ '\n')
file1.write("        class = \"IntervalTier\""+ '\n')
file1.write("        name = \"silences\""+ '\n')
file1.write("        xmin = 0"+ '\n')
file1.write("        xmax = " + str(maxTime)+ '\n')
file1.write("        intervals: size = " + str(numberOfIntervals) +'\n') 


# create intervals, transfer text into appropriate interval
for i in range(1,numberOfIntervals + 1): # I know it's weird, but I was getting fenceposting errors

	file1.write("  intervals [" + str(i) + "]:" + "\n")
	file1.write("            xmin = " + str(times.item((i * 2) - 2)) + "\n") # get the ith element from the array
	file1.write("            xmax = " + str(times.item((i * 2 ) - 1)) + "\n") # ith element + 1
	file1.write("            text = \"" + text[i - 1] + "\"\n") 

# close our files and tidy up
file.close()
file1.close()
