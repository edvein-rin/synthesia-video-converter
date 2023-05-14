# Algorithm


## I. Preprocessing


### 1. Input

On the input comes either a video with **Synthesia** (or any other piano roll) recording (directly imported into the script) or **YouTube** video link (video downloaded and processed as video input).

### 2. Clearing

Defining where intro, outro and other not related to the piano play parts of the video are and cutting them off (basically defining where actual play parts are).


## II. Processing


### 1. Determining the pitch

The audio is being processed to determine the pitch in which first left pressed key is played.  

It is required as ofter in the video it is shown only a part of the keyboard and it's not clear what the first visible octave is without the audio.  

### 2. Defining keys played

The video is being processed via methods of **Computer Vision** to extract information about what keys to play, when, with what power and with which hand if possible to determine.  

#### a. Identifying falling keys as rectangles  

For this is used a threshold filter for creating an image mask and CV object detection.  

#### b. Defining the play line

Defining the line where notes are played on an intersection with.  

Defined by finding a line where falling keys disappear.

#### c. Determining the keyboard

Determining keys size and paddings between them.  

Determined by rectangles size. The whole song should be analyzed to detect a correct size.

#### d. Falling keys are marked with actual musical notes

Each key is being marked with a pitch and a duration.  
The power with which keys should be pressed (a volume value) is determined via audio analysis.

#### e. Separating keys by hand played with  

Colors of keys in the video (if they are present) are used to determine different hands.  
It is possible to use player hands to determine what hands to use to press keys, but that's a hard challenge to deal with.



## III. Postprocessing


### 1. Saving gathered information

The gathered information is being combined and saved in the **MusicXML** format ([https://www.musicxml.com/](https://www.musicxml.com/)).

### 2. Output

Using library [music21](http://web.mit.edu/music21/) the **MusicXML** file is being converter into **MIDI** file and sheet music **PDF** that are the the output of the program.
