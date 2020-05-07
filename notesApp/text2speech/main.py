# To call mpirun -n [nprocs] python3 main.py [notesfilename] [combinedfilename]
#
#
from django.conf import settings
import sys
from gtts import gTTS
from mpi4py import MPI
# Ignore the error
from functions import  combineaudio, remove_audio, total_time
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


# ----------------------------------------------Functions--------------------------------------------

# ----------------------------------------------Functions--------------------------------------------

if __name__ == "__main__":
    t_start = MPI.Wtime()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    notestxt = str(sys.argv[1])  #file name of the uploaded text file
    filename = str(sys.argv[2])  # filename for the combined wave fie

    separator = ""
    if rank == 0:
        """
        In the root node, each text file is opened and a list is made by splitting the file into lines
        """
        f = open(notestxt, 'r')
        file = f.read()
        f.close()
        notes_split = file.split(".")
        notes_split = [x for x in notes_split if x.strip()]  # removes any lists with just spaces
        ln = len(notes_split)
        words = []
        local_list = []
        local_list_start = 0
        local_list_end = 0
        local_text = ""  # local text send to gTTS
        """
        counting # of lines and # of words.
        If number of lines is less than the # of processors, going to the divide the work by groups of words
        """
        if ln < size:
            notes_split = file.split()
            notes_split = [x for x in notes_split if x.strip()]  # removes any lists with just spaces
            n = len(notes_split)
            div_cat = "words"
            separator = " "
        else:
            div_cat = "lines"
            n = ln
            separator = ". "
        """
        This section of the code refers 
        https://www.kth.se/blogs/pdc/2019/08/parallel-programming-in-python-mpi4py-part-1/.
        """
        local_n, remainder = divmod(n, size)
        counts = [local_n + 1 if i < remainder else local_n for i in range(size)]
        # determine the starting and ending indices of each sub-task
        starts = [sum(counts[:p]) for p in range(size)]
        ends = [sum(counts[:p + 1]) for p in range(size)]
        notes2send = [notes_split[starts[p]:ends[p]] for p in range(size)]
    else:
        notes2send = None
    # Send the separator
    separator = comm.bcast(separator, root=0)
    local_text = comm.scatter(notes2send, root=0)
    text2send = separator.join(local_text) + "."

    language = 'en'

    speech = gTTS(text=text2send, lang=language, slow=False)
    speechfile = "/mnt/Audiofiles/audiofiles/voice" + str(rank) + ".wav"
    speech.save(speechfile)
    # Gives time for individual nodes to perform the conversion
    comm.Barrier()
    if rank == 0:

        # Calls the function to combine the audio
        combineaudio(filename)
        # Calls the function to remove the individual files created by individual nodes
        remove_audio(size)


