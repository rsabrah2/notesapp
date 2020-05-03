# This file contains all the functions created for the Notes app
from datetime import datetime
import glob
import shutil
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
        # print("Combining file %s" % filename)
        shutil.copyfileobj(open(filename, 'rb'), output)

    #print("Done combining files. See the final version in %s" % output_file)
    #print("Done! See the final version in %s" % output_file)
    output.close()


# This functions removes the individual .wav files created by the gTTS call in each node after combining them
def remove_audio(size):
    filepath = "/mnt/Audiofiles/audiofiles/"
    for i in range(size):
        filename = filepath + "voice" + str(i) + ".wav"
        #print("Removing file %s" % filename)
        os.remove(filename)
    print("Done!")


# This function displays the total time in a user friendly way
def total_time(totalsec):
    t_hr = totalsec // 3600
    t_min = (totalsec % 3600) // 60
    t_sec = (totalsec % 3600) % 60
    print("Total time to run the code is %02d:%02d:%09.6f" % (t_hr, t_min, t_sec))
