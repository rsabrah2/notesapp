# This file contains all the functions created for the Notes app

import glob    # Needed for combining the various .wav files
import shutil   # Needed for combining the various .wav files
import os


# This functions combines the individual .wav file created by the gTTS call in each node to  single notes File
def combineaudio(combinedname):
    dirPath = "/mnt/Audiofiles/audiofiles/"
    output_file = dirPath + "combined/" + combinedname
    output = open(output_file, 'wb')
    filenames = glob.glob(dirPath + "*.wav")
    numberoffiles = len(filenames)

    for i in range(numberoffiles):
        filename = dirPath + "voice" + str(i) + ".wav"
        shutil.copyfileobj(open(filename, 'rb'), output) #combines individual wavefiles


    output.close()


# This functions removes the individual .wav files created by the gTTS call in each node after combining them
def remove_audio(size):
    filepath = "/mnt/Audiofiles/audiofiles/"
    for i in range(size):
        filename = filepath + "voice" + str(i) + ".wav"
        os.remove(filename)
    print("Done!")


# This function displays the total time in a user friendly way
def total_time(totalsec):
    t_hr = totalsec // 3600
    t_min = (totalsec % 3600) // 60
    t_sec = (totalsec % 3600) % 60
    return t_hr, t_min, t_sec

