# Algorithm

On the input comes either video or link to the YouTube video with Synthesia (or any other piano roll) recording.  

The video is being process via methods of Computer Vision to extract information about keys to play and saved in the **MusicXML** format ([https://www.musicxml.com/](https://www.musicxml.com/)).

After this using library [music21](http://web.mit.edu/music21/) the **MusicXML** file is being converter into **MIDI** file and sheet music **PDF** that are the the output of the program.
