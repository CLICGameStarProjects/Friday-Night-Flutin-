# Friday night flutin'
## Content
This repo contains :
- `pitch_to_inputs.py`, a Python3 script to play the multiplayer version of the Friday Night Funkin' game (found [here](https://shadowmario.itch.io/funkinmulti)) that takes an audio input and orchestrates keyboard outputs.
The script was made from GitHub user `not-chciken`'s guitar tuner (repo [here](https://github.com/not-chciken/guitar_tuner)), released under no license. The verbatim copy was acquired on March 2, 2021 and was then modified independently from the original owner's updates.
- This README
- `LICENSE`, detailing the license under which this project is released
- `reqs.txt`, the list of dependencies this project was built from.

## Dependencies and installation

This program was made in Python 3.8.5. To install Python on your device, you can follow [this tutorial](https://phoenixnap.com/kb/how-to-install-python-3-windows). The project was developed and tested on Windows only although I am pretty confident that it may be portable to other OS, with some eventual work to be done on finding corresponding libraries.

The following libraries are needed :
- `numpy` (for various operations)
- `scipy` (in particular `scipy.fftpack`) for pitch recognition
- `sounddevice` for audio streaming input
- `pynput` to listen to keyboard presses
- `pydirectinput` to simulate keyboard presses.

You can either install them individually, or run
```
pip install -Ur req.txt
```
to install them all at once.

These libraries are published under their respective licenses, that can be found on their websites.

## Usage
##### Gettin flutin'
Launch the script : `python pitch_to_inputs.py`

##### Control keys
To make for easier pitch calibration, the script will detect pitch but will not simulate key presses until the `TOGGLE` key is pressed (by default, the `SHIFT` key). Key press simulations can be stopped at anytime by pressing the `TOGGLE` key once more. At any moment, the script can be stopped by pressing the `STOP` key (by default, `ESC`).

The `TOGGLE` and `STOP` keys can be modified at `pitch_to_inputs.py:25`

##### Changing mappings

To change the note-to-key mappings, change lines `pitch_to_inputs.py:29` to `pitch_to_inputs.py:48`.

For example,
```
P1UP = ['a']
[...]
P1UPNOTE = 'E4'
```
Means that when the pitch detection part of the script detects an E4 (E in the 4th octave), it will simulate the press of the 'a' key. the keys are single-element lists, in order to allow for multi-key notes.
