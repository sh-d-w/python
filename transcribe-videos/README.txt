# This is a transcribe.py python script found with Google's Gemini
# that uses a downloaded vosk model unzipped as model/ in the same
# directory.

# To use it run transcript.py on an audio.mp3 audio file extracted
# from your video you'd like to dub.
# (It will generate the output.srt) output file for you.

# You can edit that .srt file if you encounter any spelling errors.

# to stitch it back we use the following ffmpeg command:
  # to soft embed it:
  ffmpeg -i input.mp4 -i output.srt -c copy -c:s mov_text output-soft.mp4

  # to hard burn it:
  ffmpeg -i input.mp4 -vf "subtitles=output.srt" output-hard.mp4

# extra information:
  # to extract audio from your video:
  ffmpeg -i input.webm -vn -c:a libmp3lame -q:a 2 output.mp3

  # to download the vosk models:
  goto: https://alphacephei.com/vosk/models

# improvements:
  # We could perhaps wget or curl -OL auto download a model for you.
