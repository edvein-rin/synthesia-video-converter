# Algorithm


## I. Preprocessing


### 1. Input

On the input comes either a video with **Synthesia** (or any other piano roll) recording (directly imported into the script) or **YouTube** video link (video downloaded and processed as video input).

### 2. Clearing

Defining where intro, outro and other not related to the piano play parts of the video are and cutting them off (basically defining where actual play parts are).

Done by recognizing the piano keyboard: if keyboard in on the screen then likely that this part is a play part.


## II. Processing


### 1. Determining the pitch

The audio is being processed to determine the pitch in which first left pressed key is played.  

It is required as ofter in the video it is shown only a part of the keyboard and it's not clear what the first visible octave is without the audio.  

### 2. Defining keys played

Each frame of the video is being processed via methods of **Computer Vision** to extract information about what keys to play, when, with what power and with which hand if possible to determine.  


#### a. Thresholding the frame

First of all [contrast of the frame is increased](https://medium.com/dataseries/designing-image-filters-using-opencv-like-abode-photoshop-express-part-1-8765e3f4495b), then the frame is [converted into a grey scale](https://docs.opencv.org/3.4/d8/d01/group__imgproc__color__conversions.html#gga4e0972be5de079fed4e3a10e24ef5ef0a353a4b8db9040165db4dacb5bcefb6ea), then [Gaussian blur](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html) is applied, then threshold ([Otsu's Binarization](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html)) and finally [advanced morphological transformation of opening](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html).  

This step is crucial for final precision.

<!-- TODO add example of original image and thresholded to compare -->

#### b. Cutting the frame

Frame is cut to a height of a 1 pixel and only this thin line is being used for future analysis.

#### c. Defining the virtual keyboard

Determining keys size and paddings between them.  

Determined by falling keys approximate shape rectangle size. The whole song should be analyzed to detect a correct size.

#### d. Marking falling keys with actual musical notes

Using bottom part of the frame as a play line to determine keys played at the moment. Each keys is marked with a pitch.  
The power with which keys should be pressed (a volume value) is determined via audio analysis.

#### f. Separating keys by hand played with  

Colors of keys in the video (if they are present) are used to determine different hands.  
It is possible to use player hands to determine what hands to use to press keys, but that's a hard challenge to deal with.

#### e. Combining close falling keys into one

Same musical note pressed without a pause marks as a single note with specific duration.


## III. Postprocessing


### 1. Saving gathered information

The gathered information is being combined and saved in the **MusicXML** format ([https://www.musicxml.com/](https://www.musicxml.com/)).

### 2. Output

Using library [music21](http://web.mit.edu/music21/) the **MusicXML** file is being converter into **MIDI** file and sheet music **PDF** that are the the output of the program.
