import sounddevice as sd
import numpy as np
import scipy.fftpack
import os
import pydirectinput
from pynput import keyboard
import time

# General settings - to fine-tune
SAMPLE_FREQ = 48000 # sample frequency in Hz
WINDOW_SIZE = 15000 # window size of the DFT in samples
WINDOW_STEP = 5000 # step size of window
WINDOW_T_LEN = WINDOW_SIZE / SAMPLE_FREQ # length of the window in seconds
SAMPLE_T_LENGTH = 1 / SAMPLE_FREQ # length between two samples in seconds
windowSamples = [0 for _ in range(WINDOW_SIZE)]

# This function finds the closest note for a given pitch
# Returns: note (e.g. A4, G#3, ..), pitch of the tone
CONCERT_PITCH = 440
listening = False
active = True
input = keyboard.Controller()

#control keys
TOGGLE = keyboard.Key.shift
STOP = keyboard.Key.esc

# The order of the keys are from left to right in FNF. Note that those are
#lists in order to be able to press several keys at once if needed
P1LEFT = ['left']
P1DOWN = ['down']
P1UP = ['up']
P1RIGHT = ['right']

P2LEFT = ['a']
P2DOWN = ['s']
P2UP = ['w']
P2RIGHT = ['d']

#Notes
P1LEFTNOTE = 'F5'
P1DOWNNOTE = 'E5'
P1UPNOTE = 'D5'
P1RIGHTNOTE = 'C5'

P2LEFTNOTE = 'C#5'
P2DOWNNOTE = 'B5'
P2UPNOTE = 'A5'
P2RIGHTNOTE = 'G5'

players = {P1UPNOTE:P1UP, P1LEFTNOTE:P1LEFT, P1RIGHTNOTE:P1RIGHT, P1DOWNNOTE:P1DOWN,
           P2UPNOTE:P2UP, P2LEFTNOTE:P2LEFT, P2RIGHTNOTE:P2RIGHT, P2DOWNNOTE:P2DOWN}

def on_press(key):
    global listening
    #Toggle whether input are sent or not
    if key == TOGGLE:
        listening = not listening
        print("Listening : ", listening)

    #Emergency stop
    if key == STOP:
        # Stop listener
        global active
        active = False
        return False

def on_release(key):
    pass

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

ALL_NOTES = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]

def find_closest_note(pitch):
  i = int( np.round( np.log2( pitch/CONCERT_PITCH )*12 ) )
  corr = 0
  #Shady correction from original
  if i < -2 and i > -10 or i < -14:
    corr = 1
  closestNote = ALL_NOTES[i%12] + str(4 + corr + np.sign(i) * int((9+abs(i))/12) )
  closestPitch = CONCERT_PITCH*2**(i/12)
  return closestNote, closestPitch

# The sounddevice callback function
# Provides us with new data once WINDOW_STEP samples have been fetched
def callback(indata, frames, time, status):
  global windowSamples
  global next_key
  global current_key
  global players

  if status:
    print(status)
  if any(indata):
    windowSamples = np.concatenate((windowSamples,indata[:, 0])) # append new samples
    windowSamples = windowSamples[len(indata[:, 0]):] # remove old samples
    magnitudeSpec = abs( scipy.fftpack.fft(windowSamples)[:len(windowSamples)//2] )

    for i in range(int(62/(SAMPLE_FREQ/WINDOW_SIZE))):
      magnitudeSpec[i] = 0 #suppress mains hum

    maxInd = np.argmax(magnitudeSpec)
    maxFreq = maxInd * (SAMPLE_FREQ/WINDOW_SIZE)
    closestNote, closestPitch = find_closest_note(maxFreq)
    if closestNote in players.keys():
        next_key = players.get(closestNote)
    else :
        next_key = ['']


    os.system('cls' if os.name=='nt' else 'clear')
    print(f"Closest note: {closestNote} {maxFreq:.1f}/{closestPitch:.1f}")

  else:
    print('no input')


# Start the microphone input stream
try:
  with sd.InputStream(channels=1, callback=callback,
    blocksize=WINDOW_STEP,
    samplerate=SAMPLE_FREQ):
    print("Listening : ", listening)
    current_key = ''
    while active:
        # Pressing every key once. This means we can't play the same note several
        # times in a row. TODO : maybe find a way to do this ?
        if listening and not next_key == current_key:
            for key in next_key:
                pydirectinput.keyDown(key)
                pydirectinput.keyUp(key)
            current_key = next_key
except Exception as e:
    print(str(e))
