# SrtToTextgrid
Python script to convert .srt subtitle files to Praat .textgrid files. It's general enough that it *may* work on other types of files like .sub or .sbv, but please be cautious.

This was originally written in Python 2.7.3, but it also works in Python 3. 

Example file is a .srt file based on a Youtube transcription of Katie Bell's keynote at a 2015 meeting of the New Zealand Python User Group. Url: https://www.youtube.com/watch?v=dj9RR4BSqvM It's almost an hour, so the audio is really too big to upload. 

# Usage

Before you run the main SRT-to-TextGrid converter, you may need to clean up the SRT file. Sometimes the SRT may not have dedicated intervals for silences. Praat needs those to be explicit.  The example SRT file `input-SRT-file.srt`  has this problem. To create those silent intervals, run the following command:

`python3 SilentIntervalSRT.py $input-SRT-file.srt $output-SRT-file.srt`

Replace the variables $input-SRT-file.srt` and `$output-SRT-file.srt` with your files. 

You can then run the main script that will convert the SRT into a TextGrid. Try experimenting with either the original SRT or the cleaned up SRT:

`python3 SrtToTextgrid.py $output-SRT-file.srt $output-TextGrid-file.TextGrid`

`python3 SrtToTextgrid.py $input-SRT-file.srt $output-TextGrid-file.TextGrid`

Replace the variables $input-SRT-file.srt`, `$output-SRT-file.srt`, and $output-TextGrid-file.TextGrid` with your files. 


Note: The older version of `SrtToTextgrid.py' required no milliseconds in the SRT, like in the SRT file `keynote-katie-bell-how-python-works-as-a-teaching-language_en.srt`. But the current version requires milliseconds in the SRT. This can be fixed in the future.