# this Python script takes a .srt file (common sub title formant) and converts it to a Praat .textgrid file
# it *may* work on other types of files, but please be cautious 
#
# written by Rachael Tatman, please rctatman@uw.edu with any problems

# import
import datetime
import re
import numpy

# open .srt file
file = open('ccSubs_com_jessica-mckellar-keynote-pycon-2014_en.srt', 'rw')

# create (or overwrite) new file for our output
file1 = open('subs.textgrid','w')

# first, though, we need to find out how long our file is in miliseconds,  
pattern = re.compile("[0-9]*\:[0-9]*\:[0-9]*") # look for time-like things (09:08:00)
listOfTimes = [] 

# grab all the times in the file
for i, line in enumerate(open('ccSubs_com_jessica-mckellar-keynote-pycon-2014_en.srt')):
    for match in re.findall(pattern, line):
	listOfTimes.append(match)

# strip the date information from them
mydates = [ datetime.datetime.strptime(listOfTimes[x], "%H:%M:%S").time() for x in range(len(listOfTimes)) ]
# convert minutes/seconds to only seconds 
seconds = numpy.array([x.second for x in mydates])
minutes = numpy.array([x.minute for x in mydates]) * 60
times = seconds + minutes # this is a list of all times in seconds 

#ok, now that we have a list of times, we can figure out the max time and start by creating the preamble for our .textgrid
maxTime = max(times)

# to do tomorrow:
 
# write textgrid preamble
# create intervals
# transfer text into appropriate interval (the biggest problem here will be that there are a varying number of lines)

 

#for line in file:

file.close()
file1.close()
