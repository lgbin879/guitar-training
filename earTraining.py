# -*- coding: utf-8 -*-
# @Time     : 2019/01/08 
# @Author   : liguibin
#

###
'''
usage: fretboardTraining.py [-h] [-i INSTRUMENT] [-s STRINGS] [-f FRETS]
                            [-r RANGE] [-d [DELAY]] [-w] [-m] [-n] [-c]

random generate A-G pitches and play the sound

optional arguments:
  -h, --help            show this help message and exit
  -i INSTRUMENT, --instrument INSTRUMENT
                        instrument: piano/guitar
  -s STRINGS, --strings STRINGS
                        strings number: 1-6
  -f FRETS, --frets FRETS
                        specify frets range like 0-12
  -r RANGE, --range RANGE
                        Note range like C4-C5
  -d [DELAY], --delay [DELAY]
                        delay secs after bee
  -w, --word            not play character sound A-G
  -m, --music           not play pitch sound
  -n, --natrual         natrual pitches
  -c, --chromatic       chromatic pitches

'''

import os
import re
import sys
import time
import random
import argparse
import subprocess
from time import sleep

natrualPitches = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
twelvePitches = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
chromaticPitches = ['C#', 'D#', 'F#', 'G#', 'A#']

piano7Pitches = ['C2', 'D2', 'E2', 'F2', 'G2', 'A2', 'B2', 
 'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 
 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 
 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 
 'C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6',
 'C7']
pianoHalfPitches = ['C#2', 'D#2', 'F#2', 'G#2', 'A#2', 
 'C#3', 'D#3', 'F#3', 'G#3', 'A#3', 
 'C#4', 'D#4', 'F#4', 'G#4', 'A#4', 
 'C#5', 'D#5', 'F#5', 'G#5', 'A#5', 
 'C#6', 'D#6', 'F#6', 'G#6', 'A#6']
piano12Pitches = ['C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2', 
 'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 
 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 
 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5', 
 'C6', 'C#6', 'D6', 'D#6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6',
 'C7']

natrual3Chords = [  
'C', 'Cm',   
'D', 'Dm',   
'E', 'Em',   
'F', 'Fm',   
'G', 'Gm', 
'A', 'Am',   
'B', 'Bm' ]

chromatic3Chords = [
'Ab', 'Abm', 
'Bb', 'Bbm', 
'Eb', 'Ebm', 
'F#', 'F#m' ]

intervalNames = [
['Unison'],
['Minor 2nd', 'Major 2nd'],
['Minor 3rd', 'Major 3rd'],
['Perfect 4th'],
['Tritone'],
['Perfect 5th'],
['Minor 6th', 'Major 6th'],
['Minor 7th', 'Major 7th'],
['Octave'],

['Minor 9th', 'Major 9th'],
['Minor 10th', 'Major 10th'],
['Perfect 11th'],
['Diminished 12th','Perfect 12th'],
['Minor 13th', 'Major 13th'],
['Minor 14th', 'Major 14th'],
['Double Octave'],

]

# half pitch number of each scale
scaleDict = {
    'Natural Major' : [0,2,2,1,2,2,2,1],                  #: C,D,E,F,G,A,B,C
    'Natural Minor' : [0,2,1,2,2,1,2,2],          #: C,D,Eb,F,G,Ab,Bb,C
    'Harmonic Minor' : [0,2,1,2,2,1,3,1],         #: C,D,Eb,F,G,Ab,B,C
    'Melodic Minor' : [0,2,1,2,2,2,2,1],          #: C,D,Eb,F,G,A,B,C

    'Ionian' : [0,2,2,1,2,2,2,1],                 #: C,D,E,F,G,A,B,C
    'Dorian' : [0,2,1,2,2,2,1,2],                 #: C,D,Eb,F,G,A,Bb,C
    'Phrygian' : [0,1,2,2,2,1,2,2],               #: C,Db,Eb,F,G,Ab,Bb,C
    'Lydian' : [0,2,2,2,1,2,2,1],                 #: C,D,E,F#,G,A,B,C
    'Mixolydian' : [0,2,2,1,2,2,1,2],             #: C,D,E,F,G,A,Bb,C
    'Aeolian' : [0,2,1,2,2,1,2,2],                #: C,D,Eb,F,G,Ab,Bb,C
    'Locrian' : [0,1,2,2,1,2,2,2],                #: C,Db,Eb,F,Gb,Ab,Bb,C
}

cChords = ['C', 'Dm', 'Em', 'F', 'G', 'Am']

notePath = './ogg/spell/note/'
soundPath = './ogg/pitchSound/piano/'

guitarChordPath = 'ogg/chords/guitar/'
pianoChordPath = 'ogg/chords/piano/'
chordNamePath = 'ogg/spell/chords/'
scaleNamePath = 'ogg/spell/scale/'


def playKeys(noteChoice):
    for noteName in noteChoice:
        musicPath = soundPath+noteName+'.ogg'
        namePath = notePath+noteName+'.ogg'

        p = subprocess.Popen(["mplayer", musicPath], stdout=subprocess.PIPE)
        sleep(2)

        #print('\n## Info ## : ', '----------------------', noteName, '\n')
        #p = subprocess.Popen(["mplayer", namePath], stdout=subprocess.PIPE)
        #sleep(2)

def noteTraining(args):
    print('\n##### Note Ear Training Mode, Range %s #####\n'%(args.range))

    noteRange = args.range.split('-')
    noteStart = noteRange[0]
    noteEnd = noteRange[-1]

    if args.natrual:
        noteList = piano7Pitches
    elif args.chromatic:
        noteList = pianoHalfPitches
    else:
        noteList = piano12Pitches

    if noteStart not in noteList or noteEnd not in noteList:
        print('## Error :', noteStart, noteEnd, 'not in', noteList)
        sys.exit()


    noteChoice = noteList[noteList.index(noteStart):noteList.index(noteEnd)+1]

    if args.natrual:
        print('\n#### Natrual Pitches Only ####\n')
    elif args.chromatic:
        print('\n#### Chromatic Pitches Only ####\n')
    else:
        print('\n#### All 12 Pitches ####\n')

    print(noteChoice)

    playKeys(noteChoice)

    while(True):
        noteName = random.choice(noteChoice)

        musicPath = soundPath+noteName+'.ogg'
        namePath = notePath+noteName+'.ogg'

        p = subprocess.Popen(["mplayer", musicPath], stdout=subprocess.PIPE)
        sleep(2)

        print('\n## Info ## : ', '----------------------', noteName, '\n')
        p = subprocess.Popen(["mplayer", namePath], stdout=subprocess.PIPE)
        sleep(args.delay)


def playChords(chordChoice, args):
    if args.instrument == 'guitar':
        chordPath = guitarChordPath
    else:
        chordPath = pianoChordPath

    for chordName in chordChoice:
        musicPath = chordPath+chordName+'.mp3'

        p = subprocess.Popen(["mplayer", musicPath], stdout=subprocess.PIPE)
        sleep(5)


def chordTraining(args):
    print('\n##### Chord Ear Training Mode, Range %s #####\n'%(args.range))

    if args.instrument == 'guitar':
        chordPath = guitarChordPath
    else:
        chordPath = pianoChordPath

    if args.natrual:
        chordList = natrual3Chords
    elif args.chromatic:
        chordList = chromatic3Chords
    else:
        chordList = natrual3Chords+chromatic3Chords

    if args.scale == 'C':
        chordList = cChords

    chordChoice = chordList

    print(chordChoice)

    playChords(chordChoice, args)

    while(True):
        chordName = random.choice(chordChoice)

        musicPath = chordPath+chordName+'.mp3'
        namePath = chordNamePath+chordName+'.mp3'

        p = subprocess.Popen(["mplayer", musicPath], stdout=subprocess.PIPE)
        sleep(5)

        print('\n## Info ## : ', '----------------------', chordName, '\n')
        p = subprocess.Popen(["mplayer", namePath], stdout=subprocess.PIPE)
        sleep(args.delay)

def intervalTraining(args):
    pass


def scaleTraining(args):
    print('\n##### Scale Ear Training Mode, Range %s #####\n'%(args.range))

    noteRange = args.range.split('-')
    noteStart = noteRange[0]
    noteEnd = noteRange[-1]

    noteList = piano12Pitches

    if noteStart not in noteList or noteEnd not in noteList:
        print('## Error :', noteStart, noteEnd, 'not in', noteList)
        sys.exit()


    noteChoice = noteList[noteList.index(noteStart):noteList.index(noteEnd)+1]
    scaleChoice = list(scaleDict.keys())

    while(True):
        firstNote = random.choice(noteChoice)
        scaleName = random.choice(scaleChoice)
        scaleSpell = scaleNamePath+scaleName.replace(' ','')+'.mp3'

        scaleStep = scaleDict[scaleName]
        scaleBuff = []
        noteName = firstNote

        for step in scaleStep:
            noteName = noteList[noteList.index(noteName)+step]
            scaleBuff.append(noteName)

            musicPath = soundPath+noteName+'.ogg'
            namePath = notePath+noteName+'.ogg'

            p = subprocess.Popen(["mplayer", musicPath], stdout=subprocess.PIPE)
            sleep(1)

        print('\n## Info ## : ', '----------------------', scaleName, ':', scaleBuff, '\n')
        p = subprocess.Popen(["mplayer", scaleSpell], stdout=subprocess.PIPE)
        sleep(args.delay)    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='random generate A-G pitches and play the sound')
    parser.add_argument("-i", "--instrument", help="instrument: piano/guitar")
    parser.add_argument("-m", "--mode", default='note', type=str, help="note/interval/chord/scale")
    parser.add_argument("-s", "--scale", default='C', type=str, help="C/D/E/F/G/A/B")
    parser.add_argument("-r", "--range", default='C4-C5', type=str, help="Note range like C4-C5")
    parser.add_argument("-d", "--delay", default=5, type=int, nargs='?', help="delay secs after bee")
    parser.add_argument("-w", "--word", help="not play character sound A-G", action="store_true")
    parser.add_argument("-n", "--natrual", help="natrual pitches", action="store_false")
    parser.add_argument("-c", "--chromatic", help="chromatic pitches", action="store_true")

    args = parser.parse_args()
    print(args)

    if args.mode == 'note':
        noteTraining(args)
    elif args.mode == 'chord':
        chordTraining(args)
    elif args.mode == 'scale':
        scaleTraining(args)
    else:
        pass

