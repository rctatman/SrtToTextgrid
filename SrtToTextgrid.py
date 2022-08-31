# this Python script takes a .srt file (common sub title formant) and converts it to a Praat .textgrid file
# it's general enough that it *may* work on other types of files like .sub, .sbv, but please be cautious 
#
# written by Rachael Tatman, please rctatman@uw.edu with any problems.
# Additional work by Caluã Pataca (github.com/caluap)
# Additional edits by Elise Bell (github.com/elisebell)

# import
import datetime
import re
import numpy
import string
from itertools import groupby
import os
from os import scandir

from string import digits
from collections import namedtuple

# still might be useful to prompt for these at the command line eventually
path = "/Users/elisebell/Github/SrtToTextgrid/" # where the source .srt files are
output_directory = "/Users/elisebell/Github/SrtToTextgrid/" # where you want the output TextGrids to go

# define functions
# read the srt file and extract subtitles and data as a list
def srt_process(res, Subtitle):  
  subs = []

  for sub in res:
      if len(sub) >= 3: # not strictly necessary, but better safe than sorry
          sub = [x.strip() for x in sub]
          number, start_end, *content = sub 
          start, end = start_end.split(' --> ')
          subs.append(Subtitle(number, start, end, content))
  return subs

# extract timing information from list of subtitles
def make_time_list(subs):  
  listOfTimes = []
  
  for s in subs:
    listOfTimes.append(s.start)
    listOfTimes.append(s.end)
    
  # strip the date information from them
  #mydates = [ datetime.datetime.strptime(listOfTimes[x], "%H:%M:%S,%f").time() for x in range(len(listOfTimes)) ]
  
  mydates = []

  for x in range(len(listOfTimes)):
    try:
      mydates.append(datetime.datetime.strptime(listOfTimes[x], "%H:%M:%S,%f").time())
    except ValueError:
      mydates.append(datetime.datetime.strptime(listOfTimes[x], "%H:%M:%S").time()) # get around "ValueError: time data '00:00:00' does not match format '%H:%M:%S,%f'" 

  # convert microseconds/minutes/seconds to only seconds 
  milliseconds = numpy.array([x.microsecond for x in mydates]) / 1000000
  seconds = numpy.array([x.second for x in mydates])
  minutes = numpy.array([x.minute for x in mydates]) * 60
  times = milliseconds + seconds + minutes # this is a list of all times in seconds 
  numberOfIntervals = times.size//2
  
  #ok, now that we have a list of times, we can figure out the max time and start by creating the preamble for our .textgrid
  maxTime = max(times)
  return listOfTimes, times, numberOfIntervals, maxTime

# now let's extract the text
def extract_text(subs):
  text = []
  for s in subs:
    _ = ""
    for t in s.content:
      _ += t + " | "
    _ = _.replace('"','') # remove double quotes that may be misinterpreted by Praat
    text.append(_[:-3]) # some srt files don't seem to have extra characters at the end of the line, so this may not always be necessary
  return text

# write all extracted information to a new TextGrid
def tg_write(text, output_file, listOfTimes, times, numberOfIntervals, maxTime):
  # write textgrid preamble
  output_file.write("File type = \"ooTextFile\"" + '\n')
  output_file.write("Object class = \"TextGrid\""+ '\n')
  output_file.write('\n')
  output_file.write("xmin = 0"+ '\n')
  output_file.write("xmax = " + str(maxTime)+ '\n')
  output_file.write("tiers? <exists>"+ '\n')
  output_file.write("size = 1"+ '\n')
  output_file.write("item []: "+ '\n')
  output_file.write("\t item [1]:"+ '\n')
  output_file.write("\t\t class = \"IntervalTier\""+ '\n')
  output_file.write("\t\t name = \"silences\""+ '\n')
  output_file.write("\t\t xmin = 0"+ '\n')
  output_file.write("\t\t xmax = " + str(maxTime)+ '\n')
  output_file.write("\t\t intervals: size = " + str(numberOfIntervals) +'\n')
  
  # write times and text
  for i in range(1, numberOfIntervals + 1): # I know it's weird, but I was getting fenceposting errors
    output_file.write("\t\t intervals [" + str(i) + "]:" + "\n")
    output_file.write("\t\t\t xmin = " + str(times.item((i * 2) - 2)) + "\n") # get the ith element from the array
    output_file.write("\t\t\t xmax = " + str(times.item((i * 2 ) - 1)) + "\n") # ith element + 1
    output_file.write("\t\t\t text = \"" + text[i - 1] + "\"\n")
  
  # close output file
  output_file.close()

with scandir(path) as it:
    for entry in it:
        if entry.name.endswith('srt') and entry.is_file():
          # run all the things
          with open(entry) as f:
            res = [list(g) for b,g in groupby(f, lambda x: bool(x.strip())) if b]
          
            output_file_path = output_directory + entry.name[:-4]+".TextGrid" # remove .srt extension and add .TextGrid
  
            output_file = open(output_file_path,'w')
            
            # create named tuple Subtitle
            Subtitle = namedtuple('Subtitle', 'number start end content')
  
            # go through res list, splitting out subtitle components. returns a list.
            subs = srt_process(res, Subtitle)
            
            # create and return timing data variables
            listOfTimes, times, numberOfIntervals, maxTime = make_time_list(subs)
            
            # extract text in a format that can be put into a TextGrid
            text = extract_text(subs)
            
            # write the required TextGrid preamble to the output file, and append the data
            tg_write(text, output_file, listOfTimes, times, numberOfIntervals, maxTime)
