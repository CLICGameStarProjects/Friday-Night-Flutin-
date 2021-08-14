import sounddevice as sd
import numpy as np
import scipy.fftpack
import os
import pydirectinput
from pynput import keyboard
import time

# General settings
SAMPLE_FREQ = 44100 # sample frequency in Hz
WINDOW_SIZE = 44100 # window size of the DFT in samples
WINDOW_STEP = 4000 # step size of window
WINDOW_T_LEN = WINDOW_SIZE / SAMPLE_FREQ # length of the window in seconds
SAMPLE_T_LENGTH = 1 / SAMPLE_FREQ # length between two samples in seconds
windowSamples = [0 for _ in range(WINDOW_SIZE)]

# This function finds the closest note for a given pitch
# Returns: note (e.g. A4, G#3, ..), pitch of the tone
CONCERT_PITCH = 440
listening = False
active = True
input = keyboard.Controller()

#Keys
TOGGLE = keyboard.Key.shift
STOP = keyboard.Key.esc

#The order of the keys are from left to right in FNF.
P1LEFT = ['left']
P1DOWN = ['down']
P1UP = ['up']
P1RIGHT = ['right']

P2LEFT = ['a']
P2DOWN = ['s']
P2UP = ['w']
P2RIGHT = ['d']

#Notes
P1LEFTNOTE = 'E4'
P1DOWNNOTE = 'F4'
P1UPNOTE = 'G4'
P1RIGHTNOTE = 'A4'

P2LEFTNOTE = 'E5'
P2DOWNNOTE = 'F5'
P2UPNOTE = 'G5'
P2RIGHTNOTE = 'A5'

players = {P1UPNOTE:P1UP, P1LEFTNOTE:P1LEFT, P1RIGHTNOTE:P1RIGHT, P1DOWNNOTE:P1DOWN,
           P2UPNOTE:P2UP, P2LEFTNOTE:P2LEFT, P2RIGHTNOTE:P2RIGHT, P2DOWNNOTE:P2DOWN}

def on_press(key):
    global listening
    #Toggle whether input are sent or not by pressing shift
    if key == TOGGLE:
        listening = not listening
        print("Listening : ", listening)

    #Emergency stop by pressing ESC
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
  if i < -2 and i > -10 or i < -14:
    corr = 1
  closestNote = ALL_NOTES[i%12] + str(4 + corr + np.sign(i) * int((9+abs(i))/12) )
  closestPitch = CONCERT_PITCH*2**(i/12)
  return closestNote, closestPitch

# The sounddecive callback function
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
    start = time.time()
    while active:
        if time.time() - start > 0.2 and listening and not next_key == current_key:
            for key in next_key:
                pydirectinput.keyDown(key)
            for key in next_key:
                pydirectinput.keyUp(key)
            start = time.time()
            current_key = next_key
except Exception as e:
    print(str(e))